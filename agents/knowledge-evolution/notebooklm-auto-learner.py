#!/usr/bin/env python3
"""
NotebookLM 自动学习系统
自动监控已有来源、发现新来源、提炼知识到 intake
"""

import json
import os
import re
import subprocess
import sys
import feedparser
import html
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# 知识库路径
KB_ROOT = Path("/Users/baimengke/Documents/白梦客知识库")
INTAKE_DIR = KB_ROOT / "intake" / "主动学习"
LOG_DIR = Path("/tmp/knowledge-evolution")
NOTEBOOK_SOURCES_FILE = LOG_DIR / "notebook-sources.json"
PENDING_SOURCES_FILE = LOG_DIR / "notebook-pending.json"

# NotebookLM skill 路径
NOTEBOOKLM_SKILL = Path("/Users/baimengke/.claude/skills/notebooklm")
NOTEBOOKLM_SCRIPTS = NOTEBOOKLM_SKILL / "scripts"


def init():
    """初始化目录"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    INTAKE_DIR.mkdir(parents=True, exist_ok=True)


def load_notebook_sources() -> Dict:
    """加载已追踪的 notebook 来源"""
    if not NOTEBOOK_SOURCES_FILE.exists():
        return {"notebooks": [], "last_full_scan": None}

    try:
        with open(NOTEBOOK_SOURCES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"notebooks": [], "last_full_scan": None}


def save_notebook_sources(data: Dict):
    """保存 notebook 来源"""
    with open(NOTEBOOK_SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_pending_sources() -> Dict:
    """加载待确认来源"""
    if not PENDING_SOURCES_FILE.exists():
        return {"pending": [], "confirmed": [], "rejected": []}

    try:
        with open(PENDING_SOURCES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"pending": [], "confirmed": [], "rejected": []}


def save_pending_sources(data: Dict):
    """保存待确认来源"""
    with open(PENDING_SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_notebook_list() -> List[Dict]:
    """获取 NotebookLM notebook 列表"""
    library_file = NOTEBOOKLM_SKILL / "data" / "library.json"
    if not library_file.exists():
        return []

    try:
        with open(library_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            notebooks = data.get("notebooks", {})
            return [
                {
                    "id": vid,
                    "name": v.get("name", ""),
                    "url": v.get("url", ""),
                    "topics": v.get("topics", []),
                    "last_checked": v.get("last_checked")
                }
                for vid, v in notebooks.items()
            ]
    except Exception as e:
        print(f"  ⚠️ 读取 notebook 库失败: {e}")
        return []


def check_source_for_updates(source: Dict) -> bool:
    """
    检查来源是否有更新
    通过抓取 RSS 或网页检查修改时间
    """
    url = source.get("url", "")
    if not url:
        return False

    # 检查 RSS 源
    if "feed" in url.lower() or url.endswith(".xml"):
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                # 获取最新条目时间
                latest = feed.entries[0]
                if hasattr(latest, "published_parsed") and latest.published_parsed:
                    import time
                    latest_time = time.mktime(latest.published_parsed)
                    last_checked = source.get("last_update_time", 0)
                    return latest_time > last_checked
        except Exception:
            pass

    return False


def fetch_rss_entries(url: str, max_entries: int = 5) -> List[Dict]:
    """抓取 RSS 源条目"""
    try:
        feed = feedparser.parse(url)
        entries = []

        for entry in feed.entries[:max_entries]:
            # 清理 HTML
            summary = ""
            if hasattr(entry, "summary"):
                summary = re.sub(r"<[^>]+>", "", entry.summary)
            elif hasattr(entry, "description"):
                summary = re.sub(r"<[^>]+>", "", entry.description)

            entries.append({
                "title": getattr(entry, "title", "无标题"),
                "link": getattr(entry, "link", ""),
                "summary": summary[:200] if summary else "",
                "published": getattr(entry, "published", "")
            })

        return entries
    except Exception as e:
        print(f"  ⚠️ RSS 解析失败 {url}: {e}")
        return []


def discover_new_sources() -> List[Dict]:
    """
    主动发现新来源
    通过搜索 AI广告/视频相关的 RSS 源
    """
    print("  主动发现新来源...")

    # 已知的高质量 RSS 源列表
    known_feeds = [
        {
            "name": "AI 优先",
            "url": "https://feeds.feedburner.com/techcrunchAI",
            "topics": ["AI", "创业", "科技"],
            "relevance": "high"
        },
        {
            "name": "VentureBeat AI",
            "url": "https://venturebeat.com/ai/feed/",
            "topics": ["AI", "机器学习", "企业AI"],
            "relevance": "high"
        },
        {
            "name": "Adweek",
            "url": "https://www.adweek.com/feed/",
            "topics": ["广告", "营销", "品牌"],
            "relevance": "medium"
        },
        {
            "name": "Campaign US",
            "url": "https://www.campaignlive.com/rss.xml",
            "topics": ["广告", "创意", "营销"],
            "relevance": "medium"
        },
    ]

    discovered = []

    for feed in known_feeds:
        # 检查是否已存在
        sources = load_notebook_sources()
        existing_urls = [n.get("url", "") for n in sources.get("notebooks", [])]

        if feed["url"] in existing_urls:
            continue

        # 验证 RSS 源是否可用
        entries = fetch_rss_entries(feed["url"], max_entries=1)
        if entries:
            feed["entry_count"] = len(entries)
            feed["latest_title"] = entries[0]["title"]
            discovered.append(feed)
            print(f"    发现: {feed['name']} - {entries[0]['title'][:40]}...")

    print(f"    共发现 {len(discovered)} 个候选来源")
    return discovered


def evaluate_source(source: Dict) -> Dict:
    """
    评估来源质量
    """
    score = 5.0

    # 高权威来源
    high_authority = ["venturebeat", "techcrunch", "adweek", "campaign", "digiday"]
    for kw in high_authority:
        if kw in source.get("url", "").lower():
            score = 8.0
            break

    # 高相关关键词
    high_relevance = ["ai", "advertising", "creative", "video", "生成"]
    medium_relevance = ["marketing", "brand", "content"]

    url_lower = source.get("url", "").lower()
    topics_str = " ".join(source.get("topics", [])).lower()

    if any(kw in url_lower or kw in topics_str for kw in high_relevance):
        score = max(score, 7.0)
    elif any(kw in url_lower or kw in topics_str for kw in medium_relevance):
        score = max(score, 6.0)

    return {
        "score": score,
        "relevance": "high" if score >= 7 else "medium",
        "authority": "high" if score >= 8 else "medium"
    }


def send_notification(message: str):
    """发送 macOS 通知"""
    script = f'display notification "{message}" with title "NotebookLM 新来源待确认"'
    subprocess.run(["osascript", "-e", script], capture_output=True)


def generate_add_command(source: Dict) -> str:
    """生成添加 notebook 的命令"""
    topics_str = ",".join(source.get("topics", []))
    return f'''python3 scripts/run.py notebook_manager.py add \\
  --url "{source['url']}" \\
  --name "{source['name']}" \\
  --description "{source.get('description', 'AI广告创作相关来源')}" \\
  --topics "{topics_str}"'''


def add_pending_source(source: Dict):
    """添加待确认来源"""
    pending = load_pending_sources()

    # 检查是否已存在
    for p in pending["pending"]:
        if p["url"] == source["url"]:
            return

    evaluation = evaluate_source(source)
    source["evaluation"] = evaluation

    pending["pending"].append({
        "name": source["name"],
        "url": source["url"],
        "description": source.get("description", ""),
        "topics": source.get("topics", []),
        "discovered_at": datetime.now().isoformat(),
        "status": "pending",
        "evaluation": evaluation
    })

    save_pending_sources(pending)

    # 发送通知
    print(f"\n📢 发现新来源待确认")
    print(f"   来源：{source['name']}")
    print(f"   URL：{source['url']}")
    print(f"   评估：{evaluation['relevance']} | 权威性：{evaluation['authority']}")
    print(f"\n添加命令：\n{generate_add_command(source)}")

    send_notification(f"发现新来源：{source['name']}")


def extract_knowledge_from_notebook(notebook: Dict) -> List[Dict]:
    """
    从 NotebookLM notebook 提炼知识
    使用 ask_question.py 向 notebook 提问
    """
    print(f"  从 {notebook['name']} 提炼知识...")

    # 提炼问题
    questions = [
        "总结这个笔记本中关于AI视频广告创作的核心知识点（3条）",
        "有哪些可以直接应用的AI视频提示词或技法？",
        "有哪些行业趋势和创新案例？"
    ]

    knowledge_items = []

    for question in questions:
        try:
            result = subprocess.run(
                [
                    "python3",
                    str(NOTEBOOKLM_SCRIPTS / "run.py"),
                    "ask_question.py",
                    "--question", question,
                    "--notebook-url", notebook["url"]
                ],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(NOTEBOOKLM_SCRIPTS.parent)
            )

            if result.returncode == 0 and result.stdout:
                knowledge_items.append({
                    "question": question,
                    "answer": result.stdout.strip()
                })

        except subprocess.TimeoutExpired:
            print(f"    ⏱️ 提问超时，跳过")
        except Exception as e:
            print(f"    ⚠️ 提问失败: {e}")

    return knowledge_items


def save_to_intake(knowledge_items: List[Dict], source: Dict):
    """保存提炼结果到 intake"""
    if not knowledge_items:
        return

    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_title = re.sub(r"[^\w\s\u4e00-\u9fff]", "", source.get("name", "untitled"))[:30]
    filename = f"{date_str}_NotebookLM_{safe_title}.md"
    filepath = INTAKE_DIR / filename

    # 避免重名
    counter = 1
    while filepath.exists():
        filepath = INTAKE_DIR / f"{date_str}_NotebookLM_{safe_title}_{counter}.md"
        counter += 1

    # 构建内容
    content = f"""---
