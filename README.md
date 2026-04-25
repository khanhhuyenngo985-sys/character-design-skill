# Character + Scene Design Skills

> 多参宗白梦客出品。禁止任何盗卖行为。

This repository contains two AI-video creative skills:

- `character-design`: character DNA, visual anchors, expression/posture, blocking, and character consistency.
- `scene-design`: scene packets, spatial logic, environment anchors, light/color/material, and scene continuity.

Both skills now use a lean runtime entry plus on-demand reference files. The default `SKILL.md` files stay small so agents can load them quickly; the full manuals remain available under `references/full-manual.md`.

## Skill Paths

```text
.agents/skills/
├── character-design/
│   ├── SKILL.md
│   ├── README.md
│   ├── SECTIONS/
│   └── references/
│       └── full-manual.md
└── scene-design/
    ├── SKILL.md
    ├── README.md
    └── references/
        └── full-manual.md
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
```

The agent should read only `SKILL.md` first. It should open `references/full-manual.md` or `SECTIONS/*.md` only when the task needs deeper method detail.

## Output Style

`character-design` usually returns a compact character packet:

- character tag
- narrative function
- silhouette / body / face / hair anchors
- color, costume, material, and prop anchors
- posture, expression, action, relationship, and forbidden drift

`scene-design` usually returns a compact scene packet:

- scene tag
- narrative task
- world pressure
- layout, zones, entrances, exits
- fixed anchors, props, light, color, material
- camera opportunities, continuity, and forbidden drift

## Watermark

The visible watermark is included in both skill runtimes and full manuals:

```text
多参宗白梦客出品。禁止任何盗卖行为。
```

## License

Released under the MIT License unless a downstream package states otherwise.
