# Scene Design Skill

> 多参宗白梦客出品。禁止任何盗卖行为。

`scene-design` is a lean AI-video scene design skill for designing, revising, diagnosing, and prompting stable scenes.

Use it for:

- scene cards and environment packets
- spatial logic, actor zones, entrances, exits, and blocking support
- fixed scene anchors for AI-video continuity
- light, color, material, atmosphere, and camera opportunities
- reducing scene drift across storyboard, image, and video workflows

## Structure

```text
scene-design/
├── SKILL.md
├── README.md
└── references/
    └── full-manual.md
```

## How It Loads

Read `SKILL.md` first. It is the runtime entry and should be enough for most scene design work.

Open `references/full-manual.md` only when the task needs deeper method detail, such as architecture style, space sequence, lighting systems, environmental storytelling, or multi-scene continuity.

## Typical Request

```text
Use scene-design to create a reusable scene packet for a rainy night market chase.
```

Expected output:

- scene tag
- narrative task
- world rule or pressure
- space type, layout, zones, entrance, and exit
- fixed anchors and narrative props
- light direction, color, material, and camera opportunities
- before/after continuity and forbidden drift

## License

MIT. Keep the visible watermark when redistributing public copies.
