#!/usr/bin/env python3
"""
状态写入器
各 cron 任务执行后调用，写入状态到 status.json
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

LOG_DIR = Path("/tmp/knowledge-evolution")
STATUS_FILE = LOG_DIR / "status.json"


def load_status() -> dict:
    """加载现有状态"""
    if STATUS_FILE.exists():
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "last_run": None,
        "tasks": {},
        "today_stats": {"intake_new": 0, "promoted": 0, "rejected": 0, "watched": 0},
        "week_stats": {"intake_new": 0, "promoted": 0, "rejected": 0, "watched": 0}
    }


def save_status(status: dict):
    """保存状态"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    status["last_run"] = datetime.now().isoformat()
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status, f, ensure_ascii=False, indent=2)


def write_task_status(
    task_name: str,
    status: str,  # "success"|"fail"|"warn"
    duration_sec: int,
    error: Optional[str] = None,
    new_content: int = 0
):
    """
    写入任务状态

    Args:
        task_name: "competitor"|"media"|"proactive"|"scanner"|"promoter"
        status: "success"|"fail"|"warn"
        duration_sec: 运行耗时（秒）
        error: 错误信息（如有）
        new_content: 新增内容数量
    """
    status_data = load_status()

    status_data["tasks"][task_name] = {
        "last_run": datetime.now().isoformat(),
        "status": status,
        "duration_sec": duration_sec,
        "error": error,
        "new_content": new_content
    }

    save_status(status_data)
    print(f"  ✅ 状态已写入: {task_name} -> {status}")


def update_stats(promoted: int = 0, rejected: int = 0, watched: int = 0, intake_new: int = 0):
    """更新统计数据"""
    status_data = load_status()

    if "today_stats" not in status_data:
        status_data["today_stats"] = {"intake_new": 0, "promoted": 0, "rejected": 0, "watched": 0}
    if "week_stats" not in status_data:
        status_data["week_stats"] = {"intake_new": 0, "promoted": 0, "rejected": 0, "watched": 0}

    status_data["today_stats"]["promoted"] += promoted
    status_data["today_stats"]["rejected"] += rejected
    status_data["today_stats"]["watched"] += watched
    status_data["today_stats"]["intake_new"] += intake_new

    status_data["week_stats"]["promoted"] += promoted
    status_data["week_stats"]["rejected"] += rejected
    status_data["week_stats"]["watched"] += watched
    status_data["week_stats"]["intake_new"] += intake_new

    save_status(status_data)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("用法: python3 status-writer.py <task_name> <status> [duration_sec] [error] [new_content]")
        sys.exit(1)

    task_name = sys.argv[1]
    status = sys.argv[2]
    duration_sec = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    error = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != "None" else None
    new_content = int(sys.argv[5]) if len(sys.argv) > 5 else 0

    write_task_status(task_name, status, duration_sec, error, new_content)
