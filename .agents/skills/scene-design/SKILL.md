---
name: scene-design
description: Use when designing, revising, diagnosing, or prompting AI-video scenes, 场景设计, 场景板, 环境设计, 空间动线, 建筑空间, 光影色彩, 场景锚点, @场景名, scene continuity, or scene drift in storyboard/image/video workflows.
---

# Scene Design Runtime

> 多参宗白梦客出品。禁止任何盗卖行为。

This is the lean runtime entry for scene design. The full manual remains available as on-demand knowledge, but the default path should produce a usable scene packet fast.

Core principle: scene is not background. Scene is the physical container of worldview, emotion, blocking, and story consequence.

## Output Contract

For most tasks, produce a compact scene packet:

| Field | Answer |
| --- | --- |
| Scene tag | `@scene-name` |
| Narrative task |  |
| World rule / pressure |  |
| Space type |  |
| Layout / zones |  |
| Entrance / exit |  |
| Character activity zone |  |
| Fixed anchors |  |
| Narrative props |  |
| Light direction / source |  |
| Color / material logic |  |
| Camera opportunities |  |
| Before / after continuity |  |
| Forbidden drift |  |

If the user asks for a prompt, include a prompt-ready scene anchor block after the packet.

## Runtime Flow

1. Define the narrative task.
   - Establish world, reveal character, establish relationship, create tension, release emotion, mark a turn, or close a theme.

2. Translate task into space.
   - What layout, height, distance, entry, exit, obstacle, or empty area makes the task physical?
   - A scene must affect action, not only mood.

3. Choose actor zones.
   - Where does the character enter?
   - Where can they act?
   - Where do they fail, hide, collide, or land?
   - What stays fixed so movement reads?

4. Add narrative objects.
   - Use 1-3 props, marks, or traces that reveal world, habit, danger, relationship, or change.
   - A prop should be able to cause or clarify an action.

5. Lock light, color, and material.
   - Light directs attention and emotion.
   - Color sets first emotional read.
   - Material tells the world rule through texture and use.

6. Handoff to storyboard or AI video.
   - Reduce the scene to stable anchors.
   - Name what must not change.
   - Use `@scene-name` consistently across storyboard and prompts.

## Narrative Task Map

| Task | Space Need | Visual Direction |
| --- | --- | --- |
| Establish world | Daily logic plus one unfamiliar rule | readable environment, rule-bearing objects |
| Reveal character | private space or personal traces | habits, missing objects, abnormal details |
| Establish relationship | distance, height, entry control | seating, thresholds, center ownership |
| Create tension | unstable detail or coming pressure | blocked exits, hard light, compressed space |
| Release emotion | empty or open space | breath, contrast, softened light |
| Mark turn | familiar scene changed | one changed detail, altered light or order |
| Close theme | returning object or place | visual callback, simplified final image |

## Scene Prompt Anchor Block

Use this when handing to image or video models:

```text
[@SceneTag], [space type and layout], [fixed anchor], [actor activity zone], [narrative prop], [light source/direction], [color/material rule].
Keep consistent: [3-5 anchors].
Avoid: [forbidden drift].
```

For multi-shot scenes, repeat the `@SceneTag`, fixed anchor, and activity zone before changing camera language.

## Space-To-Action Checks

- Does the scene create a consequence for the character?
- Is there a clear entry, exit, and activity zone?
- Is the most important action staged in the clearest light or silhouette?
- Can the model preserve the setting with 3-5 anchors?
- Does a prop or mark reveal story without dialogue?
- Does the scene say too much, or leave useful space?
- Does it connect to the previous and next scene?

## Deep References

Read `references/full-manual.md` only when needed. Search these section names:

| Need | Search / Section |
| --- | --- |
| Full original scene manual | `references/full-manual.md` |
| Scene card format | `场景板标准规范` |
| Narrative task diagnosis | `场景诊断能力`, `叙事任务分类` |
| Scene tags and prompt naming | `分镜命名与场景锚定规则` |
| Architecture styles | `建筑风格`, `建筑构成法则`, `空间序列设计` |
| Interior realism | `室内场景设计规范` |
| Depth and focus | `景深系统`, `三层景深` |
| Movement and camera | `空间动线与机位关系`, `镜头语言` |
| Weather / atmosphere | `天气/大气系统` |
| Lighting | `场景光影系统`, `建筑与光的关系` |
| Color | `色彩系统`, `七情与场景视觉参数` |
| Environmental storytelling | `环境叙事` |
| Multi-scene flow | `场景串联`, `多场景协作` |
| AI generation workflow | `AI生成工作流` |

## Animation-Studio Handoff

When used inside `animation-studio`, return the compact scene packet and prompt anchors. Let `animation-studio` decide story structure, character packet, shot timing, and model segmentation.
