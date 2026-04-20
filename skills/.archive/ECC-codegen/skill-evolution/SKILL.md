---
name: skill-evolution
description: 创意技能进化层 - 监控技能健康度，自动触发 REFINE/BRANCH/CAPTURE 进化
origin: ECC + OpenSpace
version: 1.0.0
---

# Skill Evolution - 创意技能进化层

基于 OpenSpace 自进化思想，为白梦客 AI 创作团队设计的技能进化系统。

## 核心概念

**技能不是静态文件，是有生命周期的实体。** 每次项目执行都应该让相关技能变得更好。

## 三种进化模式

| 模式 | 触发条件 | 动作 |
|-----|---------|------|
| **REFINE** | 技能 success_score 下降 ≥15% 或 失败率上升 | 优化提示词参数，修复失败模式 |
| **BRANCH** | 发现新场景/风格/平台组合 | 复制技能并针对性调整 |
| **CAPTURE** | 3+ 案例出现共同成功模式 | 从案例提取新技能或更新现有技能 |

## 监控指标

| 指标 | 含义 | 健康范围 |
|-----|------|---------|
| `applied_count` | 被调用次数 | 越高越好 |
| `success_score` | 成功率 (0-1) | > 0.75 |
| `avg_quality` | 平均质量评分 (1-5) | > 3.5 |
| `pattern_captured` | 从案例捕获的新模式数 | 持续增长 |
| `failure_rate` | 失败率 | < 0.2 |
| `days_since_update` | 距上次更新天数 | < 30 |

## 进化触发规则

```
AUTO_TRIGGERS:
  - success_score 下降超过 15% → REFINE
  - 连续 3 个新场景出现 → BRANCH
  - 3+ 案例有共同模式 → CAPTURE
  - 30 天无更新 → 提示人工审查

MANUAL_TRIGGERS:
  - 用户手动调用 /skill-evolve
  - 项目完成后自动分析
```

## 目录结构

```
skill-evolution/
├── store.db              # SQLite: 技能质量指标
├── evolution-log.md      # 进化历史记录
├── monitor.md            # 当前监控仪表板
├── scripts/
│   ├── init-db.sh        # 初始化数据库
│   ├── analyze-skill.sh  # 分析单个技能
│   ├── evolve.sh         # 触发进化
│   └── report.sh         # 生成报告
└── prompts/
    ├── post-execution.md # 项目完成分析模板
    └── evolution.md      # 进化建议模板
```

## 使用方式

### 1. 项目完成后自动分析

```
/skill-evolution analyze --project <项目路径>
```

分析项目，提炼成功模式，更新相关技能的健康指标。

### 2. 查看技能健康状态

```
/skill-evolution status [技能名]
```

显示技能的各项指标和健康度评分。

### 3. 手动触发进化

```
/skill-evolution evolve [--skill <技能名>] [--mode REFINE|BRANCH|CAPTURE]
```

根据模式执行进化，人工确认后写入更改。

### 4. 查看进化历史

```
/skill-evolution log [--skill <技能名>] [--limit 10]
```

显示技能的进化历史和模式变化。

## 数据库 Schema

```sql
CREATE TABLE skill_metrics (
  skill_id TEXT PRIMARY KEY,
  skill_name TEXT NOT NULL,
  applied_count INTEGER DEFAULT 0,
  success_count INTEGER DEFAULT 0,
  failure_count INTEGER DEFAULT 0,
  total_quality_score REAL DEFAULT 0,
  pattern_captured INTEGER DEFAULT 0,
  last_applied_at TEXT,
  last_success_at TEXT,
  last_failure_at TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE evolution_records (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  skill_id TEXT,
  mode TEXT,  -- REFINE | BRANCH | CAPTURE
  trigger_reason TEXT,
  changes_summary TEXT,
  approved INTEGER DEFAULT 0,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (skill_id) REFERENCES skill_metrics(skill_id)
);

CREATE TABLE case_patterns (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  skill_id TEXT,
  pattern_text TEXT,
  source_case TEXT,
  frequency INTEGER DEFAULT 1,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (skill_id) REFERENCES skill_metrics(skill_id)
);
```

## 质量评分标准

每个项目完成后，对使用的技能打分 (1-5):

| 分数 | 含义 |
|-----|------|
| 5 | 超出预期，完美执行 |
| 4 | 达到预期，有些小瑕疵 |
| 3 | 基本可用，有明显问题 |
| 2 | 需要大幅修改 |
| 1 | 完全失败 |

## 与其他技能的关系

- **video-analysis** → 分析视频案例，产出 pattern → 触发 CAPTURE
- **prompt-matrix** → 技能的技能，存储提示词参数矩阵
- **scene-design** → 分镜技能，有独立的 .evolution 目录
- **skill-stocktake** → 定期人工审查，补充自动监控的盲区

## 注意事项

1. **创意技能不追求自动化程度过高** — 美学判断需要人工审核
2. **所有进化需要人工确认** — 不自动写入技能文件
3. **案例库是进化的燃料** — case-library 丰富后进化才有效
