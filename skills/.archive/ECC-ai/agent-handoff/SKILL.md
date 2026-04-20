---
技能版本: v1.0
创建日期: 2026-04-05
更新日期: 2026-04-05
使用次数: 0
最后使用项目: —
版本历史:
  - v1.0 (2026-04-05): 初始创建，基于OpenAI Agents SDK Handoff模式
---

# Agent Handoff 契约

## 功能

定义白梦客团队中各Agent之间的输入/输出契约，确保协作流程标准化。

## 为什么需要Handoff契约

**当前问题：**
- Agent之间靠"文档传递"容易信息丢失
- 没有明确的"完成标准"
- 后续Agent不知道前面产出了什么

**解决方案：**
- 每个Agent有明确的input契约（需要什么）
- 每个Agent有明确的output契约（产出什么）
- Handoff时有质量检查点

## Agent工作流

```
client-intake (接收需求)
    ↓ output: 原始需求
creative-director (创意方向)
    ↓ output: A1 创作简报
    ↓ output: skill_routing 决策
screenwriter (剧本)
    ↓ output: A3 结构大纲
    ↓ output: A6 剧本
director (分镜)
    ↓ output: A4 场景拆解
    ↓ output: A5 分镜脚本
vfx-supervisor (提示词生成)
    ↓ output: AI提示词
editor (剪辑)
    ↓ output: 剪辑方案
internal-review-lead (内部审查)
    ↓ output: 审查意见
client-review-lead (客户审查)
    ↓ output: 客户确认
```

## 工件定义 (Artifacts)

### A1: 创作简报

```json
{
  "artifact_id": "A1",
  "name": "创作简报",
  "producer": "creative-director",
  "consumer": "screenwriter, director",
  "fields": {
    "project_name": "string",
    "client": "string",
    "industry": "string",
    "style_line": "高定线 | 通用线",
    "duration": "number (秒)",
    "key_message": "string",
    "target_audience": "string",
    "creative_brief": "string (一句话描述核心创意)",
    "visual_direction": "string",
    "tone_of_voice": "string",
    "deliverables": ["string"],
    "constraints": ["string"],
    "references": ["string (案例/参考链接)"]
  },
  "quality_gate": {
    "required_fields_complete": "boolean",
    "creative_brief_clear": "boolean",
    "target_audience_defined": "boolean"
  }
}
```

### A2: 人物卡

```json
{
  "artifact_id": "A2",
  "name": "人物卡",
  "producer": "screenwriter",
  "consumer": "director",
  "fields": {
    "characters": [{
      "name": "string",
      "role": "string",
      "appearance": "string",
      "personality": "string",
      "motivation": "string",
      "visual_notes": "string"
    }]
  },
  "quality_gate": {
    "all_characters_have_visual_notes": "boolean"
  }
}
```

### A3: 结构大纲

```json
{
  "artifact_id": "A3",
  "name": "结构大纲",
  "producer": "screenwriter",
  "consumer": "director",
  "fields": {
    "act_structure": {
      "act1": { "start": "string", "end": "string", "duration": "string" },
      "act2": { "start": "string", "end": "string", "duration": "string" },
      "act3": { "start": "string", "end": "string", "duration": "string" }
    },
    "emotional_arc": "string",
    "key_moments": ["string"],
    "pacing_notes": "string"
  },
  "quality_gate": {
    "emotional_arc_defined": "boolean",
    "key_moments_listed": "boolean"
  }
}
```

### A4: 场景拆解

```json
{
  "artifact_id": "A4",
  "name": "场景拆解",
  "producer": "director",
  "consumer": "screenwriter, vfx-supervisor",
  "fields": {
    "scenes": [{
      "scene_id": "string",
      "location": "string",
      "time_of_day": "string",
      "description": "string",
      "duration": "string",
      "plot_rhythm": "loose | medium | tense",
      "emotion_rhythm": "light | medium | heavy",
      "mini_dramatic_action": "string",
      "characters_present": ["string"]
    }]
  },
  "quality_gate": {
    "all_scenes_have_duration": "boolean",
    "rhythm_annotated": "boolean"
  }
}
```

### A5: 分镜脚本

