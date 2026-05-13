# Character + Scene Design Skills

> 多参宗白梦客出品。禁止任何盗卖行为。

这是一个面向 **海外 / 欧美真人竖屏短剧** 的角色设计与场景设计技能包。它不是单纯做“好看的图”，而是把短剧前期需要的 **人物资产、权力关系、服装状态、可复用场景、竖屏动线、MJ/视频提示词** 统一成可落地的生产流程。

## 一眼怎么用

如果你只想马上开工，直接复制下面的请求：

```text
帮我用 character-design 做一组欧美真人短剧角色库：100个角色，男女老少、多族裔、多肤色、主角/反派/亲属/律师/医生/警察/富豪/底层角色都要覆盖，输出 MJ 可直接出图的 casting prompt。

帮我用 scene-design 做一个欧美真人短剧场景包：豪门继承权 + 复仇爱情类型，包含 boardroom、penthouse、hospital、law office、gala、mansion、police station，每个场景都要有权力位置、竖屏 blocking 和可复用提示词。

帮我把角色和场景合并成一集短剧的前期资产方案：谁在什么场景里占上风，服装状态如何变化，哪些画面适合做封面，哪些镜头先做 5-10 秒视频试镜。
```

## 两个技能分别管什么

| 技能 | 主要用途 | 最适合的产出 |
|------|----------|--------------|
| `character-design` | 真人短剧人物库、角色卡、骨相锚点、关系矩阵、服装状态、MJ 角色提示词 | 100人角色资产库、主角/反派补充、权力角色包、视频试镜角色包 |
| `scene-design` | 真人短剧场景库、权力空间、竖屏动线、场景状态、MJ/视频场景提示词 | 类型场景包、可复用主场景、场景试镜、人物-场景权力图 |

## 推荐工作流

### 1. 人物资产库

```text
角色目标 → 类型角色包 → 多族裔 casting 分布 → 骨相/脸型锚点 → 服装状态梯度 → MJ 全身图 → 筛图/错题 → 成品资产库
```

验收标准：

- 欧美真人短剧 casting 感，而不是概念设定或时装大片。
- 男女老少齐全，白人 / 黑人 / 拉丁裔 / 混血 / 南亚 / MENA / 原住民等分布合理。
- 全身构图、普通可信演员脸、骨相有差异，主角可以更漂亮但不能像广告模特。
- 明确排除：亚洲脸偏移、半身裁切严重、手脚崩坏、年龄错误、服装过度高定、角色功能重复。

### 2. 场景资产库

```text
剧种 → 权力空间 → 入口/出口/站位 → 竖屏 blocking lane → 光色材质锚点 → MJ 场景图 → 5-10秒视频试镜 → 可复用场景库
```

验收标准：

- 场景能拍真人短剧，不只是漂亮背景。
- 每个空间都说明谁坐、谁站、谁被挡、谁能离开、谁被迫留下。
- 适配 9:16 竖屏：前景压迫、中景对峙、后景信息点清楚。
- 明确排除：空洞豪宅背景、电影概念图、没有动线、没有权力关系、无法连续出镜。

### 3. 集成到短剧生产

```text
角色库
→ 关系矩阵
→ 服装状态梯度
→ 场景包
→ 人物-场景权力图
→ MJ资产出图
→ 视频试镜
→ 分集提示词
```

## 复制即用请求

### 角色设计

```text
帮我用 character-design 补 10 个欧美真人短剧“漂亮女主/强女主”角色，要求不同年龄、不同肤色、不同社会阶层，全身 MJ casting prompt，普通可信但有封面吸引力。
```

```text
帮我检查这批 MJ 角色图是否合格：只保留欧美真人短剧 casting 感、全身构图、年龄和族裔准确、服装可信的图；把失败原因沉淀成错题本。
```

```text
帮我按权力架构补一组角色：trust attorney、probate judge、district attorney、hospital administrator、insurance investigator、private school dean、HOA president、charity chair、gala patron。
```

### 场景设计

```text
帮我用 scene-design 做“豪门继承权”场景包：mansion foyer、boardroom、private law office、hospital corridor、gala hall、police interview room。每个场景写清权力座位、竖屏站位、道具锚点和 MJ 场景 prompt。
```

```text
帮我把一个 penthouse 场景做成三种状态：恋爱初期、权力反转、分手爆发。每种状态给光线、陈设、人物站位和 5秒视频试镜提示词。
```

```text
帮我判断这个场景是不是短剧可拍：是否有入口出口、冲突距离、压迫前景、身份道具、权力高低差、连续出镜稳定锚点。
```

## 文件位置

```text
.agents/skills/
├── character-design/
│   ├── SKILL.md
│   ├── README.md
│   ├── agents/openai.yaml
│   ├── SECTIONS/
│   └── references/
│       ├── full-manual.md
│       ├── bone-face-structure-layer.md
│       ├── frontloaded-character-assets.md
│       ├── live-action-shortdrama-casting-assets.md
│       └── shortdrama-character-production-system.md
└── scene-design/
    ├── SKILL.md
    ├── README.md
    ├── agents/openai.yaml
    └── references/
        ├── full-manual.md
        └── live-action-shortdrama-scene-system.md
```

## 安装

复制到本机 agent 技能目录：

```bash
mkdir -p ~/.agents/skills
cp -R .agents/skills/character-design ~/.agents/skills/
cp -R .agents/skills/scene-design ~/.agents/skills/
```

如果你用 Claude Code 风格目录，也可以复制到：

```bash
mkdir -p ~/.claude/skills
cp -R .agents/skills/character-design ~/.claude/skills/
cp -R .agents/skills/scene-design ~/.claude/skills/
```

## 读取原则

- 默认只读 `SKILL.md`：它是轻量运行入口。
- 需要更深方法时，再读 `references/*.md` 或 `SECTIONS/*.md`。
- 不要一开始就把完整手册全部读进上下文。
- 做短剧资产库时，优先打开真人短剧相关 reference，而不是旧的泛角色/泛场景章节。

## Git Workflow

- 所有更新走 feature branch + pull request。
- `main` 已设置保护：禁止删除、禁止 force push，并要求通过 PR 合并。
- 当前没有强制 CI/status checks，避免无 CI 时卡住合并。

## License

Released under the MIT License unless a downstream package states otherwise. Keep the visible watermark when redistributing public copies.
