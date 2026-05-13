# Character + Scene Design Skills

> 多参宗白梦客出品。禁止任何盗卖行为。

This repository contains two production-oriented AI-video creative skills:

- `character-design`: character DNA, live-action short-drama casting assets, bone/face anchors, relationship matrices, genre cast packs, wardrobe states, and video-readiness gates.
- `scene-design`: scene packets, power-space architecture, vertical 9:16 blocking lanes, genre scene packs, scene state ladders, and scene video-readiness gates.

Both skills now use a lean runtime entry plus on-demand reference files. The default `SKILL.md` files stay small so agents can load them quickly; the full manuals remain available under `references/full-manual.md`.

## What's New

- Live-action overseas short-drama production workflow.
- Western-market multicultural casting gates for MJ character asset libraries.
- Bone / face-structure anchors to reduce generic beauty and ethnicity drift.
- Institutional power design for trust, probate, DA, insurance, hospital, admissions, HOA, zoning, charity, and gala scenes.
- Relationship matrices, genre cast packs, wardrobe state ladders, and video-readiness labels for characters.
- Power-space architecture, vertical blocking lanes, scene state ladders, and scene video-readiness labels for locations.

## Skill Paths

```text
.agents/skills/
├── character-design/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── README.md
│   ├── SECTIONS/
│   └── references/
│       ├── full-manual.md
│       ├── bone-face-structure-layer.md
│       ├── frontloaded-character-assets.md
│       ├── live-action-shortdrama-casting-assets.md
│       └── shortdrama-character-production-system.md
└── scene-design/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── README.md
    └── references/
        ├── full-manual.md
        └── live-action-shortdrama-scene-system.md
```

## Install

Copy the skill folders into your agent skills directory:

```bash
mkdir -p ~/.agents/skills
cp -R .agents/skills/character-design ~/.agents/skills/
cp -R .agents/skills/scene-design ~/.agents/skills/
```

For Claude Code-style layouts, copy them into your Claude skills directory instead:

```bash
mkdir -p ~/.claude/skills
cp -R .agents/skills/character-design ~/.claude/skills/
cp -R .agents/skills/scene-design ~/.claude/skills/
```

## Usage

Ask naturally:

```text
Use character-design to create a stable AI-video character packet.
Use scene-design to create a scene packet for a night market chase.
帮我用 character-design 设计一个反派角色。
帮我用 scene-design 设计一个可以连续出镜的场景。
帮我做一组欧美真人短剧人物库，要求 MJ casting，全身，男女老少和多族裔都要有。
帮我做 CEO revenge romance 的场景包，要有 boardroom、penthouse、hospital、gala 和竖屏 blocking。
```

The agent should read only `SKILL.md` first. It should open `references/full-manual.md` or `SECTIONS/*.md` only when the task needs deeper method detail.

## Output Style

`character-design` usually returns a compact character packet:

- character tag
- narrative function
- silhouette / body / bone / face / hair anchors
- color, costume, material, and prop anchors
- posture, expression, action, relationship, and forbidden drift
- relationship edges, genre cast-pack slot, wardrobe state ladder, and video-readiness label when producing short-drama systems

`scene-design` usually returns a compact scene packet:

- scene tag
- narrative task
- world pressure
- layout, zones, entrances, exits
- power-space mechanism and vertical blocking lane
- fixed anchors, props, light, color, material
- camera opportunities, continuity, and forbidden drift
- scene state ladder, genre scene-pack slot, and scene video-readiness label when producing short-drama systems

## Short-Drama Production Flow

```text
Character library
→ genre cast pack
→ relationship matrix
→ wardrobe state ladder
→ character motion audition
→ video-ready episode prompts

Scene library
→ genre scene pack
→ power-space layout
→ vertical blocking lane
→ scene state ladder
→ 5-10s scene motion test
→ scene-video-ready episode prompts
```

## Git Workflow

Use feature branches for updates and merge into `main` through pull requests. The `main` branch should be protected from force pushes and deletion.

## Watermark

The visible watermark is included in both skill runtimes and full manuals:

```text
多参宗白梦客出品。禁止任何盗卖行为。
```

## License

Released under the MIT License unless a downstream package states otherwise.
