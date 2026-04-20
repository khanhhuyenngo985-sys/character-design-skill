#!/bin/bash
# init-db.sh - 初始化技能进化数据库

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STORE_DIR="$(dirname "$SCRIPT_DIR")"
DB_PATH="${STORE_DIR}/store.db"

echo "初始化技能进化数据库: $DB_PATH"

sqlite3 "$DB_PATH" << 'EOF'
-- 技能质量指标表
CREATE TABLE IF NOT EXISTS skill_metrics (
  skill_id TEXT PRIMARY KEY,
  skill_name TEXT NOT NULL,
  category TEXT DEFAULT 'creative',
  applied_count INTEGER DEFAULT 0,
  success_count INTEGER DEFAULT 0,
  failure_count INTEGER DEFAULT 0,
  total_quality_score REAL DEFAULT 0,
  pattern_captured INTEGER DEFAULT 0,
  last_applied_at TEXT,
  last_success_at TEXT,
  last_failure_at TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now'))
);

-- 进化记录表
CREATE TABLE IF NOT EXISTS evolution_records (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  skill_id TEXT,
  skill_name TEXT,
  mode TEXT CHECK(mode IN ('REFINE', 'BRANCH', 'CAPTURE')),
  trigger_reason TEXT,
  changes_summary TEXT,
  quality_before REAL,
  quality_after REAL,
  approved INTEGER DEFAULT 0,
  approved_by TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  FOREIGN KEY (skill_id) REFERENCES skill_metrics(skill_id)
);

-- 案例模式捕获表
CREATE TABLE IF NOT EXISTS case_patterns (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  skill_id TEXT,
  pattern_text TEXT NOT NULL,
  pattern_tags TEXT,
  source_case TEXT,
  frequency INTEGER DEFAULT 1,
  effectiveness REAL DEFAULT 0.5,
  created_at TEXT DEFAULT (datetime('now')),
  FOREIGN KEY (skill_id) REFERENCES skill_metrics(skill_id)
);

-- 项目记录表
CREATE TABLE IF NOT EXISTS project_records (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  project_name TEXT,
  project_path TEXT,
  skills_used TEXT,
  overall_quality REAL,
  notes TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_evolution_skill ON evolution_records(skill_id);
CREATE INDEX IF NOT EXISTS idx_evolution_mode ON evolution_records(mode);
CREATE INDEX IF NOT EXISTS idx_patterns_skill ON case_patterns(skill_id);
CREATE INDEX IF NOT EXISTS idx_patterns_freq ON case_patterns(frequency);

-- 初始化已存在的技能
INSERT OR IGNORE INTO skill_metrics (skill_id, skill_name, category) VALUES
  ('video-analysis', '视频拉片分析', 'creative'),
  ('prompt-matrix', '提示词矩阵', 'creative'),
  ('scene-design', '分镜设计', 'creative'),
  ('video-prompt-writer', '视频提示词写作', 'creative'),
  ('beauty-editorial', '美妆Editorial', 'industry'),
  ('luxury-fashion', '奢侈时尚', 'industry'),
  ('liquor-luxury', '酒类奢侈', 'industry'),
  ('food-product', '食品产品', 'industry'),
  ('tech-product', '科技产品', 'industry'),
  ('humanize-dialogue', '台词去AI味', 'utility'),
  ('brief-parser', 'Brief解析', 'utility'),
  ('creative-director', '创意总监', 'agent'),
  ('director', '导演', 'agent'),
  ('screenwriter', '编剧', 'agent'),
  ('colorist', '调色师', 'agent');

EOF

echo "数据库初始化完成"
sqlite3 "$DB_PATH" "SELECT name FROM sqlite_master WHERE type='table';"
