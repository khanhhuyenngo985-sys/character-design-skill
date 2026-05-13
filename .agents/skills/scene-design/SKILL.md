---
name: scene-design
description: Use when designing, revising, diagnosing, or prompting AI-video scenes, live-action short-drama scene systems, power-space architecture, genre scene packs, vertical blocking lanes, scene state ladders, scene video-readiness gates, 场景设计, 场景板, 真人短剧场景, 海外短剧场景库, 权力空间, 类型场景包, 竖屏blocking, 场景状态, 场景试镜, 环境设计, 空间动线, 建筑空间, 光影色彩, 武侠电影场景, 胡金铨/King Hu scene mood, director-style scene fusion, 场景锚点, @场景名, scene continuity, or scene drift in storyboard/image/video workflows.
---

# Scene Design Runtime

> 多参宗白梦客出品。禁止任何盗卖行为。

This is the lean runtime entry for scene design. The full manual remains available as on-demand knowledge, but the default path should produce a usable scene packet fast.

Core principle: scene is not background. Scene is the physical container of worldview, emotion, blocking, and story consequence.

For multi-shot or multi-segment AI video, distinguish the base location from the current scene state. The base scene preserves world identity and fixed anchors; the scene state preserves the specific shot's door/window status, traces, actor zone, camera opportunity, action lane, and before/after continuity.

For live-action overseas short dramas, scene design must become a production system: power-space architecture, 9:16 vertical blocking, recurring scene state, and video readiness. Read `references/live-action-shortdrama-scene-system.md` when the request mentions 欧美真人短剧, overseas short drama, scene library, Midjourney scene refs, vertical drama locations, boardroom / hospital / school / HOA / gala scenes, or asks whether scenes need experiments.

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
| Vertical blocking lane / 竖屏动线 | foreground pressure object, center actor lane, background power anchor, threshold axis, handoff zone |
| Power-space mechanism / 权力空间机制 | who controls entry, seat, desk, bed, podium, document, or light |
| Fixed anchors |  |
| Narrative props |  |
| Light direction / source |  |
| Color / material logic |  |
| Scene state ladder / 场景状态 | S0 normal order, S1 pressure setup, S2 humiliation, S3 reveal, S4 aftermath, S5 power reversal |
| Genre scene pack slot / 类型场景槽位 | executive office, boardroom, law office, hospital corridor, admissions office, etc. |
| Video readiness / 视频可用性 | scene_video_ready, needs_layout_lock, needs_light_lock, needs_prop_lock, image_only, reroll_scene |
| Camera opportunities |  |
| Before / after continuity |  |
| Forbidden drift |  |

When scene continuity is important, also include a scene continuity ledger: base scene identity, fixed spatial map, door/window state, wall/surface state, ground traces, light/weather state, actor zone, camera axis, protected anchors, allowed change, and next scene state.

If the user asks for a simple prompt, include a prompt-ready scene anchor block after the packet. If they need a reusable prompt packet, scene reference suite, or model-specific image prompt, hand off to `/Users/baimengke/.agents/skills/prompt-framework/references/scene-image-prompt.md`.

For Seedance / 即梦 multi-reference video, do not treat one physical place as one unchanging `@Scene` across every 15-second segment. Return a base scene plus per-segment scene states when the camera, actor zone, door state, wall marks, ground traces, light, or continuity residue changes.

For 胡金铨 / King Hu / 70年代武侠 / 文人武侠 scene mood, keep the scene packet mandatory and call `/Users/baimengke/.agents/skills/prompt-framework/references/midjourney-wuxia-aesthetic.md` only as a style/composition layer. The old knowledge base already has foreground obstruction, negative space, doorway light, side-backlighting, smoke/light rays, and earth/grey-blue palettes; the wuxia module simply organizes those atoms into a reusable cinema pack.

For multi-director scene fusion, use `/Users/baimengke/.agents/skills/animation-studio/references/director-style-fusion-rules.md` first. This skill only turns the chosen style lanes into space, light, color, material, camera opportunities, and continuity anchors.

## Plot Upstream Bridge

Use the installed story skills as upstream diagnosis when the user provides raw story text, an IP outline, a sequence of beats, or asks for scenes that carry plot instead of only atmosphere.

