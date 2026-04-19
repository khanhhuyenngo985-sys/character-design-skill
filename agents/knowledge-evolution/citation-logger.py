#!/usr/bin/env python3
"""
知识库引用日志记录器
记录 Agent 的知识库引用行为，用于审计和分析
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

LOG_DIR = Path("/tmp/knowledge-evolution")
CITATION_LOG = LOG_DIR / "citation-log.jsonl"
KNOWLEDGE_USAGE_LOG = LOG_DIR / "knowledge-usage.jsonl"
KB_ROOT = Path("/Users/baimengke/Documents/白梦客知识库")


def log_citation(
    agent: str,
    scene: str,
    citation: List[str],
    kb_content_found: bool,
    status: str,
    notes: Optional[str] = None
) -> Dict:
    """
    记录一次引用行为

    Args:
        agent: Agent 名称（如 director, screenwriter）
        scene: 场景类型（simple/complex）
        citation: 引用的文件路径列表
        kb_content_found: 知识库是否找到相关内容
        status: 状态（valid/no_citation/invalid_files/missing_specific/no_kb_content）
        notes: 额外备注

    Returns:
        记录的日志条目
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent,
        "scene": scene,
        "citation": citation,
        "kb_content_found": kb_content_found,
        "status": status,
    }

    if notes:
        log_entry["notes"] = notes

    with open(CITATION_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    return log_entry


def validate_files(cited_files: List[str]) -> Dict:
    """
    验证引用的文件是否存在

    Args:
        cited_files: 引用的文件路径列表

    Returns:
        验证结果 {"valid": bool, "invalid_files": list}
    """
    invalid = []
    for f in cited_files:
        path = Path(f).expanduser()
        if not path.exists():
            invalid.append(f)

    return {"valid": len(invalid) == 0, "invalid_files": invalid}


def extract_citation_block(response: str) -> Optional[str]:
    """
    从响应中提取引用声明块

    Args:
        response: Agent 响应文本

    Returns:
        引用声明块内容，或 None
    """
    markers = ["已引用知识库", "⚠️ 未引用知识库"]
    for marker in markers:
        if marker in response:
            # 找到标记后，提取到下一个空行或分段
            lines = response.split("\n")
            block_lines = []
            in_block = False
            for line in lines:
                if marker in line:
                    in_block = True
                if in_block:
                    block_lines.append(line)
                    if line.strip() == "" and len(block_lines) > 1:
                        break
            return "\n".join(block_lines)
    return None


def extract_cited_files(citation_block: str) -> List[str]:
    """
    从引用声明块中提取文件路径

    Args:
        citation_block: 引用声明块

    Returns:
        文件路径列表
    """
    import re
    # 匹配常见路径格式
    pattern = r'/[\w\-/]+(?:\.\w+)+'
    return re.findall(pattern, citation_block)


def check_response(response: str) -> Dict:
    """
    检查响应是否包含正确的引用声明

    Args:
        response: Agent 响应文本

    Returns:
        检查结果
    """
    citation_block = extract_citation_block(response)

    if not citation_block:
        return {
            "has_citation": False,
            "citation_block": None,
            "status": "no_citation",
            "cited_files": []
        }

    cited_files = extract_cited_files(citation_block)
    validation = validate_files(cited_files)

    return {
        "has_citation": True,
        "citation_block": citation_block,
        "status": "valid" if validation["valid"] else "invalid_files",
        "cited_files": cited_files,
        "invalid_files": validation.get("invalid_files", [])
    }


def get_citation_stats(agent: Optional[str] = None, days: int = 7) -> Dict:
    """
    获取引用统计数据

    Args:
        agent: 可选，按 Agent 过滤
        days: 统计天数

    Returns:
        统计数据
    """
    if not CITATION_LOG.exists():
        return {"total": 0, "by_agent": {}, "by_status": {}}

    cutoff = datetime.now().timestamp() - (days * 86400)
    stats = {
        "total": 0,
        "by_agent": {},
        "by_status": {},
        "citation_rate": 0.0,
        "valid_rate": 0.0
    }

    valid_count = 0

    with open(CITATION_LOG, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                timestamp = datetime.fromisoformat(entry["timestamp"]).timestamp()
                if timestamp < cutoff:
                    continue

                stats["total"] += 1

                agent_name = entry.get("agent", "unknown")
                status = entry.get("status", "unknown")

                stats["by_agent"][agent_name] = stats["by_agent"].get(agent_name, 0) + 1
                stats["by_status"][status] = stats["by_status"].get(status, 0) + 1

                if status == "valid":
                    valid_count += 1

            except (json.JSONDecodeError, KeyError):
                continue

    if stats["total"] > 0:
        stats["citation_rate"] = round(
            stats["by_agent"].get(agent, stats["total"]) / stats["total"], 2
        )
        stats["valid_rate"] = round(valid_count / stats["total"], 2)

    return stats


def log_knowledge_usage(
    agent: str,
    cited_files: List[str],
    project: Optional[str] = None
) -> Dict:
    """
    记录知识使用情况
    追踪哪些晋升的知识被实际使用

    Args:
        agent: Agent 名称
        cited_files: 引用的文件路径列表
        project: 项目名称（可选）

    Returns:
        使用记录
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # 检查哪些引用来自 auto-promoted 目录
    auto_promoted_files = []
    for f in cited_files:
        path = Path(f).expanduser()
        # 检查是否在 auto-promoted 目录
        if "auto-promoted" in str(path) or "intake" in str(path):
            auto_promoted_files.append(f)

    if not auto_promoted_files:
        return {"usage_recorded": False}

    # 提取知识 ID（文件名）
    knowledge_items = []
    for f in auto_promoted_files:
        path = Path(f)
        knowledge_items.append({
            "filename": path.name,
            "path": str(path),
            "category": _infer_category(str(path))
        })

    usage_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent,
        "knowledge_used": knowledge_items,
        "project": project,
        "count": len(knowledge_items)
    }

    with open(KNOWLEDGE_USAGE_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(usage_entry, ensure_ascii=False) + "\n")

    return {"usage_recorded": True, "knowledge_items": knowledge_items}


def _infer_category(path: str) -> str:
    """推断知识类别"""
    if "提示词" in path or "prompt" in path.lower():
        return "prompt"
    elif "竞品" in path or "competitor" in path.lower():
        return "competitor"
    elif "洞察" in path or "insight" in path.lower():
        return "insight"
    elif "导演" in path or "director" in path.lower():
        return "director"
    else:
        return "other"


def get_knowledge_usage_stats(days: int = 30) -> Dict:
    """
    获取知识使用统计

    Args:
        days: 统计天数

    Returns:
        使用统计
    """
    if not KNOWLEDGE_USAGE_LOG.exists():
        return {"total_usage": 0, "by_category": {}, "by_agent": {}, "top_knowledge": []}

    cutoff = datetime.now() - timedelta(days=days)
    stats = {
        "total_usage": 0,
        "by_category": {},
        "by_agent": {},
        "top_knowledge": [],
        "usage_count": {}  # 每条知识被使用的次数
    }

    try:
        with open(KNOWLEDGE_USAGE_LOG, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    timestamp = datetime.fromisoformat(entry["timestamp"])
                    if timestamp < cutoff:
                        continue

                    stats["total_usage"] += entry.get("count", 0)

                    agent = entry.get("agent", "unknown")
                    stats["by_agent"][agent] = stats["by_agent"].get(agent, 0) + 1

                    for item in entry.get("knowledge_used", []):
                        category = item.get("category", "other")
                        stats["by_category"][category] = stats["by_category"].get(category, 0) + 1

                        # 统计每条知识的使用次数
                        filename = item.get("filename", "")
                        if filename:
                            stats["usage_count"][filename] = stats["usage_count"].get(filename, 0) + 1

                except (json.JSONDecodeError, KeyError, ValueError):
                    continue

        # 计算 top knowledge
        top = sorted(stats["usage_count"].items(), key=lambda x: x[1], reverse=True)[:10]
        stats["top_knowledge"] = [{"filename": k, "count": v} for k, v in top]

    except Exception as e:
        print(f"⚠️ 读取使用日志失败: {e}")

    return stats


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="知识库引用日志记录器")
    parser.add_argument("--agent", default="unknown", help="Agent 名称")
    parser.add_argument("--scene", default="simple", choices=["simple", "complex"], help="场景类型")
    parser.add_argument("--citation", nargs="*", default=[], help="引用的文件路径")
    parser.add_argument("--kb-found", action="store_true", help="知识库是否找到内容")
    parser.add_argument("--status", default="valid", help="状态")
    parser.add_argument("--notes", help="额外备注")
    parser.add_argument("--stats", action="store_true", help="显示引用统计信息")
    parser.add_argument("--check", help="检查响应是否包含引用声明")
    parser.add_argument("--usage", action="store_true", help="显示知识使用统计")
    parser.add_argument("--project", help="项目名称（用于知识使用追踪）")

    args = parser.parse_args()

    if args.check:
        result = check_response(args.check)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.stats:
        stats = get_citation_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    elif args.usage:
        stats = get_knowledge_usage_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        entry = log_citation(
            agent=args.agent,
            scene=args.scene,
            citation=args.citation,
            kb_content_found=args.kb_found,
            status=args.status,
            notes=args.notes
        )
        print(f"✅ 引用日志已记录: {entry['timestamp']}")

        # 同时记录知识使用情况
        if args.citation:
            usage = log_knowledge_usage(
                agent=args.agent,
                cited_files=args.citation,
                project=args.project
            )
            if usage.get("usage_recorded"):
                print(f"✅ 知识使用已记录: {len(usage.get('knowledge_items', []))} 条")


if __name__ == "__main__":
    main()
