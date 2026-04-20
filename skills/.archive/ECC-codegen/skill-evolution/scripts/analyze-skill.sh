#!/bin/bash
# analyze-skill.sh - 分析单个技能的健康度

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STORE_DIR="$(dirname "$SCRIPT_DIR")"
DB_PATH="${STORE_DIR}/store.db"

SKILL_ID="${1:-}"

if [ -z "$SKILL_ID" ]; then
  echo "用法: $0 <skill_id>"
  echo "示例: $0 video-analysis"
  exit 1
fi

echo "=== 技能健康度分析: $SKILL_ID ==="
echo ""

# 检查技能是否存在
EXISTS=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM skill_metrics WHERE skill_id='$SKILL_ID';")

if [ "$EXISTS" -eq 0 ]; then
  echo "技能 $SKILL_ID 不存在，初始化中..."
  sqlite3 "$DB_PATH" "INSERT INTO skill_metrics (skill_id, skill_name) VALUES ('$SKILL_ID', '$SKILL_ID');"
fi

# 获取各项指标
sqlite3 -header -column "$DB_PATH" << EOF
SELECT
  skill_id AS "技能ID",
  skill_name AS "技能名",
  category AS "分类",
  applied_count AS "调用次数",
  success_count AS "成功次数",
  failure_count AS "失败次数",
  CASE
    WHEN applied_count > 0 THEN ROUND(CAST(success_count AS REAL) / applied_count, 3)
    ELSE 0
  END AS "成功率",
  CASE
    WHEN (success_count + failure_count) > 0 THEN ROUND(CAST(failure_count AS REAL) / (success_count + failure_count), 3)
    ELSE 0
  END AS "失败率",
  CASE
    WHEN success_count > 0 THEN ROUND(total_quality_score / success_count, 2)
    ELSE 0
  END AS "平均质量",
  pattern_captured AS "捕获模式数",
  last_applied_at AS "最后调用",
  CASE
    WHEN last_applied_at IS NULL THEN '从未'
    ELSE CAST(CAST((julianday('now') - julianday(last_applied_at)) AS INTEGER) AS TEXT)
  END AS "未更新天数"
FROM skill_metrics
WHERE skill_id = '$SKILL_ID';
EOF

echo ""
echo "=== 最近进化记录 ==="
sqlite3 -header -column "$DB_PATH" << EOF
SELECT
  mode AS "模式",
  trigger_reason AS "触发原因",
  SUBSTR(changes_summary, 1, 50) AS "变更摘要",
  approved AS "已确认",
  created_at AS "时间"
FROM evolution_records
WHERE skill_id = '$SKILL_ID'
ORDER BY created_at DESC
LIMIT 5;
EOF

echo ""
echo "=== 高频模式 ==="
sqlite3 -header -column "$DB_PATH" << EOF
SELECT
  pattern_text AS "模式内容",
  frequency AS "出现频率",
  effectiveness AS "有效度"
FROM case_patterns
WHERE skill_id = '$SKILL_ID'
ORDER BY frequency DESC
LIMIT 5;
EOF

# 计算健康度评分
python3 - "$SKILL_ID" "$DB_PATH" << 'PYEOF'
import sqlite3, sys

skill_id, db_path = sys.argv[1], sys.argv[2]
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("""
  SELECT applied_count, success_count, failure_count, total_quality_score,
         pattern_captured, last_applied_at
  FROM skill_metrics WHERE skill_id = ?
""", (skill_id,))
row = cur.fetchone()

if not row:
    print("无数据")
    sys.exit(0)

applied, success, failure, total_q, patterns, last_used = row

# 健康度评分计算
score = 0
reasons = []

# 基础分数：调用次数 (最多20分)
if applied > 50:
    score += 20
elif applied > 20:
    score += 15
elif applied > 5:
    score += 10
elif applied > 0:
    score += 5
reasons.append(f"调用次数: {applied}")

# 成功率 (最多30分)
if applied > 0:
    success_rate = success / applied
    score += int(success_rate * 30)
    reasons.append(f"成功率: {success_rate:.1%}")

# 失败率惩罚 (最多-20分)
if (success + failure) > 0:
    fail_rate = failure / (success + failure)
    score -= int(fail_rate * 20)
    reasons.append(f"失败率: {fail_rate:.1%} ({failure}次)")

# 质量分数 (最多25分)
if success > 0:
    avg_q = total_q / success
    score += int((avg_q / 5) * 25)
    reasons.append(f"平均质量: {avg_q:.2f}/5")

# 模式捕获 (最多15分)
if patterns > 20:
    score += 15
elif patterns > 10:
    score += 10
elif patterns > 5:
    score += 7
elif patterns > 0:
    score += 3
reasons.append(f"捕获模式: {patterns}")

# 活跃度 (最多10分)
if last_used:
    import time
    from datetime import datetime
    last = datetime.fromisoformat(last_used)
    days = (datetime.now() - last).days
    if days < 7:
        score += 10
    elif days < 30:
        score += 7
    elif days < 90:
        score += 3
    reasons.append(f"最后活跃: {days}天前")

score = max(0, min(100, score))

grade = "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 50 else "D"

print(f"\n{'='*40}")
print(f"健康度评分: {score}/100 (Grade: {grade})")
print(f"{'='*40}")
for r in reasons:
    print(f"  • {r}")

conn.close()
PYEOF
