# 白梦客创作技能索引

> 本文件帮助团队成员（和AI agent）理解：有哪些技能，什么时候用，怎么组合。

---

## 技能地图

```
创意方向选择
    │
    ├── style-fusion ──── B×A 风格融合 ──────────────────────────────┐
    │                        输出：融合风格参数 + 平台提示词              │
    │                                                                  │
    ▼                                                                  │
创作简报确认                                                              │
    │                                                                  │
    ├── creative-director ── Mood Board + 方向判断                      │
    │                                                                  │
    ▼                                                                  │
A5 分镜脚本完成                                                           │
    │                                                                  │
    ├── prompt-engineer ── 强制查询4个知识库 ────────────────────────┐ │
    │                        输出：结构化提示词（含查询记录）            │ │
    │                                                                  │ │
    │                        底层调用：                                │ │
    │                        ┌─────────────────────────────┐            │ │
    │                        │  video-prompt-schema ──────┼── JSON    │ │
    │                        │  prompt-matrix ────────────┼── 平台格式│ │
    │                        └─────────────────────────────┘            │ │
    │                                                                   │ │
    └──────────────────┬───────────────────────────────────────────────┘ │
                       ▼
                 vfx-supervisor ── AI可行性评估
                       │
                       ▼
               AI视频生成工具（Seedance / Vidu / 海螺）
```

---

## 四层说明

### Layer 1 — 风格融合（最上层）
**技能：** `style-fusion`

| 属性 | 说明 |
|------|------|
| 什么时候用 | 项目开始前，需要确定风格方向 |
| 输入 | B系列代码（B1-B5）+ A系列代码（A1-A4）|
| 输出 | 融合后的调色板、光影、构图、节奏、质感参数 |
| 谁调用 | creative-director、用户 |
| 不调用其他技能 | 独立运行 |

**使用示例：**
```bash
python3 ~/.claude/skills/style-fusion/fusion.py B2 A3 --platform seedance
```

---

### Layer 2 — 创作简报
**技能：** `creative-director`（agent）

| 属性 | 说明 |
|------|------|
| 什么时候用 | 收到客户Brief后 |
| 输入 | 客户需求 + style-fusion 输出的风格参数 |
| 输出 | Mood Board + 创意方向 + A1简报 |
| 调用 | 内部判断，不调用其他skill |

---

### Layer 3 — 提示词工程（中层）
**调用关系：**
```
prompt-engineer
    ├── → video-prompt-schema ── 输出 JSON Schema
    └── → prompt-matrix ────────── 输出平台化格式
```

这两个是 prompt-engineer 的**内部工具**，不单独使用。

#### `video-prompt-schema`
| 属性 | 说明 |
|------|------|
| 核心功能 | 分镜脚本 → 结构化 JSON Schema |
| 输入 | A5分镜脚本（景别/角度/运动/时长） |
| 输出 | 标准化的 JSON，含 palette/lighting/composition/rhythm/texture |
| 平台无关 | 是，Schema 与平台解耦 |

#### `prompt-matrix`
| 属性 | 说明 |
|------|------|
| 核心功能 | JSON Schema → 平台化提示词 |
| 输入 | video-prompt-schema 输出的 JSON |
| 输出 | Seedance / Vidu / 海螺 格式的提示词 |
| 平台相关 | 是，根据目标平台格式化 |

**三者关系：**
```
video-prompt-schema（格式转换）
    ↓
prompt-matrix（平台适配）
    ↓
prompt-engineer（组装 + 质量门控）
```

---

### Layer 4 — 视觉叙事
**技能：** `video-prompt-writer`

| 属性 | 说明 |
|------|------|
| 什么时候用 | 写提示词时的规范参考 |
| 输入 | 视觉序列描述 |
| 输出 | "写看到的，不写想到的" — 视觉序列描述法 |
| 谁用 | prompt-engineer 在组装提示词时的参考 |

**核心原则：** AI视频模型是"视觉序列匹配器"，不理解因果逻辑和情绪标签。提示词要写成它能匹配的视觉序列描述。

---

## 决策树：什么时候用哪个

```
项目开始，有风格方向了吗？
├── 未知 ──→ style-fusion（找融合配方）
│              └─→ 选 B1-B5 + A1-A4 → 得到风格参数
│
├── 已知 ──→ creative-director（出 Mood Board）
│              └─→ 出 A1 创作简报
│
└── 分镜完成后 ──→ prompt-engineer（生成提示词）
                    ├─→ video-prompt-schema（结构化）
                    ├─→ prompt-matrix（平台化）
                    └─→ 输出含4知识库查询记录的提示词
```

---

## Agent × 技能调用关系

| Agent | 调用的 Skill | 角色 |
|-------|-------------|------|
| creative-director | 无（内部判断）| 方向决策 |
| director | 无（内部判断）| 分镜设计 |
| prompt-engineer | video-prompt-schema + prompt-matrix | 提示词组装 |
| vfx-supervisor | 无（内部判断）| AI可行性评估 |
| style-fusion | 无（独立使用）| 风格融合 |

---

## 禁止反向调用

- creative-director **不调用** style-fusion（它给出方向，不是执行工具）
- prompt-engineer **不调用** style-fusion（风格参数来自 creative-director 的 A1 简报）
- vfx-supervisor **不调用** prompt-engineer（它是审查者，不是执行者）

---

## 快速参考

### 查风格融合配方
```bash
python3 ~/.claude/skills/style-fusion/fusion.py B2 A3 --platform all
```

### 查已有矩阵（B×A 20个融合）
```
skills/style-fusion/SKILL.md  —— 融合矩阵总览
skills/style-fusion/style-database.json —— 原始参数数据
```

### 查平台格式规范
```
skills/video-prompt-schema/SKILL.md —— Schema 格式
skills/prompt-matrix/SKILL.md —— 平台参数
skills/video-prompt-writer/SKILL.md —— 视觉序列描述法
```

---

## 更新日志

| 日期 | 更新内容 |
|------|---------|
| 2026-04-11 | 初始创建，统一 style-fusion / video-prompt-schema / prompt-matrix 关系 |
