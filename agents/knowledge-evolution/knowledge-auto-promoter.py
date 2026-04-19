#!/usr/bin/env python3
"""
知识库自动晋升系统
自动评估intake内容，晋升高质量内容到核心知识库
"""

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

# 知识库根目录
KB_ROOT = Path("/Users/baimengke/Documents/白梦客知识库")
INTAKE_DIR = KB_ROOT / "intake"
AUTO_PROMOTED_DIRS = {
    "prompt": KB_ROOT / "04-行业知识/AI视频提示词库/auto-promoted",
    "competitor": KB_ROOT / "04-行业知识/竞品广告库/auto-promoted",
    "insight": KB_ROOT / "04-行业知识/行业洞察/auto-promoted",
    "director": KB_ROOT / "01-导演组/行业动态/auto-promoted",
}
ARCHIVE_DIR = INTAKE_DIR / "archive"
LOG_DIR = Path("/tmp/knowledge-evolution")
PROMOTION_LOG = LOG_DIR / "promotion-log.jsonl"

# 评分权重
WEIGHTS = {
    "relatedness": 0.3,    # 相关度
    "credibility": 0.2,   # 可信度
    "timeliness": 0.2,    # 时效性
    "knowledge_value": 0.3  # 知识价值
}

# 晋升阈值
THRESHOLD_PROMOTE = 7.0   # ≥7.0 自动晋升
THRESHOLD_WATCH = 5.0     # 5.0-7.0 待观察
THRESHOLD_REJECT = 5.0    # <5.0 丢弃


