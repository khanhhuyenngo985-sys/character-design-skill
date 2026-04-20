---
name: mempalace
description: AI跨会话记忆系统，96.6% LongMemEval得分，自动保存关键上下文到记忆宫殿。触发词：「记住这个」「保存到记忆」「调取记忆」「mempalace」「跨会话记忆」。
---

# MemPalace

AI 记忆系统 — 跨会话记住一切。

## 安装状态

- Python 3.11 环境已配置
- Palace 目录：`~/.mempalace`
- MCP 服务器：`python3.11 -m mempalace.mcp_server`

## MCP 服务器配置

```bash
claude mcp add mempalace -- python3.11 -m mempalace.mcp_server
```

## 核心概念

| 概念 | 说明 |
|------|------|
| **Wing** | 项目或人（最大分类） |
| **Room** | 主题（ wing 内的细分） |
| **Closet** | 摘要（指向原始内容的指针） |
| **Drawer** | 原始内容（完整对话存档） |

## 记忆层级

| 层级 | 内容 | Token数 |
|------|------|---------|
| L0 | 身份（AI是谁） | ~50 |
| L1 | 关键事实（团队、项目、偏好） | ~120 |
| L2 | 房间回忆（当前项目、最近会话） | 按需 |
| L3 | 深度搜索（语义搜索所有closets） | 按需 |

## 可用工具（19个）

**Palace 读取**
- `mempalace_status` — 宫殿概览 + AAAK规范
- `mempalace_list_wings` — wing列表及数量
- `mempalace_list_rooms` — wing内的房间
- `mempalace_get_taxonomy` — 完整分类树
- `mempalace_search` — 语义搜索
- `mempalace_get_aaak_spec` — AAAK方言参考

**Palace 写入**
- `mempalace_add_drawer` — 添加原始内容
- `mempalace_delete_drawer` — 删除内容

**知识图谱**
- `mempalace_kg_query` — 实体关系查询
- `mempalace_kg_add` — 添加事实
- `mempalace_kg_timeline` — 时间线

## 命令行

```bash
# 初始化
mempalace init ~/.mempalace

# 挖掘数据
mempalace mine ~/projects/myapp                    # 项目文件
mempalace mine ~/chats/ --mode convos              # 对话记录

# 搜索
mempalace search "auth决策"                         # 搜索全部
mempalace search "query" --wing myapp              # 指定wing搜索

# 状态
mempalace status                                    # 宫殿概览
```

## Auto-Save Hooks

添加到 `settings.json` 的 `hooks` 部分：

```json
"Stop": [
  {
    "description": "MemPalace auto-save",
    "hooks": [{"command": "bash /Users/baimengke/.claude/skills/mempalace/hooks/mempal_save_hook.sh", "type": "command"}],
    "matcher": "*"
  }
]
```

## AAAK 方言（实验性）

AAAK 是一种缩写语言，用于压缩重复实体。当前得分低于原始模式（84.2% vs 96.6%），存储默认使用原始模式。

## 基准测试

| 模式 | LongMemEval R@5 | API调用 |
|------|----------------|---------|
| **原始模式** | **96.6%** | 零 |
| 混合+Haiku重排 | 100% | ~500 |

96.6% 是目前开源最高分，无需API密钥。

## 故障排除

```bash
# 修复
python3.11 -m mempalace repair

# 检查状态
python3.11 -m mempalace status
```
