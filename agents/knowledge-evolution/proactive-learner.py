#!/usr/bin/env python3
"""
知识库主动学习系统
主动发现新知识，而非被动等待
"""

import os
import json
import re
import time

# status-writer integration
try:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from status_writer import write_task_status, update_stats
except ImportError:
    write_task_status = None
    update_stats = None
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set
from xml.etree import ElementTree as ET
import urllib.request
import urllib.error
import urllib.parse
import hashlib

# 知识库根目录
KB_ROOT = Path("/Users/baimengke/Documents/白梦客知识库")
INTAKE_DIR = KB_ROOT / "intake" / "主动学习"
# 追踪文件放在/tmp目录，避免沙盒权限问题
TRACKING_FILE = Path("/tmp/knowledge-evolution/proactive-tracking.json")

# 追踪关键词
TRACK_KEYWORDS = {
    "广告创意": [
        "AI广告", "虚拟广告", "AIGC广告", "AI创意",
        "虚拟拍摄", "AI生成视频", "Sora广告", "Gen3广告"
    ],
    "营销趋势": [
        "小红书营销", "抖音广告", "内容营销", "种草",
        "私域运营", "KOL营销", "KOC营销", "爆款文案", "病毒传播"
    ],
    "技术工具": [
        "MidJourney", "Vidu", "即梦"
    ],
    "行业动态": [
        "广告公司", "创意热店", "MCN机构", "品牌创意",
        "广告节", "Cannes", "One Show"
    ],
    "虚拟广告": [
        "虚拟广告复刻", "AI复刻广告", "虚拟拍摄",
        "AI虚拟广告", "Virtual Ad"
    ],
    "奢侈品香水": [
        "Chanel香水", "Dior香水", "Tom Ford香水", "Jo Malone",
        "Le Labo", "Byredo", "小众香水", "沙龙香"
    ],
    "奢侈品箱包": [
        "LV包", "Hermès Birkin", "Chanel包", "Dior包",
        "Gucci包", "Prada包", "Bottega", "奢侈品包", "顶奢"
    ],
    "服装品牌": [
        "奢侈品服装", "设计师品牌", "时尚大片", " runway",
        "LVMH", "开云集团", "历峰集团", "时尚广告"
    ]
}

# 竞品媒体源（官网/社媒RSS）
COMPETITOR_SOURCES = {
    "服装": [
        {"name": "ICICLE官方", "url": "https://www.icicle.com/news", "type": "web"},
        {"name": "JNBY官方", "url": "https://www.jnby.com/news", "type": "web"},
    ],
    "美妆": [
        {"name": "完美日记官方", "url": "https://www.perfectdaily.com/news", "type": "web"},
        {"name": "花西子官方", "url": "https://www.huaxizi.com/news", "type": "web"},
    ],
    "快消": [
        {"name": "元气森林", "url": "https://www.yuanqishenglin.com/news", "type": "web"},
    ],
    "电子": [
        {"name": "小米", "url": "https://www.mi.com/news", "type": "web"},
        {"name": "华为", "url": "https://www.huawei.com/cn/news", "type": "web"},
    ]
}

# 搜索源配置
SEARCH_SOURCES = {
    "news": {
        "name": "新闻搜索",
        "url_template": "https://www.baidu.com/s?wd={keyword}&tn=news&rtt=4&bsst=1&cl=2&wd={keyword}&medium=0",
        "type": "search"
    },
    "tech": {
        "name": "36kr搜索",
        "url_template": "https://36kr.com/search/articles/{keyword}",
        "type": "search"
    }
}


def get_tracking_data() -> Dict:
    """获取追踪数据"""
    if TRACKING_FILE.exists():
        with open(TRACKING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "last_run": None,
        "keywords_last_searched": {},  # 关键词 -> 上次搜索时间
        "sources_last_checked": {},      # 来源 -> 上次检查时间
        "articles_collected": 0,
        "findings": []  # 重大发现
    }


