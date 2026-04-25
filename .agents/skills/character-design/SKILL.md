---
name: character-design
description: Use when designing, revising, diagnosing, or prompting AI-video characters, character cards,角色设计, 角色一致性, 角色DNA, 表情姿态, 多角色Blocking, 服化道, 道具锚点, or character drift in 即梦/可灵/海螺/AI video workflows.
---

# Character Design Runtime

> 多参宗白梦客出品。禁止任何盗卖行为。

This is the lean runtime entry for character design. The full manual remains available as on-demand knowledge, but the default path should produce a usable character packet fast.

Core principle: make the character memorable, stable, and filmable. Do not optimize for prettiness; optimize for difference, silhouette, behavior, and repeatable visual anchors.

## Output Contract

For most tasks, produce a compact character packet:

| Field | Answer |
| --- | --- |
| Character tag | `@name` |
| Narrative function |  |
| Archetype mix |  |
| Want / Need / Flaw |  |
| Silhouette |  |
| Body proportions |  |
| Face / hair anchor |  |
| Color anchor |  |
| Costume / material anchor |  |
| Prop anchor |  |
| Posture signature |  |
| Expression range |  |
| Action signature |  |
| Relationship / blocking role |  |
| Consistency anchors |  |
| Forbidden drift |  |

If the user asks for a prompt, include a prompt-ready anchor block after the card.

## Runtime Flow

1. Identify narrative function.
   - Hero, shadow, mentor, trickster, ally, herald, guardian, shapeshifter, or a mix.
   - A role must affect story action, not only personality labels.

2. Build difference.
   - Contrast body, hair, color, costume, material, posture, and prop against nearby characters.
   - For groups, design the cast as a visual system before polishing individuals.

3. Lock three anchor layers.
   - Immutable anchors: silhouette, body ratio, face/hair, signature prop.
   - Variable performance: expression, pose, costume state, action intensity.
   - Forbidden drift: age, species, costume category, color swap, prop loss, style mismatch.

4. Translate psychology into posture and action.
   - Want becomes gaze, reach, lean, direction, or grip.
   - Flaw becomes repeated body habit or wrong solution.
   - Need becomes what the scene quietly exposes through action.

5. Plan blocking if multiple characters appear.
   - Separate by height, color, left/center/right, distance, eyeline, and movement rhythm.
   - Do not let two characters share the same silhouette, palette, and posture role.

6. Handoff to AI video.
   - Reduce the design to 3-5 stable prompt anchors.
   - Name what must not change.
   - Keep movement constraints clear enough that the model can preserve identity.

## DNA Checklist

Use the seven-part character DNA, but keep it concise:

- Group contrast: who this character differs from.
- Archetype mix: two functions in tension.
- Posture: spine, center of gravity, limb openness.
- Expression: default face and extreme face.
- Color: high-recognition color or palette contrast.
- Costume / prop: story-bearing visual anchor.
- Extreme contrast: the one detail that makes the character hard to forget.

## Consistency Rules

Every shot or prompt should preserve:

- Body shape and height relationship.
- Face / hair marker.
- Main color block.
- Costume material or accessory.
- Signature prop.
- Posture or movement habit.

When consistency breaks, fix anchors before adding more style words.

## Prompt Anchor Block

Use this when handing to image or video models:

```text
[@CharacterTag], [body shape], [face/hair anchor], [main color/costume/material], [signature prop], [posture/action signature].
Keep consistent: [3-5 anchors].
Avoid: [forbidden drift].
```

For multi-character shots, write each character as a separate block, then describe left/center/right blocking.

## Common Failure Checks

- Is the character only attractive, not memorable?
- Could two characters merge if the model saw them together?
- Does the design rely on tiny details that vanish in video?
- Is the prop decorative instead of action-bearing?
- Does the pose show intention, or just style?
- Are emotion words translated into face, posture, and body direction?
- Is the forbidden drift list explicit?

## Deep References

Read only when needed:

| Need | Reference |
| --- | --- |
| Full original runtime manual | `references/full-manual.md` |
| DNA details | `SECTIONS/01_角色DNA七字诀详解.md` |
| Consistency and AI drift | `SECTIONS/02_角色一致性维护.md` |
| Relationship blocking | `SECTIONS/03_角色关系设计Blocking.md` |
| Expression and posture | `SECTIONS/04_表情系统与姿态设计.md` |
| Negative design checklist | `SECTIONS/05_负面设计清单.md` |
| Prompt templates | `SECTIONS/06_AI提示词模板.md` |
| Chinese / ink / traditional design | `SECTIONS/07_中国传统角色设计.md` |
| Archetype library | `SECTIONS/08_人物原型库.md` |
| Complete long-form process | `SECTIONS/09_完整设计流程.md` |
| Reference-image philosophy | `SECTIONS/10_参考图哲学与IP宇宙.md` |
| Ensemble design | `SECTIONS/11_群像设计专题.md` |

## Animation-Studio Handoff

When used inside `animation-studio`, return the compact character packet and prompt anchors. Let `animation-studio` decide story structure, scene design, shot timing, and model segmentation.