来源: {source.get('name', 'Unknown')}
来源URL: {source.get('url', 'N/A')}
类型: NotebookLM提炼
自动提炼日期: {date_str}
提炼自: NotebookLM auto-learn
---

# {source.get('name', '无标题')} 知识提炼

"""

    for i, item in enumerate(knowledge_items, 1):
        content += f"## 问题 {i}\n"
        content += f"{item['question']}\n\n"
        content += f"### 答案\n{item['answer']}\n\n---\n\n"

    content += f"""*本条目由 NotebookLM 自动学习系统生成*
"""

    filepath.write_text(content, encoding="utf-8")
    print(f"  ✅ 保存到 intake: {filepath.name}")


def run():
    """主运行函数"""
    init()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] NotebookLM 自动学习开始...")

    # 1. 获取已有 notebook 列表
    print("\n📋 检查已有 NotebookLM 来源...")
    notebooks = get_notebook_list()
    print(f"  已追踪 {len(notebooks)} 个 notebook")

    # 2. 检查来源更新并提炼知识
    sources_updated = 0
    for notebook in notebooks:
        has_update = check_source_for_updates(notebook)
        if has_update:
            sources_updated += 1
            # 提炼新知识
            knowledge = extract_knowledge_from_notebook(notebook)
            if knowledge:
                save_to_intake(knowledge, notebook)

            # 更新来源记录
            notebook["last_checked"] = datetime.now().isoformat()
            notebook["last_update_time"] = datetime.now().timestamp()

    if notebooks:
        print(f"  {sources_updated} 个来源有新内容")

    # 3. 主动发现新来源
    print("\n🔍 主动发现新来源...")
    new_sources = discover_new_sources()

    for source in new_sources:
        # 所有发现的来源都加入待确认队列
        add_pending_source(source)

    # 4. 检查待确认队列
    pending = load_pending_sources()
    if pending["pending"]:
        print(f"\n⏳ {len(pending['pending'])} 个来源待确认")
        for p in pending["pending"]:
            print(f"   - {p['name']}: {p['url']}")

    # 5. 更新最后扫描时间
    sources = load_notebook_sources()
    sources["notebooks"] = notebooks
    sources["last_full_scan"] = datetime.now().isoformat()
    save_notebook_sources(sources)

    # 6. 统计
    stats = {
        "notebooks_tracked": len(notebooks),
        "sources_updated": sources_updated,
        "new_discovered": len(new_sources),
        "pending_confirmation": len(pending["pending"])
    }

    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] NotebookLM 自动学习完成")
    print(f"  追踪 notebook: {stats['notebooks_tracked']}")
    print(f"  来源有更新: {stats['sources_updated']}")
    print(f"  新发现来源: {stats['new_discovered']}")
    print(f"  待确认: {stats['pending_confirmation']}")


if __name__ == "__main__":
    run()
