#!/usr/bin/env python3
"""
知识库引用审计脚本
检查 Agent 的引用合规性，生成审计报告
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

LOG_DIR = Path("/tmp/knowledge-evolution")
CITATION_LOG = LOG_DIR / "citation-log.jsonl"
AGENTS_DIR = Path("/Users/baimengke/.claude/agents")

# 合规阈值
CITATION_RATE_THRESHOLD = 0.7  # 70% 引用率
VALID_RATE_THRESHOLD = 0.8    # 80% 有效引用率


def load_citation_logs(days: int = 7) -> List[Dict]:
    """加载引用日志"""
    if not CITATION_LOG.exists():
        return []

    cutoff = datetime.now() - timedelta(days=days)
    logs = []

    try:
        with open(CITATION_LOG, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    timestamp = datetime.fromisoformat(entry["timestamp"])
                    if timestamp >= cutoff:
                        logs.append(entry)
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue
    except Exception as e:
        print(f"⚠️ 读取日志失败: {e}")

    return logs


def get_agents_with_citation_requirement() -> List[str]:
    """获取需要引用检查的 Agent 列表"""
    # 从 agent 文件中提取有知识库调用章节的 agent
    agents = []

    citation_agents = [
        "director.md",
        "screenwriter.md",
        "creative-director.md",
        "cinematographer.md",
        "editor.md",
        "colorist.md",
        "vfx-supervisor.md",
        "sound-designer.md",
        "production-manager.md",
    ]

    for agent_file in citation_agents:
        agent_path = AGENTS_DIR / agent_file
        if agent_path.exists():
            content = agent_path.read_text(encoding="utf-8")
            if "已引用知识库" in content or "未引用知识库" in content:
                agents.append(agent_file.replace(".md", ""))

    return agents


def calculate_agent_stats(logs: List[Dict]) -> Dict:
    """计算各 Agent 的引用统计"""
    stats = defaultdict(lambda: {
        "total": 0,
        "cited": 0,
        "valid": 0,
        "invalid": 0,
        "no_citation": 0,
        "by_scene": defaultdict(lambda: {"total": 0, "cited": 0})
    })

    for log in logs:
        agent = log.get("agent", "unknown")
        status = log.get("status", "unknown")

        stats[agent]["total"] += 1

        if status == "valid":
            stats[agent]["cited"] += 1
            stats[agent]["valid"] += 1
        elif status == "invalid_files":
            stats[agent]["cited"] += 1
            stats[agent]["invalid"] += 1
        elif status == "no_citation":
            stats[agent]["no_citation"] += 1

        # 按场景统计
        scene = log.get("scene", "unknown")
        stats[agent]["by_scene"][scene]["total"] += 1
        if status in ("valid", "invalid_files"):
            stats[agent]["by_scene"][scene]["cited"] += 1

    return dict(stats)


def generate_audit_report(logs: List[Dict], stats: Dict) -> str:
    """生成审计报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    report_lines = [
        f"# 知识库引用审计报告",
        f"",
        f"> 生成时间：{now}",
        f"> 审计范围：最近7天",
        f"> 日志条目：{len(logs)} 条",
        f"",
        f"---",
        f"",
    ]

    # 总体统计
    total_logs = len(logs)
    total_cited = sum(s["cited"] for s in stats.values())
    total_valid = sum(s["valid"] for s in stats.values())
    total_no_citation = sum(s["no_citation"] for s in stats.values())

    overall_citation_rate = total_cited / total_logs if total_logs > 0 else 0
    overall_valid_rate = total_valid / total_cited if total_cited > 0 else 0

    report_lines.extend([
        f"## 总体统计",
        f"",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 总对话数 | {total_logs} |",
        f"| 有引用 | {total_cited} |",
        f"| 有效引用 | {total_valid} |",
        f"| 无引用 | {total_no_citation} |",
        f"| 引用率 | {overall_citation_rate:.1%} |",
        f"| 有效率 | {overall_valid_rate:.1%} |",
        f"",
    ])

    # Agent 排名
    report_lines.extend([
        f"## Agent 引用排行",
        f"",
        f"| Agent | 对话数 | 引用数 | 引用率 | 有效率 | 合规状态 |",
        f"|-------|--------|--------|--------|--------|----------|",
    ])

    compliant_agents = []
    non_compliant_agents = []

    for agent, s in sorted(stats.items(), key=lambda x: x[1]["cited"] / max(x[1]["total"], 1), reverse=True):
        citation_rate = s["cited"] / max(s["total"], 1)
        valid_rate = s["valid"] / max(s["cited"], 1)

        is_compliant = citation_rate >= CITATION_RATE_THRESHOLD and valid_rate >= VALID_RATE_THRESHOLD
        status = "✅ 合规" if is_compliant else "❌ 不合规"

        if is_compliant:
            compliant_agents.append(agent)
        else:
            non_compliant_agents.append(agent)

        report_lines.append(
            f"| {agent} | {s['total']} | {s['cited']} | {citation_rate:.1%} | {valid_rate:.1%} | {status} |"
        )

    report_lines.append("")

    # 不合规详情
    if non_compliant_agents:
        report_lines.extend([
            f"## 不合规详情",
            f"",
        ])

        for agent in non_compliant_agents:
            s = stats[agent]
            citation_rate = s["cited"] / max(s["total"], 1)
            valid_rate = s["valid"] / max(s["cited"], 1)

            report_lines.append(f"### {agent}")
            report_lines.append("")

            issues = []
            if citation_rate < CITATION_RATE_THRESHOLD:
                issues.append(f"引用率过低 ({citation_rate:.1%} < {CITATION_RATE_THRESHOLD:.1%})")
            if s["invalid"] > 0:
                issues.append(f"存在 {s['invalid']} 条无效引用（文件不存在）")

            report_lines.append(f"**问题：** {'; '.join(issues)}")
            report_lines.append("")
            report_lines.append(f"**建议：** 检查 {agent}.md 是否正确使用引用声明格式")
            report_lines.append("")

    # 合规建议
    if compliant_agents:
        report_lines.extend([
            f"## 合规建议",
            f"",
            f"以下 Agent 引用合规：{', '.join(compliant_agents)}",
            f"",
            f"持续监控，确保维持合规水平。",
            f"",
        ])

    report_lines.extend([
        f"---",
        f"",
        f"*本报告由 citation-audit.py 自动生成*",
    ])

    return "\n".join(report_lines)


