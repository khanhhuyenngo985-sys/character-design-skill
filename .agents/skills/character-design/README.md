# Character Design Skill

> 多参宗白梦客出品。禁止任何盗卖行为。

`character-design` 是面向 AI 视频和 **海外 / 欧美真人竖屏短剧** 的人物设计技能。它不仅输出角色外貌，还负责把人物做成可生产的资产：角色功能、骨相脸型、服装状态、关系矩阵、MJ casting prompt、视频试镜提示词。

## 适合什么时候用

- 做 50-100 个欧美真人短剧人物资产库。
- 补主角、漂亮女主、强女主、反派、亲属、闺蜜、情敌、富豪、律师、医生、警察、法官等类型角色。
- 按权力架构设计角色：trust attorney、probate judge、district attorney、hospital administrator、insurance investigator、private school dean、HOA president、charity chair、gala patron。
- 给角色加骨相 / face structure anchors，避免 AI 生成普通网红脸或族裔漂移。
- 诊断 MJ 角色图：筛掉亚洲脸偏移、半身裁切、时装大片、概念设定、年龄/族裔错误。

## 复制即用

```text
帮我用 character-design 做一组欧美真人短剧角色库：100个角色，男女老少、多族裔、多肤色、主角/反派/亲属/律师/医生/警察/富豪/底层角色都要覆盖，输出 MJ 可直接出图的 full-body casting prompt。
```

```text
帮我补 10 个特别漂亮但可信的欧美真人短剧女主：不要广告模特感，要普通演员脸 + 封面吸引力；每个角色写年龄、族裔/肤色、骨相、职业、服装状态、MJ prompt。
```

```text
帮我检查这批 MJ 角色图是否合格：只保留欧美真人短剧 casting 感、全身构图、年龄和族裔准确、服装可信的图；把失败原因记录成错题本。
```

## 常用输出格式

### 角色卡

- 角色编号 / 中文名 / 英文名
- 叙事功能：主角、反派、盟友、压迫者、证人、制度代理人等
- 年龄层 / 性别 / 族裔或肤色 / 社会阶层
- 骨相与脸型锚点：jawline、cheekbones、brow ridge、nose bridge、face shape 等
- 体型、发型、表情、姿态、服装、材质、道具
- 关系边：谁压迫谁、谁依附谁、谁掌握秘密
- 服装状态梯度：日常、受辱、反击、胜利、崩溃
- MJ prompt / negative prompt / 筛图标准

### MJ 真人短剧 casting prompt

```text
full-body live-action short drama casting photo of [role], [age/gender/ethnicity/skin tone], ordinary believable Western actor face, specific bone structure: [face anchors], wardrobe fitting for [social role], neutral casting studio light, clean full body composition, realistic proportions, practical TV drama styling, not fashion editorial, not concept art --ar 2:3 --style raw
```

### 合格门槛

- 必须像真人短剧选角照 / wardrobe fitting，而不是概念设定图。
- 必须全身构图，脸、身形、服装和角色功能能同时读清楚。
- 多族裔分布必须真实，不能全部变成同一种“泛欧美网红脸”。
- 主角可以更漂亮，但仍要有可信演员感和生活质感。
- 失败图直接淘汰：亚洲脸偏移、半身裁切严重、手脚崩坏、年龄错误、服装过度时装大片、角色功能不清。

## 结构

```text
character-design/
├── SKILL.md
├── README.md
├── agents/openai.yaml
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
    ├── full-manual.md
    ├── bone-face-structure-layer.md
    ├── frontloaded-character-assets.md
    ├── live-action-shortdrama-casting-assets.md
    └── shortdrama-character-production-system.md
```

## 读取原则

先读 `SKILL.md`。做欧美真人短剧人物库时，优先打开：

- `references/live-action-shortdrama-casting-assets.md`
- `references/shortdrama-character-production-system.md`
- `references/bone-face-structure-layer.md`

只有需要完整旧方法论时，才读 `references/full-manual.md` 或 `SECTIONS/*.md`。

## License

MIT. Keep the visible watermark when redistributing public copies.
