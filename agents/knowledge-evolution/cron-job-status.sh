#!/bin/bash
#
# 知识进化状态快速查看
#

STATUS_FILE="/tmp/knowledge-evolution/status.json"

if [ ! -f "$STATUS_FILE" ]; then
    echo "📊 知识进化状态"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "⚠️ 暂无状态数据"
    echo ""
    echo "提示: 运行 cron 任务后会有数据"
    exit 0
fi

echo "📊 知识进化状态 | $(date '+%Y-%m-%d %H:%M')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 读取任务状态
tasks=$(python3 -c "
import json
from datetime import datetime

with open('$STATUS_FILE', 'r') as f:
    data = json.load(f)

tasks_config = {
    'competitor': ('🏪 竞品广告库', 'success'),
    'media': ('📰 媒体监控', 'success'),
    'proactive': ('🔍 主动学习', 'success'),
    'scanner': ('📊 健康扫描', 'success'),
    'promoter': ('🚀 知识晋升', 'success'),
}

for task_id, (name, default_status) in tasks_config.items():
    info = data.get('tasks', {}).get(task_id, {})
    if info:
        status = info.get('status', default_status)
        last_run = info.get('last_run', None)
        new_content = info.get('new_content', 0)
        icon = '✅' if status == 'success' else ('⚠️' if status == 'warn' else '❌')
        if last_run:
            dt = datetime.fromisoformat(last_run)
            delta = datetime.now() - dt
            if delta.total_seconds() < 3600:
                ago = f'{int(delta.total_seconds()//60)}分钟前'
            elif delta.total_seconds() < 86400:
                ago = f'{int(delta.total_seconds()//3600)}小时前'
            else:
                ago = f'{int(delta.days)}天前'
            print(f'{icon} {name[2:]} | {ago} | +{new_content}条')
        else:
            print(f'⏸️ {name[2:]} | 从未运行 | -')
    else:
        print(f'⏸️ {name[2:]} | 未配置 | -')
")
echo "$tasks"