def init():
    """初始化，创建必要目录"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    for d in AUTO_PROMOTED_DIRS.values():
        d.mkdir(parents=True, exist_ok=True)


def load_promotion_log() -> Set[str]:
    """加载已晋升内容的hash集合，用于去重"""
    promoted_hashes: Set[str] = set()
    if not PROMOTION_LOG.exists():
        return promoted_hashes

    try:
        with open(PROMOTION_LOG, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    if "hash" in entry:
                        promoted_hashes.add(entry["hash"])
                except json.JSONDecodeError:
                    continue
    except Exception:
        pass

    return promoted_hashes


def scan_intake() -> List[Dict]:
    """扫描intake目录，返回待处理内容列表"""
    intake_dirs = [
        INTAKE_DIR / "媒体监控",
        INTAKE_DIR / "主动学习",
    ]

    # 加载已晋升的内容hash
    promoted_hashes = load_promotion_log()
    print(f"  📋 已晋升记录: {len(promoted_hashes)} 条")

    contents = []
    seen_hashes: Set[str] = set()

    for intake_dir in intake_dirs:
        if not intake_dir.exists():
            print(f"  ℹ️ 目录不存在: {intake_dir}")
            continue

        for md_file in intake_dir.glob("*.md"):
            # 跳过追踪文件
            if md_file.name.startswith("."):
                continue

            # 读取内容
            content = md_file.read_text(encoding="utf-8")

            # 简单解析（标题、首行、内容）
            lines = content.strip().split("\n")
            title = lines[0].lstrip("# ").strip() if lines else md_file.stem

            # 生成内容hash用于去重
            content_hash = hashlib.md5(content.encode()).hexdigest()[:12]

            # 跳过已晋升的内容（幂等性保证）
            if content_hash in promoted_hashes:
                continue

            if content_hash in seen_hashes:
                continue
            seen_hashes.add(content_hash)

            # 判断来源类型
            source = "unknown"
            if "媒体监控" in str(intake_dir):
                source = "media"
            elif "主动学习" in str(intake_dir):
                source = "proactive"

            # 提取日期（文件名格式：YYYY-MM-DD_标题.md）
            date_match = re.match(r"(\d{4}-\d{2}-\d{2})", md_file.stem)
            date = date_match.group(1) if date_match else datetime.now().strftime("%Y-%m-%d")

            contents.append({
                "title": title,
                "content": content,
                "path": str(md_file),
                "source": source,
                "date": date,
                "hash": content_hash
            })

    return contents


def _score_relatedness(content: Dict) -> float:
    """相关度评分：内容与AI视频/广告创作的相关程度"""
    text = (content.get("title", "") + " " + content.get("content", "")).lower()

    # 关键词匹配
    high_relevance = ["ai广告", "aigc广告", "虚拟广告", "ai视频", "sora", "midjourney",
                      "vidu", "即梦", "seedance", "虚拟拍摄", "ai生成视频", "gen3"]
    medium_relevance = ["广告创意", "影视制作", "营销策略", "分镜", "脚本", "视觉设计"]
    low_relevance = ["创意方法", "商业趋势", "技术新闻", "行业报告"]
    irrelevant = ["政治", "娱乐八卦", "体育", "美食"]

    # 检查无关关键词
    for kw in irrelevant:
        if kw in text:
            return 0.0

    # 检查高相关关键词
    for kw in high_relevance:
        if kw in text:
            return 10.0

    # 检查中相关关键词
    for kw in medium_relevance:
        if kw in text:
            return 5.0

    # 检查低相关关键词
    for kw in low_relevance:
        if kw in text:
            return 3.0

    return 3.0  # 默认低相关


def _score_credibility(content: Dict) -> float:
    """可信度评分：来源的权威性"""
    text = (content.get("title", "") + " " + content.get("content", "")).lower()

    # 高权威来源
    high_authority = ["广告门", "socialbeta", "数英网", "36kr", "虎嗅"]
    medium_authority = ["公众号", "微博", "知乎"]
    low_authority = ["未知来源", "匿名"]

    for kw in high_authority:
        if kw in text:
            return 10.0

    for kw in medium_authority:
        if kw in text:
            return 5.0

    for kw in low_authority:
        if kw in text:
            return 2.0

    return 5.0  # 默认中等


def _score_timeliness(content: Dict) -> float:
    """时效性评分：内容的新鲜程度"""
    date_str = content.get("date", "")

    if not date_str:
        return 5.0  # 无法判断，默认中等

    try:
        content_date = datetime.strptime(date_str, "%Y-%m-%d")
        days_ago = (datetime.now() - content_date).days

        if days_ago <= 1:
            return 10.0  # 24小时内
        elif days_ago <= 7:
            return 8.0   # 7天内
        elif days_ago <= 30:
            return 5.0   # 30天内
        elif days_ago <= 90:
            return 3.0   # 90天内
        else:
            return 0.0   # 更早
    except:
        return 5.0  # 解析失败，默认中等


def _score_knowledge_value(content: Dict) -> float:
    """知识价值评分：内容对团队的启发价值"""
    text = (content.get("title", "") + " " + content.get("content", "")).lower()

    # 高启发价值关键词
    high_value = ["提示词", "prompt", "技法", "教程", "案例", "公式", "方法"]
    medium_value = ["分析", "趋势", "观点", "视角"]
    low_value = ["新闻", "资讯", "动态"]

    # 检查高启发
    for kw in high_value:
        if kw in text:
            return 10.0

    for kw in medium_value:
        if kw in text:
            return 5.0

    for kw in low_value:
        if kw in text:
            return 3.0

    return 5.0  # 默认中等


def score_content(content: Dict) -> Dict:
    """计算四维度综合评分"""
    relatedness = _score_relatedness(content)
    credibility = _score_credibility(content)
    timeliness = _score_timeliness(content)
    knowledge_value = _score_knowledge_value(content)

    total = (relatedness * WEIGHTS["relatedness"] +
             credibility * WEIGHTS["credibility"] +
             timeliness * WEIGHTS["timeliness"] +
             knowledge_value * WEIGHTS["knowledge_value"])

    return {
        "relatedness": relatedness,
        "credibility": credibility,
        "timeliness": timeliness,
        "knowledge_value": knowledge_value,
        "total": round(total, 1)
    }


def check_stop_signals(content: Dict, score: float) -> Dict:
    """检查停止信号"""
    signals = {
        "stop": False,
        "reasons": []
    }

    text = (content.get("title", "") + " " + content.get("content", "")).lower()

    # 1. 内容重复检测（简单关键词匹配）
    duplicate_keywords = ["同样的", "重复", "抄袭", "一模一样"]
    for kw in duplicate_keywords:
        if kw in text:
            signals["stop"] = True
            signals["reasons"].append("contentDuplication")

    # 2. 质量回归检测（新内容明显低于已有）
    if score < 3.0:
        signals["stop"] = True
        signals["reasons"].append("qualityRegression")

    # 3. 内容过时检测
    timeliness = _score_timeliness(content)
    if timeliness < 3.0:
        signals["stop"] = True
        signals["reasons"].append("contentOutdated")

    # 4. 噪音检测（标题党、无实质内容）
    if len(content.get("content", "")) < 50 and score < 5.0:
        signals["stop"] = True
        signals["reasons"].append("noiseRatioTooHigh")

    return signals


def extract_learnable_signals(content: Dict) -> Dict:
    """提取可学习信号"""
    text = content.get("content", "")
    title = content.get("title", "")

    # 判断信号类型
    signal_type = "insight"
    if any(kw in text.lower() for kw in ["提示词", "prompt", "关键词"]):
        signal_type = "prompt-pattern"
    elif any(kw in text.lower() for kw in ["技法", "方法", "技巧"]):
        signal_type = "technique"
    elif any(kw in text.lower() for kw in ["案例", "示例"]):
        signal_type = "case-study"

    # 简单关键词提取（实际可用NLP，这里用规则）
    key_phrases = []
    if len(text) > 100:
        # 取内容前200字作为核心内容
        core_content = text[:200]
        key_phrases.append(core_content.replace("\n", " ").strip())

    return {
        "type": signal_type,
        "content": key_phrases[0] if key_phrases else title,
        "applicable_scene": "AI视频广告创作",
        "confidence": "medium"
    }


def route_content(content: Dict) -> str:
    """路由决策，返回目标目录类型"""
    text = (content.get("title", "") + " " + content.get("content", "")).lower()

    # 竞品广告：含品牌名+广告内容
    brand_keywords = ["完美日记", "花西子", "元气森林", "小米", "华为", "苹果", "nike", "adidas"]
    ad_keywords = ["广告", "营销", "campaign"]

    has_brand = any(kw in text for kw in brand_keywords)
    has_ad = any(kw in text for kw in ad_keywords)

    if has_brand and has_ad:
        return "competitor"

    # 提示词/工具：含AI工具名
    tool_keywords = ["midjourney", "sora", "即梦", "vidu", "seedance", "runway",
                     "提示词", "prompt", "生成", "ai视频"]
    if any(kw in text for kw in tool_keywords):
        return "prompt"

    # 行业洞察：广告/影视行业分析
    insight_keywords = ["行业", "洞察", "分析", "趋势", "市场", "报告"]
    if any(kw in text for kw in insight_keywords):
        return "insight"

    # 导演相关：分镜、镜头、叙事
    director_keywords = ["分镜", "镜头", "叙事", "导演", "拍摄"]
    if any(kw in text for kw in director_keywords):
        return "director"

    # 默认：行业洞察
    return "insight"


def promote_to_knowledge_base(content: Dict, target_dir: str, scores: Dict, signals: Dict):
    """晋升内容到核心知识库"""

    # 确定目标目录
    dir_map = {
        "prompt": AUTO_PROMOTED_DIRS["prompt"],
        "competitor": AUTO_PROMOTED_DIRS["competitor"],
        "insight": AUTO_PROMOTED_DIRS["insight"],
        "director": AUTO_PROMOTED_DIRS["director"],
    }

    target_path = dir_map.get(target_dir, AUTO_PROMOTED_DIRS["insight"])

    # 生成文件名
    date_str = content.get("date", datetime.now().strftime("%Y-%m-%d"))
    safe_title = re.sub(r'[^\w\s\u4e00-\u9fff]', '', content.get("title", "untitled"))[:30]
    filename = f"{date_str}_{safe_title}.md"
    filepath = target_path / filename

    # 避免重名
    counter = 1
    while filepath.exists():
        filepath = target_path / f"{date_str}_{safe_title}_{counter}.md"
        counter += 1

    # 构建晋升内容
    promoted_content = f"""---
