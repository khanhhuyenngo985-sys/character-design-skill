---
技能版本: v1.0
创建日期: 2026-04-04
更新日期: 2026-04-04
使用次数: 0
最后使用项目: —
版本历史:
  - v1.0 (2026-04-04): 初始创建，基于跨国药企/高端医疗机构品牌美学
---

# 医药健康广告 - 信任线技能

## 适用场景
- 行业：医药健康（制药、保健品、医疗器械）
- 风格：信任线
- 品牌调性：科学、关怀、可靠

## 美学配方

### 色调
- 冷白30% + 浅蓝25% + 清新灰20% + 克制暖色25%
- 参考：跨国药企品牌视觉、高端医疗机构

### 光影
- 明亮干净的自然光70%
- 柔和补光20%
- 极轻氛围光10%
- 避免过度戏剧性打光

### 节奏
- 平稳叙事60% + 静默留白25% + 偶尔情绪快切15%
- 禁忌：全程快切、过度剪辑

### 质感
- 高清数码或35mm胶片
- 清晰锐利，但不过度锐化
- 轻柔和色调

## 镜头语言

### 推荐景别
- 人物表情特写（眼神、微笑）
- 产品细节（药品、医疗器械）
- 专家/医生形象
- 数据可视化/图表
- 生活场景（家庭、健康生活）

### 氛围元素
- 专业感、可信赖感
- 温暖的人文关怀
- 科学与技术元素
- 真实患者故事（避免过度煽情）

### 禁忌
- 不能夸大功效（合规要求）
- 不能用过于刺激的颜色（高饱和、荧光色）
- 不能过度情感化/煽情
- 不能使用不真实的数据展示
- 不能出现患者面部特写（隐私）

## 声音设计

### BGM风格
- 舒缓钢琴曲或氛围音乐
- 或轻量电子乐（柔和）
- 音量轻柔，衬底为主

### 音效
- 清晰配音，专业播音腔
- 环境音（医院、实验室氛围）
- 禁忌：过度音效、科技感过强的电子音

## 参考案例
- 跨国药企品牌广告（诺华、辉瑞、葛兰素史克）
- 高端医疗机构品牌片（和睦家、Mayo Clinic）
- 医疗器械企业形象片（GE医疗、西门子医疗）
- 保健品信赖感广告（Swisse、Blackmores）

## 输出格式

screenwriter/director 使用此技能时：
1. 读取本技能的美学配方
2. 在 A1/A5 中引用对应条款
3. 确保所有创作决策符合本技能规范
4. 所有台词需过 humanize-dialogue 技能去AI味
5. 注意医药广告合规要求，避免夸大表述
6. **路由到 `prompt-matrix` 生成最终平台化提示词**

## AI视频提示词模板

```
[Style/Genre] healthcare/pharmaceutical commercial, [main subject] [core action],

[00:00-00:05] Shot 1: [camera movement] [angle], [subject] [action], [lighting] [atmosphere], [texture details]
then cut to:
[00:05-00:10] Shot 2: [camera movement] [angle], [subject] [action], [lighting] [atmosphere], [texture details]
then cut to:
[00:10-00:15] Shot 3: [camera movement] [angle], [subject] [action], [lighting] [atmosphere], [texture details]
then cut to:
[00:15-00:20] Shot 4: [camera movement] [angle], [subject] [action], [lighting] [atmosphere], [texture details]

Cinematic, Kodak Portra 400 or clean digital, 1.85:1,
cold white 30% + light blue 25% + fresh gray 20% + restrained warm tone 25%,
bright clean natural light 70% + soft fill light 20% + minimal ambient light 10%,
steady narrative 60% + silence pause 25% + occasional emotional quick cut 15%,
sharp but not over-sharpened, soft color tones,
soothing piano [BGM风格] or ambient music, clear professional voice-over
参考：Novartis, Pfizer, GSK brand films, United Family Healthcare, Mayo Clinic medical films
```

Make sure the prompt captures:
- 色调：冷白30% + 浅蓝25% + 清新灰20% + 克制暖色25%
- 光影：明亮干净自然光70% + 柔和补光20% + 极轻氛围光10%
- 节奏：平稳叙事60% + 静默留白25% + 偶尔情绪快切15%
- 质感：高清数码，清晰锐利，轻柔和色调
- 参考：诺华、辉瑞、葛兰素史克、和睦家、Mayo Clinic
