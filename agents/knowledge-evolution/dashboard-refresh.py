#!/usr/bin/env python3
"""
知识进化状态面板刷新脚本
每日运行，读取日志和状态，生成完整面板
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

KB_ROOT = Path("/Users/baimengke/Documents/白梦客知识库")
LOG_DIR = Path("/tmp/knowledge-evolution")
STATUS_FILE = LOG_DIR / "status.json"
PROMOTION_LOG = LOG_DIR / "promotion-log.jsonl"
INTAKE_DIR = KB_ROOT / "intake"
DASHBOARD_FILE = KB_ROOT / "00-总览" / "知识进化状态.md"

TASK_CONFIG = {
    "competitor": {"name": "竞品广告库更新", "icon": "🏪"},
    "media": {"name": "行业媒体监控", "icon": "📰"},
    "proactive": {"name": "主动学习", "icon": "🔍"},
    "scanner": {"name": "知识库健康扫描", "icon": "📊"},
    "promoter": {"name": "知识自动晋升", "icon": "🚀"},
}


def get_date_range() -> tuple:
    """获取今日、本周、本月的日期范围"""
    today = datetime.now()
    start_of_today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_week = start_of_today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return start_of_today, start_of_week, start_of_month


def load_status() -> dict:
    """加载状态文件"""
    if STATUS_FILE.exists():
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"tasks": {}, "today_stats": {}, "week_stats": {}}


def get_task_status_icon(status: str) -> str:
    """获取状态图标"""
    icons = {"success": "✅", "fail": "❌", "warn": "⚠️", "disabled": "⏸️"}
    return icons.get(status, "❓")


def format_duration(seconds: int) -> str:
    """格式化时长"""
    if seconds < 60:
        return f"{seconds}秒"
    elif seconds < 3600:
        return f"{seconds//60}分{seconds%60}秒"
    else:
        return f"{seconds//3600}小时{(seconds%3600)//60}分"


def get_time_ago(timestamp: str) -> str:
    """获取时间描述"""
    dt = datetime.fromisoformat(timestamp)
    delta = datetime.now() - dt

    if delta.total_seconds() < 3600:
        return f"{int(delta.total_seconds()//60)}分钟前"
    elif delta.total_seconds() < 86400:
        return f"{int(delta.total_seconds()//3600)}小时前"
    else:
        return f"{int(delta.days)}天前"


def count_intake_files(dir_path: Path, since: datetime) -> int:
    """统计目录中指定时间后的新文件数"""
    if not dir_path.exists():
        return 0

    count = 0
    for md_file in dir_path.glob("*.md"):
        if md_file.name.startswith("."):
            continue
        if md_file.stat().st_mtime > since.timestamp():
            count += 1
    return count


def get_intake_stats() -> Dict:
    """获取 intake 统计"""
    start_of_today, start_of_week, start_of_month = get_date_range()

    stats = {
        "media": {"today": 0, "week": 0, "month": 0},
        "proactive": {"today": 0, "week": 0, "month": 0},
    }

    media_dir = INTAKE_DIR / "媒体监控"
    proactive_dir = INTAKE_DIR / "主动学习"

    stats["media"]["today"] = count_intake_files(media_dir, start_of_today)
    stats["media"]["week"] = count_intake_files(media_dir, start_of_week)
    stats["media"]["month"] = count_intake_files(media_dir, start_of_month)

    stats["proactive"]["today"] = count_intake_files(proactive_dir, start_of_today)
    stats["proactive"]["week"] = count_intake_files(proactive_dir, start_of_week)
    stats["proactive"]["month"] = count_intake_files(proactive_dir, start_of_month)

    return stats


def get_promotion_stats() -> Dict:
    """获取晋升统计"""
    start_of_today, start_of_week, start_of_month = get_date_range()

    stats = {
        "today": {"total": 0, "routes": {}},
        "week": {"total": 0, "routes": {}},
        "month": {"total": 0, "routes": {}}
    }

    if not PROMOTION_LOG.exists():
        return stats

    with open(PROMOTION_LOG, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                dt = datetime.fromisoformat(entry["timestamp"])

                if dt >= start_of_today:
                    stats["today"]["total"] += 1
                    route = entry.get("route", "unknown")
                    stats["today"]["routes"][route] = stats["today"]["routes"].get(route, 0) + 1

                if dt >= start_of_week:
                    stats["week"]["total"] += 1
                    route = entry.get("route", "unknown")
                    stats["week"]["routes"][route] = stats["week"]["routes"].get(route, 0) + 1

                if dt >= start_of_month:
                    stats["month"]["total"] += 1
            except Exception:
                continue

    return stats


def get_recent_promotions(limit: int = 5) -> List[Dict]:
    """获取最近晋升记录"""
    promotions = []

    if not PROMOTION_LOG.exists():
        return promotions

    with open(PROMOTION_LOG, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in reversed(lines[-100:]):
        try:
            entry = json.loads(line.strip())
            promotions.append(entry)
            if len(promotions) >= limit:
                break
        except Exception:
            continue

    return promotions


def generate_dashboard() -> str:
    """生成面板内容"""
    status_data = load_status()
    intake_stats = get_intake_stats()
    promotion_stats = get_promotion_stats()
    recent_promotions = get_recent_promotions()

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = []
    lines.append(f"# 知识进化状态")
    lines.append(f"")
    lines.append(f"> 生成时间：{now}")
    lines.append(f"> 数据范围：今日 + 本周累计")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    lines.append(f"## 任务执行状态")
    lines.append(f"")
    lines.append(f"| 任务 | 最后运行 | 状态 | 运行时长 | 错误详情 |")
    lines.append(f"|------|----------|------|----------|----------|")

    for task_id, config in TASK_CONFIG.items():
        task_info = status_data.get("tasks", {}).get(task_id, {})
        last_run = task_info.get("last_run", None)
        task_status = task_info.get("status", "disabled")
        duration = task_info.get("duration_sec", 0)
        error = task_info.get("error", None)

        icon = config["icon"]
        name = config["name"]
        status_icon = get_task_status_icon(task_status)

        if last_run:
            time_ago = get_time_ago(last_run)
            duration_str = format_duration(duration) if duration else "-"
            error_str = error if error else "-"
            lines.append(f"| {icon} {name} | {time_ago} | {status_icon} | {duration_str} | {error_str} |")
        else:
            lines.append(f"| {icon} {name} | 从未 | ⏸️ 禁用 | - | - |")

    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    lines.append(f"## 内容处理量")
    lines.append(f"")
    lines.append(f"### intake 入口统计")
    lines.append(f"")
    lines.append(f"| 来源 | 今日新增 | 本周新增 | 本月新增 |")
    lines.append(f"|------|----------|----------|----------|")

    media_today = intake_stats["media"]["today"]
    media_week = intake_stats["media"]["week"]
    proactive_today = intake_stats["proactive"]["today"]
    proactive_week = intake_stats["proactive"]["week"]

    lines.append(f"| 📰 媒体监控 | {media_today}条 | {media_week}条 | - |")
    lines.append(f"| 🔍 主动学习 | {proactive_today}条 | {proactive_week}条 | - |")
    lines.append(f"| **合计** | **{media_today + proactive_today}条** | **{media_week + proactive_week}条** | - |")

    lines.append(f"")
    lines.append(f"### 晋升情况")
    lines.append(f"")
    lines.append(f"| 指标 | 今日 | 本周 | 晋升率 |")
    lines.append(f"|------|------|------|--------|")

    today_promoted = promotion_stats["today"]["total"]
    week_promoted = promotion_stats["week"]["total"]
    today_intake = media_today + proactive_today
    week_intake = media_week + proactive_week

    today_rate = f"{today_promoted/today_intake*100:.1f}%" if today_intake > 0 else "0%"
    week_rate = f"{week_promoted/week_intake*100:.1f}%" if week_intake > 0 else "0%"

    lines.append(f"| 自动晋升 | {today_promoted}条 | {week_promoted}条 | {week_rate} |")

    lines.append(f"")
    lines.append(f"**晋升路由分布：**")
    if promotion_stats["week"]["routes"]:
        for route, count in promotion_stats["week"]["routes"].items():
            route_name = {"prompt": "AI视频提示词库", "competitor": "竞品广告库", "insight": "行业洞察", "director": "导演动态"}.get(route, route)
            lines.append(f"- {route_name}：{count}条")
    else:
        lines.append(f"- 暂无晋升数据")

    lines.append(f"")
    lines.append(f"**最近晋升：**")
    if recent_promotions:
        for p in recent_promotions:
            dt = datetime.fromisoformat(p["timestamp"]).strftime("%m-%d %H:%M")
            title = p.get("title", "无标题")[:30]
            route = p.get("route", "unknown")
            route_name = {"prompt": "提示词", "competitor": "竞品", "insight": "洞察", "director": "导演"}.get(route, route)
            score = p.get("score", 0)
            lines.append(f"- {dt} | {title} → {route_name} | 评分{score}")
    else:
        lines.append(f"- 暂无晋升记录")

    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    lines.append(f"*本面板由 dashboard-refresh.py 自动生成*")
    lines.append(f"*下次更新：今日 {datetime.now().strftime('%H:00')} 点*")

    return "\n".join(lines)


def run():
    """主运行函数"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 刷新知识进化状态面板...")

    DASHBOARD_FILE.parent.mkdir(parents=True, exist_ok=True)

    content = generate_dashboard()

    DASHBOARD_FILE.write_text(content, encoding="utf-8")
    print(f"  ✅ 面板已更新: {DASHBOARD_FILE}")

    print()
    print(content)


if __name__ == "__main__":
    run()