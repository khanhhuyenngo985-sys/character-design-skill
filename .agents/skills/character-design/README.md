# Character Design Skill

> 多参宗白梦客出品。禁止任何盗卖行为。

`character-design` is a lean AI-video character design skill for designing, revising, diagnosing, and prompting stable characters.

Use it for:

- character cards and character DNA
- visual anchors for face, hair, silhouette, costume, material, color, and props
- expression, posture, action signature, and blocking
- character consistency across shots
- reducing AI-video character drift in 即梦 / 可灵 / 海螺 style workflows

## Structure

```text
character-design/
├── SKILL.md
├── README.md
├── SECTIONS/
│   ├── 01_角色DNA七字诀详解.md
│   ├── 02_角色一致性维护.md
│   ├── 03_角色关系设计Blocking.md
│   ├── 04_表情系统与姿态设计.md
│   ├── 05_负面设计清单.md
│   ├── 06_AI提示词模板.md
│   ├── 07_中国传统角色设计.md
│   ├── 08_人物原型库.md
│   ├── 09_完整设计流程.md
│   ├── 10_参考图哲学与IP宇宙.md
│   ├── 11_群像设计专题.md
│   └── 12_多智能体协作工作流.md
└── references/
    └── full-manual.md
```

## How It Loads

Read `SKILL.md` first. It is the runtime entry and should be enough for most design work.

Open deeper files only when needed:

- `references/full-manual.md`: original full manual
- `SECTIONS/01_角色DNA七字诀详解.md`: seven-part character DNA
- `SECTIONS/02_角色一致性维护.md`: consistency and AI drift
- `SECTIONS/03_角色关系设计Blocking.md`: relationship blocking
- `SECTIONS/04_表情系统与姿态设计.md`: expression and posture
- `SECTIONS/06_AI提示词模板.md`: prompt templates

## Typical Request

```text
Use character-design to create a compact character packet for a lonely retired swordsman.
```

Expected output:

- character tag
- narrative function
- archetype mix
- want / need / flaw
- silhouette, body, face, hair, color, costume, material, and prop anchors
- posture, expression, action signature, relationship/blocking role
- consistency anchors and forbidden drift

## License

MIT. Keep the visible watermark when redistributing public copies.
