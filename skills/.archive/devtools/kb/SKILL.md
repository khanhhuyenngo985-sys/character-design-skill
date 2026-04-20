---
name: kb
description: 知识库管理技能，沉淀、检索、更新白梦客知识库内容。触发词：「知识库」「查一下」「入库」「沉淀」。
---

# Knowledge Base Management Skill

## Overview

Manages the ECC Wiki and Baimengke Creative Wiki knowledge bases.

## Wiki Locations

- **ECC Wiki**: `~/.claude/wiki/`
- **Creative Wiki**: `~/Documents/白梦客知识库/wiki/`

## Operations

### Ingest

Add new knowledge to the wiki:

```
When: New agent/skill/command created, user provides feedback, best practice discovered
Steps:
1. Analyze source
2. Extract knowledge (functionality, use cases, config, best practices)
3. Create/update wiki page
4. Update index.md
5. Record in log.md
```

### Query

Search the knowledge base:

```
When: User asks about ECC config or creative work
Steps:
1. Parse intent (ECC vs Creative)
2. Determine scope
3. Search index.md and relevant pages
4. Synthesize answer
```

### Lint

Health check the wiki:

```
When: Weekly or when issues suspected
Checks:
1. Orphan pages
2. Broken links
3. Consistency
4. Completeness
5. Staleness
```

## Quick Commands

| Command | Function |
|---------|----------|
| /kb ingest | Add new knowledge |
| /kb query | Search knowledge |
| /kb lint | Health check |
| /kb log | View changelog |