def check_agent_citation_format(agent_name: str) -> Dict:
    """检查 Agent 文件是否包含正确的引用格式"""
    agent_path = AGENTS_DIR / f"{agent_name}.md"

    if not agent_path.exists():
        return {"exists": False, "has_format": False}

    content = agent_path.read_text(encoding="utf-8")

    has_citation_section = "已引用知识库" in content or "⚠️ 未引用知识库" in content
    has_citation_format = "已引用知识库：" in content

    return {
        "exists": True,
        "has_citation_section": has_citation_section,
        "has_citation_format": has_citation_format
    }


def main():
    """主函数"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 知识库引用审计开始...")

    # 加载日志
    logs = load_citation_logs(days=7)
    print(f"  加载 {len(logs)} 条日志")

    if not logs:
        print("  ⚠️ 无日志数据，请确认 Agent 已使用引用声明")
        print("  检查 Agent 文件格式...")
        agents = get_agents_with_citation_requirement()
        for agent in agents:
            format_check = check_agent_citation_format(agent)
            status = "✅" if format_check["has_citation_format"] else "❌"
            print(f"    {status} {agent}")
        return

    # 计算统计
    stats = calculate_agent_stats(logs)

    # 生成报告
    report = generate_audit_report(logs, stats)

    # 保存报告
    report_path = KB_ROOT / "00-总览" / "引用审计报告.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    print(f"  报告已生成: {report_path}")
    print(f"\n{report}")


if __name__ == "__main__":
    KB_ROOT = Path("/Users/baimengke/Documents/白梦客知识库")
    main()
