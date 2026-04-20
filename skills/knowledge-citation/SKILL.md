---
name: knowledge-citation
description: Use when generating any response that involves creative work, filmmaking, advertising, or knowledge-based queries. Checks if knowledge base was properly cited.
---

# Knowledge Citation Skill

## Overview

强制知识库引用检查机制。确保 Agent 回答前尝试引用知识库，并在回答中显式声明引用情况。

## When to Use

每个 Agent 回答前必须调用此 skill：
- 涉及创作方向讨论
- 涉及分镜/脚本/视觉设计
- 涉及行业知识引用
- 任何需要专业知识支撑的回答

## Citation Flow

```
1. 理解问题 → 判断是否需要知识库
2. 搜索相关知识库文件
3. 如有相关内容 → 显式引用后回答
4. 如无相关内容 → 标记"⚠️ 未引用知识库"后回答
```

## Citation Format

### 有相关内容时

回答开头必须包含：

```
已引用知识库：
- /path/to/file1.md
  → 具体引用内容（如适用）
- /path/to/file2.md
  → 具体引用内容

[正式回答...]
```

### 无相关内容时

回答开头必须包含：

```
⚠️ 未引用知识库（知识库无相关内容 / 本次回答基于通用经验）

[正式回答...]
```

## File Validation

引用声明后，验证文件是否存在：

```python
from pathlib import Path

def validate_citations(cited_files: list) -> dict:
    invalid = []
    for f in cited_files:
        if not Path(f).expanduser().exists():
            invalid.append(f)
    return {"valid": len(invalid) == 0, "invalid_files": invalid}
```

## Citation Logging

每次对话的引用情况记录到：

```
/tmp/knowledge-evolution/citation-log.jsonl
```

```json
{"timestamp":"2026-03-31T14:00","agent":"director","scene":"complex","citation":["/path/to/file.md"],"kb_content_found":true,"status":"valid"}
```

## Scene Types

| 场景类型 | 定义 | 示例 | 引用要求 |
|----------|------|------|----------|
| **简单场景** | 方向讨论、概念咨询 | "这个广告方向怎么样" | 引用文件即可 |
| **复杂场景** | 分镜设计、脚本写作 | "设计这个场景的分镜" | 引用具体观点 |

## Quick Reference

| 状态 | 含义 | 后续动作 |
|------|------|----------|
| ✅ 引用有效 | 文件存在、内容相关 | 正常输出 |
| ⚠️ 引用存疑 | 文件路径错误或内容不相关 | 修正后输出 |
| ⚠️ 未引用 | 无引用声明 | 标记后输出 |

## Citation Block Pattern

响应中必须包含以下标记之一：

**引用声明开头：**
```
已引用知识库：
```

**未引用声明开头：**
```
⚠️ 未引用知识库
```

如果响应中没有这两个标记之一，说明引用检查未执行。

---

*此 skill 由知识进化系统自动晋升机制驱动*