来源: {content.get('source', 'unknown')}
原始链接: {content.get('url', 'N/A')}
类型: {target_dir}
综合评分: {scores['total']}
相关度: {scores['relatedness']} | 可信度: {scores['credibility']} | 时效性: {scores['timeliness']} | 知识价值: {scores['knowledge_value']}
PairwiseJudge结果: 待评估
自动晋升日期: {datetime.now().strftime('%Y-%m-%d')}
晋升原因: 综合评分{scores['total']} >= {THRESHOLD_PROMOTE}
---

# {content.get('title', '无标题')}

## 摘要
{content.get('content', '')[:200]}

## 核心内容
{content.get('content', '')}

## 对白梦客的启发
待填写

## 可学习信号 (Learnable Signals)
- **类型**: {signals.get('type', 'insight')}
- **内容**: {signals.get('content', 'N/A')}
- **适用场景**: {signals.get('applicable_scene', 'AI视频广告创作')}
- **置信度**: {signals.get('confidence', 'medium')}

## 相关标签
#AI视频 #广告创作 #自动晋升

---

*本条目由知识自动晋升系统生成*
*晋升路由: {target_dir}*
"""

    # 写入文件
    filepath.write_text(promoted_content, encoding="utf-8")
    print(f"  ✅ 晋升到: {filepath.relative_to(KB_ROOT)}")

    # 记录日志
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "title": content.get("title"),
        "source": content.get("source"),
        "route": target_dir,
        "score": scores["total"],
        "filepath": str(filepath),
        "hash": content.get("hash", "")
    }
    with open(PROMOTION_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    return str(filepath)


def archive_replaced_content(old_content: Dict, new_content: Dict, reason: str):
    """归档被替换的内容"""

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    # 生成归档文件名
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_title = re.sub(r'[^\w\s\u4e00-\u9fff]', '', old_content.get("title", "untitled"))[:20]
    filename = f"{date_str}_ARCHIVED_{safe_title}.md"
    filepath = ARCHIVE_DIR / filename

    # 构建归档内容
    archive_content = f"""---
