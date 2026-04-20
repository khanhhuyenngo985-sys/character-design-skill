#!/bin/bash
# evolve.sh - 触发技能进化

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STORE_DIR="$(dirname "$SCRIPT_DIR")"
DB_PATH="${STORE_DIR}/store.db"
LOG_PATH="${STORE_DIR}/evolution-log.md"

SKILL_ID="${1:-}"
MODE="${2:-}"  # REFINE | BRANCH | CAPTURE

if [ -z "$SKILL_ID" ] || [ -z "$MODE" ]; then
  echo "用法: $0 <skill_id> <REFINE|BRANCH|CAPTURE> [触发原因]"
  echo "示例: $0 video-analysis REFINE \"成功率下降15%\""
  exit 1
fi

TRIGGER_REASON="${3:-手动触发}"

echo "=== 技能进化: $SKILL_ID ($MODE) ==="
echo "触发原因: $TRIGGER_REASON"
echo ""

# 获取技能当前状态
python3 - "$SKILL_ID" "$DB_PATH" "$MODE" "$TRIGGER_REASON" << 'PYEOF'
import sqlite3, sys, datetime
from pathlib import Path

skill_id, db_path, mode, trigger_reason = sys.argv[1], sys.argv[2], sys.argv[3], ' '.join(sys.argv[4:])

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# 获取当前指标
cur.execute("""
  SELECT applied_count, success_count, failure_count, total_quality_score, pattern_captured
  FROM skill_metrics WHERE skill_id = ?
""", (skill_id,))
row = cur.fetchone()

if not row:
    print(f"错误: 技能 {skill_id} 不存在")
    sys.exit(1)

applied, success, failure, total_q, patterns = row
quality_before = total_q / success if success > 0 else 0

print(f"当前状态:")
print(f"  调用次数: {applied}")
print(f"  成功率: {success}/{applied} = {success/applied*100:.1f}%" if applied > 0 else "  成功率: N/A")
print(f"  失败次数: {failure}")
print(f"  平均质量: {quality_before:.2f}/5")
print(f"  捕获模式: {patterns}")
print()

# 根据模式生成进化建议
suggestions = []

if mode == "REFINE":
    suggestions = [
        f"优化 {skill_id} 的提示词参数",
        f"检查失败案例 ({failure} 次失败)，提取失败模式",
        "更新 SKILL.md 中的示例和最佳实践",
        "调整提示词矩阵中的权重分配"
    ]
elif mode == "BRANCH":
    suggestions = [
        f"为 {skill_id} 创建细分版本（如：按行业/按平台/按风格）",
        "复制技能到新目录，命名格式: skill-name-{variant}",
        "针对新场景调整核心参数",
        "更新主技能的 BRANCH 说明"
    ]
elif mode == "CAPTURE":
    suggestions = [
        f"从 {patterns} 个捕获模式中提炼共性",
        "提取成功模式的的核心特征",
        "更新 skill.md 的 PATTERNS 部分",
        "如模式足够通用，考虑提升为独立技能"
    ]

print(f"进化建议 ({mode}):")
for i, s in enumerate(suggestions, 1):
    print(f"  {i}. {s}")
print()

# 生成变更摘要
changes_summary = f"[{mode}] {trigger_reason}. 建议: {'; '.join(suggestions[:2])}"

# 记录进化请求（待批准）
cur.execute("""
  INSERT INTO evolution_records
  (skill_id, mode, trigger_reason, changes_summary, quality_before, approved)
  VALUES (?, ?, ?, ?, ?, 0)
""", (skill_id, mode, trigger_reason, changes_summary, quality_before))

conn.commit()
conn.close()

print(f"进化请求已记录，等待人工确认...")
print(f"数据库ID: (请查看 store.db 获取)")
PYEOF

echo ""
echo "确认后，运行以下命令完成进化："
echo "  sqlite3 $DB_PATH \"UPDATE evolution_records SET approved=1 WHERE approved=0 ORDER BY id DESC LIMIT 1;\""