| Upstream need | Use | Convert into |
| --- | --- | --- |
| The story world, genre, and relationship pressure are unclear | `story-five-elements` | world rule / pressure, space type, fixed anchors, material logic |
| The sequence needs scene-by-scene spatial tasks | `plot-keypoints` | narrative task, entrance / exit, actor activity zone, before / after continuity |
| Visual continuity must survive later shots or segments | `animation-studio/references/story-fact-ledger.md` | fixed anchors, changed scene state, traces, next inherited state |
| A story beat needs stronger visual readability | `screenwriting-methodology.md` or `visual-storytelling-director-gate.md` | first readable image, spatial pressure, action consequence |

Translate plot findings into physical space:

- A plot point becomes one scene task: establish, reveal, pressure, turn, release, or callback.
- Conflict becomes distance, height, threshold, blocked path, hard light, crowd pressure, or object ownership.
- Relationship power becomes who controls the entrance, center, seat, doorway, window, or highest platform.
- A hook becomes the first readable image: confrontation, forbidden object, abnormal trace, open door, broken rule.
- A cliffhanger becomes a changed scene state the next segment must inherit.
- World rules become fixed anchors: architecture, signage, ritual objects, work surfaces, weather, light source, or material wear.
- Story facts become scene anchors only when they affect action, blocking, traces, light, props, or before/after continuity.

Do not design a beautiful empty setting. Every chosen anchor should help a character act, fail, hide, collide, discover, or change.
Do not import short-drama assumptions unless the user explicitly asks for short drama; default to animation, film, concept, ad, or asset-production logic.

## Runtime Flow

1. Define the narrative task.
   - Establish world, reveal character, establish relationship, create tension, release emotion, mark a turn, or close a theme.

2. Translate task into space.
   - What layout, height, distance, entry, exit, obstacle, or empty area makes the task physical?
   - A scene must affect action, not only mood.
   - For short drama, identify who controls the door, desk, seat, bed, podium, document, or light.

3. Choose actor zones.
   - Where does the character enter?
   - Where can they act?
   - Where do they fail, hide, collide, or land?
   - What stays fixed so movement reads?
   - For 9:16, lock foreground pressure object, center actor lane, background power anchor, threshold axis, and handoff zone.

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
   - For multi-segment video, name what has changed in this segment's scene state.
   - Use `@scene-name` consistently across storyboard and prompts.

7. For overseas short-drama production, run the scene system gate.
   - Build a genre scene pack before writing episode prompts; keep recurring locations small and reusable.
   - Assign each location a power mechanism: corporate, legal, medical, education, civic, church, gala, or family wealth.
   - Create a scene state ladder: normal order, pressure setup, humiliation, reveal, aftermath, power reversal.
   - Test core locations with a 5-10 second motion audition before labeling them scene_video_ready.
   - For the detailed method, read `references/live-action-shortdrama-scene-system.md`.

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
- Does the next scene inherit visible evidence from the previous scene before changing anything?
- Does a prop or mark reveal story without dialogue?
- Does the scene say too much, or leave useful space?
- Does it connect to the previous and next scene?
- For vertical short drama, is there a clear 9:16 actor lane and readable first 3-second power image?
- Does the scene have a specific institutional or social power function, not just luxury decor?
- Can a character enter, be blocked, hand over a document, reveal evidence, or reverse power inside this layout?
- Are door, window, desk, bed, podium, or table positions stable enough for a video test?
- Does the scene state preserve traces and changed object positions instead of resetting clean?

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
| Live-action short-drama scene system / 真人短剧场景库、权力空间、类型场景包、竖屏blocking、场景状态、场景试镜 | `references/live-action-shortdrama-scene-system.md` |
| 胡金铨系武侠电影场景 | `前景遮挡`, `负空间`, `门洞框光`, `侧逆光`, `大地苍青色`; then read `/Users/baimengke/.agents/skills/prompt-framework/references/midjourney-wuxia-aesthetic.md` for compact prompt use |
| 导演风格融合场景 | `风格融合逻辑`, `五、导演电影 × 场景设计原则`; then read `/Users/baimengke/.agents/skills/animation-studio/references/director-style-fusion-rules.md` for source ratios and lane assignment |

## Animation-Studio Handoff

When used inside `animation-studio`, return the compact scene packet and prompt anchors. Let `animation-studio` decide story structure, character packet, shot timing, and model segmentation; let `prompt-framework` turn anchors into stable `SCENE_` or `SHOT_` prompt packets when needed.