归档日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
被替换原因: {reason}
替换标题: {new_content.get('title', 'N/A')}
---

# {old_content.get('title', '无标题')}

{old_content.get('content', '')}
"""

    filepath.write_text(archive_content, encoding="utf-8")
    print(f"  📦 归档: {filepath.name}")


def pairwise_judge(new_content: Dict, existing_contents: List[Dict]) -> Dict:
    """
    两两对比判断新内容是否优于已有内容
    简化版本：直接对比分数，不做深度内容对比
    """

    if not existing_contents:
        return {
            "verdict": "no_existing",
            "winner": "new",
            "confidence": "high",
            "reason": "无已有内容，直接晋升"
        }

    new_score = score_content(new_content)["total"]

    # 找出最高分的已有内容
    best_existing = max(existing_contents, key=lambda x: score_content(x)["total"])
    best_score = score_content(best_existing)["total"]

    # 判断
    score_diff = new_score - best_score

    if score_diff > 1.0:
        # 新内容明显优于已有
        return {
            "verdict": "new_better",
            "winner": "new",
            "confidence": "high" if score_diff > 2.0 else "medium",
            "reason": f"新内容({new_score})优于已有({best_score})",
            "replaced_content": best_existing
        }
    elif score_diff < -1.0:
        # 新内容劣于已有
        return {
            "verdict": "existing_better",
            "winner": "existing",
            "confidence": "high" if abs(score_diff) > 2.0 else "medium",
            "reason": f"新内容({new_score})劣于已有({best_score})"
        }
    else:
        # 相近，进入待观察
        return {
            "verdict": "similar",
            "winner": "none",
            "confidence": "low",
            "reason": f"内容相近：新{new_score} vs 已{best_score}"
        }


def run():
    """主运行函数"""
    init()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 知识自动晋升开始...")

    # 1. 扫描intake
    contents = scan_intake()
    print(f"  📥 发现 {len(contents)} 条待处理内容")

    if not contents:
        print("  ℹ️ 无待处理内容")
        return

    # 2. 遍历处理每条内容
    promoted_count = 0
    rejected_count = 0
    watch_count = 0

    for content in contents:
        print(f"\n  处理: {content.get('title', '无标题')[:50]}")

        # 计算评分
        scores = score_content(content)
        print(f"    评分: {scores['total']} (相关{scores['relatedness']}|可信{scores['credibility']}|时效{scores['timeliness']}|价值{scores['knowledge_value']})")

        # 检查停止信号
        signals = check_stop_signals(content, scores['total'])
        if signals['stop']:
            print(f"    🛑 停止: {', '.join(signals['reasons'])}")
            rejected_count += 1
            continue

        # 低于阈值直接拒绝
        if scores['total'] < THRESHOLD_REJECT:
            print(f"    ❌ 拒绝: 评分{scores['total']} < {THRESHOLD_REJECT}")
            rejected_count += 1
            continue

        # 5.0-7.0 进入待观察
        if scores['total'] < THRESHOLD_PROMOTE:
            print(f"    ⏳ 待观察: 评分{scores['total']} 在 {THRESHOLD_WATCH}-{THRESHOLD_PROMOTE} 之间")
            watch_count += 1
            continue

        # ≥7.0 晋升
        print(f"    ✅ 达到晋升阈值 {THRESHOLD_PROMOTE}")

        # 路由决策
        route = route_content(content)
        print(f"    📍 路由: {route}")

        # 提取可学习信号
        learnable_signals = extract_learnable_signals(content)

        # 晋升
        promote_to_knowledge_base(content, route, scores, learnable_signals)
        promoted_count += 1

    # 3. 输出总结
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 知识自动晋升完成")
    print(f"  ✅ 晋升: {promoted_count} 条")
    print(f"  ⏳ 待观察: {watch_count} 条")
    print(f"  ❌ 拒绝: {rejected_count} 条")


if __name__ == "__main__":
    run()
