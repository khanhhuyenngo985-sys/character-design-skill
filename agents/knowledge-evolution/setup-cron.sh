#!/bin/bash
#
# 知识库自动进化 - Cron 设置脚本
# 运行方式: bash setup-cron.sh [install|remove|status|run-all]
#

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCANNER="$SCRIPT_DIR/scanner.py"
COMPETITOR="$SCRIPT_DIR/competitor-scraper.py"
MEDIA="$SCRIPT_DIR/media-monitor.py"
PROACTIVE="$SCRIPT_DIR/proactive-learner.py"
PROMOTER="$SCRIPT_DIR/knowledge-auto-promoter.py"
NOTEBOOK="$SCRIPT_DIR/notebooklm-auto-learner.py"
CITATION="$SCRIPT_DIR/citation-audit.py"
DASHBOARD="$SCRIPT_DIR/dashboard-refresh.py"
LOG_DIR="/tmp/knowledge-evolution"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

# Cron条目
# 每周日凌晨2点：知识库健康扫描
CRON_SCANNER="0 2 * * 0 cd $SCRIPT_DIR && python3 $SCANNER >> $LOG_DIR/scanner.log 2>&1 # 知识库每周扫描"
# 每周日凌晨3点：竞品广告库更新
CRON_COMPETITOR="0 3 * * 0 cd $SCRIPT_DIR && python3 $COMPETITOR >> $LOG_DIR/competitor.log 2>&1 # 竞品广告库每周更新"
# 每天早上8点：行业媒体监控
CRON_MEDIA="0 8 * * * cd $SCRIPT_DIR && python3 $MEDIA >> $LOG_DIR/media.log 2>&1 # 行业媒体每日监控"
# 每6小时：主动学习（3点、9点、15点、21点）
CRON_PROACTIVE="0 3,9,15,21 * * * cd $SCRIPT_DIR && python3 $PROACTIVE >> $LOG_DIR/proactive.log 2>&1 # 主动学习每6小时"
# 每天10点：知识自动晋升
CRON_PROMOTER="0 10 * * * cd $SCRIPT_DIR && python3 $PROMOTER >> $LOG_DIR/promoter.log 2>&1 # 知识自动晋升每天10点"
# 每天9点：NotebookLM 自动学习
CRON_NOTEBOOK="0 9 * * * cd $SCRIPT_DIR && python3 $NOTEBOOK >> $LOG_DIR/notebook.log 2>&1 # NotebookLM 自动学习每天9点"
# 每周一10点：引用审计
CRON_CITATION="0 10 * * 1 cd $SCRIPT_DIR && python3 $CITATION >> $LOG_DIR/citation.log 2>&1 # 知识引用每周审计"
CRON_DASHBOARD="0 10 * * * cd $SCRIPT_DIR && python3 $DASHBOARD >> $LOG_DIR/dashboard.log 2>&1 # 知识进化看板每日刷新"

show_status() {
    echo "📊 Cron 状态检查..."
    echo ""
    echo "当前安装的任务："
    crontab -l 2>/dev/null | grep -E "(knowledge-evolution|竞品|媒体|主动学习)" | sed 's/^/  /' || echo "  (无)"
    echo ""
    echo "最近运行日志："
    ls -la "$LOG_DIR"/*.log 2>/dev/null | tail -5 | sed 's/^/  /' || echo "  (无日志)"
}

case "$1" in
    install)
        echo "📦 安装知识库自动进化 Cron..."

        # 移除旧条目（如果有）
        crontab -l 2>/dev/null | grep -v "knowledge-evolution\|竞品广告库每周更新\|行业媒体每日监控\|主动学习每6小时\|知识自动晋升每天10点\|NotebookLM 自动学习每天9点\|知识引用每周审计\|知识进化看板每日刷新" | crontab - 2>/dev/null || true

        # 添加新条目
        (crontab -l 2>/dev/null; echo "$CRON_SCANNER") | crontab -
        (crontab -l 2>/dev/null; echo "$CRON_COMPETITOR") | crontab -
        (crontab -l 2>/dev/null; echo "$CRON_MEDIA") | crontab -
        (crontab -l 2>/dev/null; echo "$CRON_PROACTIVE") | crontab -
        (crontab -l 2>/dev/null; echo "$CRON_PROMOTER") | crontab -
        (crontab -l 2>/dev/null; echo "$CRON_NOTEBOOK") | crontab -
        (crontab -l 2>/dev/null; echo "$CRON_CITATION") | crontab -
        (crontab -l 2>/dev/null; echo "$CRON_DASHBOARD") | crontab -

        echo "✅ 安装成功！"
        echo ""
        echo "定时任务："
        echo "  每周日凌晨2点 - 知识库健康扫描"
        echo "  每周日凌晨3点 - 竞品广告库更新"
        echo "  每天早上8点 - 行业媒体监控"
        echo "  每6小时(3/9/15/21点) - 主动学习"
        echo "  每天9点 - NotebookLM 自动学习"
        echo "  每天10点 - 知识自动晋升"
        echo "  每周一10点 - 引用审计"
        echo "  每天10点 - 知识进化看板刷新"
        echo ""
        show_status
        ;;
    remove)
        echo "🗑️ 移除知识库自动进化 Cron..."
        crontab -l 2>/dev/null | grep -v "knowledge-evolution\|竞品广告库每周更新\|行业媒体每日监控\|主动学习每6小时\|知识自动晋升每天10点\|NotebookLM 自动学习每天9点\|知识引用每周审计\|知识进化看板每日刷新" | crontab - 2>/dev/null || true
        echo "✅ 已移除所有进化任务"
        ;;
    status)
        show_status
        ;;
    run-all)
        echo "🚀 运行全部进化脚本..."
        echo ""
        echo "📊 1. 知识库健康扫描..."
        python3 "$SCANNER"
        echo ""
        echo "🏪 2. 竞品广告库更新..."
        python3 "$COMPETITOR"
        echo ""
        echo "📰 3. 行业媒体监控..."
        python3 "$MEDIA"
        echo ""
        echo "🔍 4. 主动学习..."
        python3 "$PROACTIVE"
        echo ""
        echo "✅ 全部完成！"
        ;;
    run-scanner)
        echo "📊 运行知识库健康扫描..."
        python3 "$SCANNER"
        ;;
    run-competitor)
        echo "🏪 运行竞品广告库更新..."
        python3 "$COMPETITOR"
        ;;
    run-media)
        echo "📰 运行行业媒体监控..."
        python3 "$MEDIA"
        ;;
    run-proactive)
        echo "🔍 运行主动学习..."
        python3 "$PROACTIVE"
        ;;
    run-notebook)
        echo "📓 运行 NotebookLM 自动学习..."
        python3 "$NOTEBOOK"
        ;;
    *)
        echo "用法: bash setup-cron.sh [install|remove|status|run-all]"
        echo ""
        echo "  install        - 安装全部自动任务"
        echo "  remove         - 移除全部自动任务"
        echo "  status         - 查看当前状态和日志"
        echo "  run-all        - 立即运行全部脚本"
        echo "  run-scanner    - 仅运行知识库扫描"
        echo "  run-competitor - 仅运行竞品库更新"
        echo "  run-media      - 仅运行媒体监控"
        echo "  run-proactive  - 仅运行主动学习"
        echo "  run-notebook   - 仅运行 NotebookLM 自动学习"
        ;;
esac