def save_tracking_data(data: Dict):
    """保存追踪数据"""
    data["last_run"] = datetime.now().isoformat()
    INTAKE_DIR.mkdir(parents=True, exist_ok=True)
    with open(TRACKING_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def hash_content(content: str) -> str:
    """内容哈希用于去重"""
    return hashlib.md5(content.encode('utf-8')).hexdigest()[:12]


def is_new_content(content_hash: str, seen_hashes: Set[str]) -> bool:
    """判断是否是新内容"""
    return content_hash not in seen_hashes


def fetch_url(url: str, timeout: int = 10) -> Optional[str]:
    """抓取URL内容"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read().decode('utf-8', errors='ignore')
            return content
    except Exception as e:
        print(f"   ⚠️ 抓取失败 {url}: {e}")
        return None


def search_news(keyword: str) -> List[Dict]:
    """搜索新闻"""
    results = []
    try:
        # URL编码关键词
        encoded_keyword = urllib.parse.quote(keyword)
        url = f"https://36kr.com/search/articles/{encoded_keyword}"
        content = fetch_url(url)
        if content:
            # 提取标题和链接
            titles = re.findall(r'<h3[^>]*class="[^"]*title[^"]*"[^>]*>(.*?)</h3>', content, re.DOTALL)
            links = re.findall(r'<a[^>]*href="(/p/\d+)"[^>]*>', content)

            for i, title in enumerate(titles[:5]):
                # 清理HTML
                title_clean = re.sub(r'<[^>]+>', '', title).strip()
                if title_clean and i < len(links):
                    link = f"https://36kr.com{links[i]}" if links[i].startswith('/') else links[i]
                    results.append({
                        "title": title_clean,
                        "url": link,
                        "source": "36kr",
                        "keyword": keyword,
                        "date": datetime.now().strftime("%Y-%m-%d")
                    })
    except Exception as e:
        print(f"   ⚠️ 搜索失败 {keyword}: {e}")

    return results


def analyze_content(title: str, content: str, keyword: str) -> Dict:
    """分析内容价值"""
    score = 0
    tags = []

    # 标题关键词加分
    positive_keywords = ["AI", "虚拟", "创新", "趋势", "案例", "复刻", "广告", "创意", "生成"]
    negative_keywords = ["广告法", "违规", "处罚", "下架"]

    for kw in positive_keywords:
        if kw in title:
            score += 1
            tags.append(kw)

    for kw in negative_keywords:
        if kw in title:
            score -= 2

    # 判断是否有价值
    is_valuable = score >= 1 and len(title) > 5

    return {
        "score": score,
        "tags": tags,
        "is_valuable": is_valuable,
        "summary": title[:100] if title else ""
    }


def save_finding(category: str, keyword: str, item: Dict, analysis: Dict) -> Path:
    """保存发现到intake"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    time_str = datetime.now().strftime('%H%M')

    # 生成安全文件名
    safe_keyword = re.sub(r'[^\w\s-]', '', keyword)[:20]
    safe_title = re.sub(r'[^\w\s-]', '', item.get('title', 'unknown'))[:30]
    filename = f"{date_str}_{time_str}_{safe_keyword}_{safe_title}.md"

    filepath = INTAKE_DIR / category / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)

    content = f"""# {item.get('title', '未知标题')}

> 关键词：{keyword}
> 类别：{category}
> 来源：{item.get('source', '未知')}
> 发现时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
> 链接：{item.get('url', '无')}

---

## 内容摘要

{item.get('summary', '待补充')}

## 分析

| 维度 | 数值 |
|------|------|
| 价值评分 | {analysis.get('score', 0)} |
| 标签 | {', '.join(analysis.get('tags', []))} |

## 相关关键词

- {keyword}

## 下一步

- [ ] 人工审核内容价值
- [ ] 判断是否入知识库
- [ ] 如有需要，创建对应术语词条

---

*由主动学习系统自动创建*
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath


def run_keyword_search(tracking: Dict) -> List[Dict]:
    """运行关键词搜索"""
    print("\n🔍 主动搜索关键词...")

    new_findings = []
    now = datetime.now()

    for category, keywords in TRACK_KEYWORDS.items():
        for keyword in keywords:
            # 检查是否需要搜索（每24小时最多一次）
            last_searched = tracking.get("keywords_last_searched", {}).get(keyword)
            should_search = True

            if last_searched:
                last_time = datetime.fromisoformat(last_searched)
                hours_since = (now - last_time).total_seconds() / 3600
                if hours_since < 24:
                    should_search = False
                    print(f"   ⏭️ 跳过 {keyword}（{hours_since:.1f}小时前搜索过）")

            if should_search:
                print(f"   📡 搜索: {keyword}")

                # 执行搜索
                results = search_news(keyword)

                if results:
                    # 分析并保存
                    for item in results:
                        analysis = analyze_content(item['title'], '', keyword)
                        if analysis['is_valuable']:
                            filepath = save_finding(category, keyword, item, analysis)
                            print(f"      ✅ 保存: {item['title'][:40]}...")
                            new_findings.append({
                                "category": category,
                                "keyword": keyword,
                                "item": item,
                                "filepath": str(filepath)
                            })
                            tracking["articles_collected"] = tracking.get("articles_collected", 0) + 1

                # 更新搜索时间
                if "keywords_last_searched" not in tracking:
                    tracking["keywords_last_searched"] = {}
                tracking["keywords_last_searched"][keyword] = now.isoformat()

    return new_findings


def run_trend_discovery(tracking: Dict) -> List[Dict]:
    """发现行业趋势"""
    print("\n📈 趋势发现...")

    trends = []

    # 检测最近的知识库更新
    # 如果某个领域最近更新少，可能是知识缺口

    return trends


def generate_daily_report(findings: List[Dict]) -> Path:
    """生成每日学习报告"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    filepath = INTAKE_DIR / f"学习报告_{date_str}.md"

    # 按类别分组
    by_category = {}
    for f in findings:
        cat = f.get('category', '未知')
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(f)

    content = f"""# 主动学习日报

> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
> 本次发现：{len(findings)} 条

---

## 概览

| 类别 | 数量 |
|------|------|
"""

    for cat, items in by_category.items():
        content += f"| {cat} | {len(items)} |\n"

    content += "\n---\n\n## 详细内容\n\n"

    for cat, items in by_category.items():
        content += f"### {cat}\n\n"
        for item in items:
            title = item.get('item', {}).get('title', '未知')[:60]
            url = item.get('item', {}).get('url', '')
            keyword = item.get('keyword', '')
            content += f"- **{title}**\n"
            content += f"  - 关键词: {keyword}\n"
            if url:
                content += f"  - [链接]({url})\n"
            content += f"  - 文件: `{item.get('filepath', '')}`\n\n"

    content += """---

## 下一步行动

1. [ ] 审核今日发现的内容
2. [ ] 判断是否入知识库
3. [ ] 如有新术语，更新术语词典
4. [ ] 如有重要发现，通知相关角色

---

*由主动学习系统自动生成*
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath


def run_learning():
    """运行主动学习"""
    start_time = time.time()
    findings = []

    try:
        print(f"🚀 开始主动学习...")
        print(f"   摄入目录: {INTAKE_DIR}")
        print(f"   追踪关键词: {sum(len(v) for v in TRACK_KEYWORDS.values())} 个")

        # 确保目录存在
        INTAKE_DIR.mkdir(parents=True, exist_ok=True)

        # 加载追踪数据
        tracking = get_tracking_data()
        last_run = tracking.get("last_run", "从未")
        print(f"   上次运行: {last_run[:10] if last_run and len(last_run) > 10 else last_run}")

        # 1. 关键词搜索
        findings = run_keyword_search(tracking)

        # 2. 趋势发现
        trends = run_trend_discovery(tracking)
        findings.extend(trends)

        # 保存追踪数据
        save_tracking_data(tracking)

        # 3. 生成报告
        if findings:
            report_path = generate_daily_report(findings)
            print(f"\n📊 学习报告: {report_path.name}")

        # 触发知识自动晋升
        try:
            from pathlib import Path
            import subprocess
            promoter_script = Path(__file__).parent / "knowledge-auto-promoter.py"
            if promoter_script.exists():
                result = subprocess.run(
                    ["python3", str(promoter_script)],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                if result.returncode == 0:
                    print("  ✅ 知识自动晋升完成")
                else:
                    print(f"  ⚠️ 晋升过程有警告: {result.stderr[:100]}")
        except Exception as e:
            print(f"  ⚠️ 无法触发知识晋升: {e}")

        print(f"\n✅ 主动学习完成")
        print(f"   本次发现: {len(findings)} 条")
        print(f"   累计发现: {tracking.get('articles_collected', 0)} 条")
        print(f"   报告目录: {INTAKE_DIR}")

        # Write status on success
        duration = int(time.time() - start_time)
        if write_task_status:
            write_task_status("proactive", "success", duration, None, len(findings))

        return findings

    except Exception as e:
        duration = int(time.time() - start_time)
        if write_task_status:
            write_task_status("proactive", "fail", duration, str(e), len(findings))
        raise


if __name__ == "__main__":
    run_learning()