```json
{
  "artifact_id": "A5",
  "name": "分镜脚本",
  "producer": "director",
  "consumer": "vfx-supervisor, editor",
  "fields": {
    "shots": [{
      "shot_id": "string",
      "scene_ref": "string",
      "timestamp": "[mm:ss-mm:ss]",
      "shot_type": "string",
      "camera": {
        "movement": "string",
        "angle": "string",
        "distance": "string"
      },
      "subject": "string",
      "action": "string",
      "dialogue": "string (如有)",
      "music_notes": "string",
      "notes": "string"
    }],
    "color_direction": "string",
    "overall_pacing": "string"
  },
  "quality_gate": {
    "timestamps_correct": "boolean",
    "camera_instructions_complete": "boolean"
  }
}
```

### A6: 剧本

```json
{
  "artifact_id": "A6",
  "name": "剧本",
  "producer": "screenwriter",
  "consumer": "director",
  "fields": {
    "title": "string",
    "writer": "string",
    "date": "string",
    "scenes": [{
      "scene_heading": "string",
      "scene_description": "string",
      "action": "string",
      "dialogue": [{
        "character": "string",
        "line": "string",
        "parenthetical": "string (可选)"
      }]
    }]
  },
  "quality_gate": {
    "humanize_dialogue_passed": "boolean",
    "scene_headings_correct": "boolean"
  }
}
```

### AI提示词 (VFX Output)

```json
{
  "artifact_id": "PROMPT",
  "name": "AI视频提示词",
  "producer": "vfx-supervisor",
  "consumer": "editor",
  "fields": {
    "platform": "seedance | vidu | hairui",
    "scene_prompts": [{
      "timestamp": "string",
      "prompt_text": "string (中文/英文)",
      "negative_prompt": "string (可选)",
      "seed": "number (可选)"
    }],
    "style_reference": "string",
    "technical_specs": {
      "resolution": "string",
      "fps": "number",
      "duration": "string"
    }
  },
  "quality_gate": {
    "platform_language_correct": "boolean",
    "timestamps_match_A5": "boolean"
  }
}
```

## Handoff检查清单

### creative-director → screenwriter

```
检查项：
[ ] A1 所有必填字段已完成
[ ] creative_brief 清晰可执行
[ ] target_audience 已定义
[ ] references 有实质内容
```

### screenwriter → director

```
检查项：
[ ] A2 人物卡完成
[ ] A3 结构大纲完成
[ ] A6 剧本初稿完成
[ ] humanize-dialogue 已调用（台词已去AI味）
```

### director → vfx-supervisor

```
检查项：
[ ] A4 场景拆解完成
[ ] A5 分镜脚本完成
[ ] 情绪曲线视觉映射已对照
[ ] 质量门全部通过
```

### vfx-supervisor → editor

```
检查项：
[ ] AI提示词已生成
[ ] prompt-schema 质量检查通过
[ ] 各平台格式正确
[ ] 负向提示词已设置
```

## 错误处理

### 工件不完整

如果后续Agent发现前序工件不完整：
1. 标记具体缺失字段
2. 返回给前序Agent补充
3. 不擅自填补空白

### 质量门未通过

如果质量门检查失败：
1. 列出具体未通过项
2. 说明不通过原因
3. 返回前序Agent重做

## 使用方法

当需要交接工作时：

1. **读取前序Artifact** - 确认工件存在且完整
2. **对照质量门** - 检查是否满足交接标准
3. **如有缺失** - 返回前序Agent补充
4. **如通过** - 开始自己的创作工作
5. **产出新Artifact** - 供后续Agent使用

## 案例

### 正常Handoff

```
director 完成 A5 分镜脚本后：

检查 A5 质量门：
✅ timestamps_correct: true
✅ camera_instructions_complete: true

Handoff 给 vfx-supervisor：
"分镜脚本 A5 已完成，质量门通过。
请基于 A5 和 A4 生成 AI 提示词。
目标平台：seedance"
```

### 质量门失败

```
screenwriter 提交 A6 剧本后，director 发现问题：

❌ humanize_dialogue_passed: false

返回 screenwriter：
"A6 剧本质量门未通过：
1. 对话仍有AI味，请用 humanize-dialogue 重新处理
2. 第三幕节奏拖沓，建议压缩

请修正后重新提交。"
```
