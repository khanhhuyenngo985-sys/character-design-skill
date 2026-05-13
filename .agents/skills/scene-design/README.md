# Scene Design Skill

> 多参宗白梦客出品。禁止任何盗卖行为。

`scene-design` 是面向 AI 视频和 **海外 / 欧美真人竖屏短剧** 的场景设计技能。它不是只做“漂亮背景”，而是把场景设计成能承载冲突、权力、走位和连续出镜的生产资产。

## 适合什么时候用

- 做欧美真人短剧场景库：豪宅、办公室、医院、律师事务所、警局、学校、慈善晚宴、董事会、法院、底层公寓等。
- 设计权力空间：谁坐主位、谁被迫站着、谁被门口/桌子/玻璃隔开、谁能控制出口。
- 为 9:16 竖屏短剧设计 blocking lane：前景压迫、中景对峙、后景信息点。
- 把同一场景做成多种状态：恋爱、羞辱、反击、崩溃、胜利。
- 输出 MJ 场景 prompt、视频试镜 prompt、人物-场景权力关系表。

## 复制即用

```text
帮我用 scene-design 做一个欧美真人短剧场景包：豪门继承权 + 复仇爱情类型，包含 mansion foyer、boardroom、penthouse、hospital corridor、law office、gala hall、police interview room。每个场景都要写权力位置、竖屏 blocking、道具锚点和 MJ prompt。
```

```text
帮我把 penthouse 做成三种状态：恋爱初期、权力反转、分手爆发。每种状态输出光线、陈设、人物站位、情绪压力和 5秒视频试镜提示词。
```

```text
帮我诊断这个场景是否短剧可拍：是否有入口出口、冲突距离、压迫前景、身份道具、权力高低差、连续出镜稳定锚点。
```

## 常用输出格式

### 场景卡

- 场景编号 / 中文名 / 英文名
- 类型功能：压迫、诱惑、审判、交易、秘密暴露、反击、逃离
- 空间结构：入口、出口、主位、从属位、阻隔物、可移动路线
- 权力机制：谁高、谁低、谁坐、谁站、谁控制门/桌/灯/文件
- 竖屏 blocking：前景压迫、中景冲突、后景信息点
- 光线、色彩、材质、固定道具、声音锚点
- 场景状态梯度：日常、危机、爆发、余波
- MJ 场景 prompt / 5-10 秒视频试镜 prompt / 禁止漂移

### MJ 真人短剧场景 prompt

```text
live-action vertical short drama set photo of [scene], realistic Western TV drama location, clear power-space layout: [who controls the room / seating / exits], 9:16 blocking lanes with foreground pressure, midground confrontation space, background story anchors, practical production design, believable props, cinematic but not concept art, no empty luxury showroom --ar 9:16 --style raw
```

### 合格门槛

- 必须能服务真人短剧表演，而不是一张空背景。
- 必须有权力关系：座位、门、桌、玻璃、楼梯、走廊尽头都要有叙事作用。
- 必须适配竖屏：人物站进去后仍然能看出压迫、距离和身份。
- 必须能连续出镜：有稳定锚点，下一场还能认出来。
- 失败场景直接重做：只有豪华装修、没有动线、没有冲突距离、没有可拍的前中后景、像游戏概念图。

## 结构

```text
scene-design/
├── SKILL.md
├── README.md
├── agents/openai.yaml
└── references/
    ├── full-manual.md
    └── live-action-shortdrama-scene-system.md
```

## 读取原则

先读 `SKILL.md`。做真人短剧场景库时，优先打开：

- `references/live-action-shortdrama-scene-system.md`

只有需要完整场景方法论时，才读 `references/full-manual.md`。

## License

MIT. Keep the visible watermark when redistributing public copies.
