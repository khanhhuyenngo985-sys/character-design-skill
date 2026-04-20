#!/bin/bash
# report.sh - 生成技能进化监控报告

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STORE_DIR="$(dirname "$SCRIPT_DIR")"
DB_PATH="${STORE_DIR}/store.db"
MONITOR_PATH="${STORE_DIR}/monitor.md"

echo "=== 技能进化监控报告 ==="
echo "生成时间: $(date '+%Y-%m-%d %H:%M')"
echo ""

# 整体统计
echo "## 整体统计"
echo ""
sqlite3 -header -column "$DB_PATH" << 'EOF'
SELECT
  COUNT(*) AS "技能总数",
  SUM(applied_count) AS "总调用次数",
  SUM(success_count) AS "总成功次数",
  SUM(failure_count) AS "总失败次数",
  SUM(pattern_captured) AS "总捕获模式"
FROM skill_metrics;
EOF

echo ""
echo "## 需要关注的技能"
echo ""

# 失败率过高的技能
echo "### 失败率 > 20%"
sqlite3 -header -column "$DB_PATH" << 'EOF'
SELECT
  skill_id AS "技能",
  failure_count AS "失败",
  success_count AS "成功",
  ROUND(CAST(failure_count AS REAL) / (success_count + failure_count) * 100, 1) AS "失败率%"
FROM skill_metrics
WHERE (success_count + failure_count) > 0
  AND CAST(failure_count AS REAL) / (success_count + failure_count) > 0.2
ORDER BY ROUND(CAST(failure_count AS REAL) / (success_count + failure_count) * 100, 1) DESC;
EOF

# 30天未活跃的技能
echo ""
echo "### 30天未调用"
sqlite3 -header -column "$DB_PATH" << 'EOF'
SELECT
  skill_id AS "技能",
  applied_count AS "调用",
  last_applied_at AS "最后调用"
FROM skill_metrics
WHERE last_applied_at IS NULL
   OR (julianday('now') - julianday(last_applied_at)) > 30
ORDER BY last_applied_at;
EOF

# 高质量技能
echo ""
echo "### 高质量技能 (质量 > 4.0)"
sqlite3 -header -column "$DB_PATH" << 'EOF'
SELECT
  skill_id AS "技能",
  ROUND(total_quality_score * 1.0 / success_count, 2) AS "平均质量",
  success_count AS "成功次数",
  pattern_captured AS "模式数"
FROM skill_metrics
WHERE success_count > 0
  AND (total_quality_score * 1.0 / success_count) > 4.0
ORDER BY 平均质量 DESC;
EOF

echo ""
echo "## 进化记录"
echo ""
sqlite3 -header -column "$DB_PATH" << 'EOF'
SELECT
  skill_id AS "技能",
  mode AS "模式",
  trigger_reason AS "触发原因",
  created_at AS "时间",
  approved AS "已确认"
FROM evolution_records
ORDER BY created_at DESC
LIMIT 10;
EOF

echo ""
echo "## 模式捕获排行"
echo ""
sqlite3 -header -column "$DB_PATH" << 'EOF'
SELECT
  skill_id AS "技能",
  COUNT(*) AS "模式数",
  SUM(frequency) AS "总出现",
  MAX(effectiveness) AS "最高有效度"
FROM case_patterns
GROUP BY skill_id
ORDER BY 模式数 DESC
LIMIT 10;
EOF

# 写入 monitor.md
cat > "$MONITOR_PATH" << 'EOF'
# 技能进化监控仪表板

> 自动生成，请勿手动编辑

## 最后更新

EOF

echo "$(date '+%Y-%m-%d %H:%M')" >> "$MONITOR_PATH"

cat >> "$MONITOR_PATH" << 'EOF'

## 健康度概览

| 技能 | 健康度 | 状态 |
|-----|-------|------|
EOF

python3 - "$DB_PATH" >> "$MONITOR_PATH" << 'PYEOF'
import sqlite3, sys
db_path = sys.argv[1]
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("SELECT skill_id FROM skill_metrics")
for (skill_id,) in cur.fetchall():
    cur.execute("""
        SELECT applied_count, success_count, failure_count, total_quality_score, pattern_captured
        FROM skill_metrics WHERE skill_id = ?
    """, (skill_id,))
    row = cur.fetchone()
    if not row: continue
    applied, success, failure, total_q, patterns = row

    score = 0
    if applied > 50: score += 20
    elif applied > 20: score += 15
    elif applied > 5: score += 10
    elif applied > 0: score += 5

    if applied > 0:
        score += int((success / applied) * 30)

    if (success + failure) > 0:
        score -= int((failure / (success + failure)) * 20)

    if success > 0:
        score += int((total_q / success / 5) * 25)

    if patterns > 20: score += 15
    elif patterns > 10: score += 10
    elif patterns > 5: score += 7
    elif patterns > 0: score += 3

    score = max(0, min(100, score))
    grade = "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 50 else "D"
    status = "正常" if score >= 70 else "需关注" if score >= 50 else "待修复"

    print(f"| {skill_id} | {score}/100 ({grade}) | {status} |")

conn.close()
PYEOF

echo ""
echo "报告已保存到: $MONITOR_PATH"
