---
name: mj-prompt
description: 生成Midjourney/niji静态图像提示词，融合白梦客东方美学体系。触发词：「MJ提示词」「生成图片」「Midjourney」「niji」「图生提示词」「封面图」。
---

# MJ 提示词技能 · 白梦客美学版

> 版本：v1.1 | 更新：2026-04-20 | 适用：Midjourney v7 + niji7

## TL;DR
```
创作需求 → 选择风格线（高定线/通用线）→ 匹配合影调+光影+构图 → 组装英文提示词 → 迭代生成
```

## 启动检查点

激活后先确认：
1. **风格线**：高定线（品牌广告）or 通用线（故事/情绪短片）？
2. **场景类型**：胡金铨山林 / 王家卫街道 / 北野武海边 / 高定线品牌？
3. **画幅**：4:5（小红书封面）/ 9:16（视频）/ 1:1（图文）/ 2.35:1（电影）？

---

## 核心原则

**MJ是画布，不是摄影机。**
- 研究**画家/艺术家/美学运动**，不是电影导演
- 视频动态交给 Seedance，MJ专注静态画面美学

---

## 小红书速查

| 内容类型 | 推荐比例 | --ar 值 | 说明 |
|----------|----------|---------|------|
| 竖版视频封面 | 4:5 | --ar 4:5 | **小红书最常用**，移动端满屏 |
| 竖版视频素材 | 9:16 | --ar 9:16 | 全屏视频，沉浸感强 |
| 方形图文封面 | 1:1 | --ar 1:1 | 简洁，突出主体 |
| 电影感横版 | 2.35:1 | --ar 2.35:1 | 小红书横版内容少，不推荐 |

**首选 4:5**，最适合小红书移动端浏览体验。

---

## 一、白梦客美学配方

### 通用线（故事短片/情绪短片）
融合：胡金铨 + 王家卫 + 北野武 + 李安

| 维度 | 配方 |
|------|------|
| 色调 | 大地色50% + 苍青20% + 琥珀霓虹20% + 饱和红10% |
| 光影 | 侧逆光+烟雾70% + 霓虹漫射30% |
| 构图 | 前景遮挡+极简留白 + 情绪元素点缀 |
| 节奏 | 长镜头留白70% + 抽帧慢动作20% + 硬切断刀10% |

### 高定线（高端品牌广告）
融合：Apple + Chanel/Dior + 北野武 + 李安

| 维度 | 配方 |
|------|------|
| 色调 | 黑白40% + 大地灰20% + 冷白20% + 克制金/铜20% |
| 光影 | 自然光50% + 单一致光源30% + 极轻霓虹20% |
| 构图 | 60%+负空间，极简留白，16:9或2.35:1 |
| 节奏 | 长镜头凝视60% + 静默留白30% + 偶尔快切10% |
| 质感 | 16mm/35mm胶片，过曝1/3档，轻颗粒 |

---

## 二、色彩体系

### 胡金铨色调（通用线基础）

```
核心配方：大地色 50% + 苍青色 20% + 烟雾 20% + 阳光 10%

主色板：
- 苔藓绿 (60, 80, 55) — 山林、竹林
- 土褐 (100, 85, 65) — 寺庙、土地
- 烟灰 (130, 135, 130) — 烟雾、晨雾
- 苍青 (100, 130, 140) — 天空、水面
- 暗赭 (80, 50, 40) — 屋顶、门框
- 暖白 (220, 210, 190) — 阳光、宣纸
- 墨黑 (25, 25, 25) — 夜色、墨迹
```

### 王家卫色调（通用线点缀）

```
高饱和暖冷撞色：
- 琥珀/橙红 vs 阴郁蓝/绿
- 暖黄 Kodak Vision3 感
- 1990s Hong Kong 霓虹

关键色彩词：
amber neon, warm orange, deep teal, nostalgic yellow
```

### 北野武色调（通用线融合）

```
冷调人工（都市）：
墨蓝、碳灰为主

白梦客通用线融合：
胡金铨大地50% + 北野武蓝灰30% + 霓虹20%
```

---

## 三、光影系统

### 胡金铨四大光效

| 光效 | 描述 | MJ关键词 |
|------|------|----------|
| 侧逆光 | 45度侧逆，人物轮廓发光 | side-backlighting, golden rim light |
| 晨雾光 | 半阴天，软光层次多 | mist diffusion, foggy morning, soft light |
| 树隙光 | 穿过树叶的光斑，丁达尔 | god rays, dappled light through leaves |
| 灯笼光 | 寺庙/夜场景，暖黄/橙红 | warm lantern glow, amber, stable warm light |

### 光比参数

| 场景 | 光比 | MJ描述 |
|------|------|--------|
| 山林 | 1:2 | soft diffused light, gentle shadows |
| 寺庙 | 1:3 | directional light, clear contrast |
| 夜内 | 1:4 | single warm light source, deep shadow |
| 动作 | 1:6 | dramatic low-key, theatrical |

---

## 四、构图体系

### 东方绘画构图原理

```
1. 留白60%+：不是空的，是呼吸
2. 前景遮挡60%：门框、树枝、石块
3. 纵深引导：道路、栏杆、山脉
4. 黄金点偏心：人物不居中
5. 人极小，山极大
```

### 景别策略

| 景别 | 效果 |
|------|------|
| 极远景 | 人物如蚂蚁、天人合一 |
| 远景 | 建立氛围、人与环境关系 |
| 中景 | 叙事单元 |
| 近景 | 情绪 |
| 特写 | 聚焦眼睛、手、细节 |

---

## 五、画面情绪类型

### A. 禅意留白类（胡金铨）
```
场景：竹林、山寺、枯山水、晨雾
情绪：禅定、冥想、孤独修行
光效：侧逆光+烟雾散射
构图：留白70%+，前景竹子遮挡
```

### B. 都市孤独类（王家卫）
```
场景：霓虹街道、雨夜、咖啡馆、窗口
情绪：疏离、怀旧、爱而不得
光效：单一暖黄路灯、低调照明
构图：框中框（门框/窗户）、镜子反射
```

### C. 暴力沉默类（北野武）
```
场景：海边、码头、雪景、极简房间
情绪：压抑、暴力后的平静、虚无
光效：冷白自然光、低反差
构图：极端简洁、大量负空间
```

### D. 温暖怀旧类（李安）
```
场景：老宅、厨房、庭院、阴雨天
情绪：家庭、情感压抑、含蓄
光效：暖黄自然光、散射
色调：大地色为主、饱和度低
```

---

## 六、MJ提示词模板

### 模板结构

```
[画家/美学运动参考]
[画面主体描述]
[场景环境描述]
[光影效果描述]
[色彩基调描述]
[构图方式描述]
[质感/材质描述]
[情绪氛围描述]
[技术参数]
```

### 英文提示词模板

```
[美学参考], [画家参考]

[主体描述：人物/静物/风景]
[场景描述：环境、道具、氛围]
[光线描述：类型、方向、色温]
[色彩描述：主色调、撞色关系]
[构图描述：景别、留白、前景遮挡]
[质感描述：胶片/绘画材质]
[情绪描述：氛围、意境]

--ar [比例] --style raw --v 7 --s [风格化值]
```

### 参数指南

| 画风类型 | --s 值 | --style | 备注 |
|----------|--------|---------|------|
| 宋元山水 | 600-800 | raw 必须 | 太高会失真 |
| 八大山人 | 500-700 | raw 必须 | 极简难把握 |
| 超现实（达利）| 800-1000 | raw 可选 | 需要细节 |
| 马格里特 | 700-900 | raw 必须 | 干净克制 |
| 基里科 | 800-1000 | raw 可选 | 需要光影 |
| 侘寂/物哀/幽玄 | 600-800 | raw 必须 | 克制即美 |
| 胡金铨大地色 | 500-700 | raw 必须 | 还原胶片感 |
| 王家卫霓虹 | 400-600 | raw 必须 | 克制霓虹 |

---

## 七、场景类型库

### 1. 胡金铨·山林禅意

```
King Hu style, 1970s Kodak Ektachrome earth tones
cinematic scope 2.35:1

bamboo grove at dawn, morning mist rolling through
earth tone green + pale cyan sky + warm white
side-backlighting, smoke scattering, mist diffusion

foreground bamboo stalks as frame obstruction 60%
negative space 70%, figure small in frame
minimalist composition, classical Chinese landscape

meditative atmosphere, martial arts as spiritual practice
no digital feel, authentic film grain texture

--ar 2.35:1 --style raw --v 7 --s 650
```

### 2. 胡金铨·寺庙场景

```
King Hu temple interior, Zen Buddhism
1970s Kodak Ektachrome color science

Shaolin temple courtyard, incense smoke drifting
earth tones: ochre 40% + charcoal 30% + pale cyan 20% + warm white 10%
single directional light through window, dust particles visible

monks in medium shot, small in frame
architectural symmetry, Buddhist proportion

static contemplative, long take feel
incense smoke, ancient China atmosphere
no music, only ambient stillness

--ar 2.35:1 --style raw --v 7 --s 650
```

### 3. 王家卫·都市孤独

```
Wong Kar-wai aesthetic, 1990s Hong Kong
handheld camera slightly unstable, intimate and restless

neon-lit wet street at night, single warm amber streetlight
high saturation: amber orange vs deep teal shadows
low-key lighting, Rembrandt on half face

character standing still in foreground, neon crowd motion blur behind
step-printing slow motion effect, time feels thick and heavy

 voyeuristic frame through slightly open door
melancholic urban solitude, dreamlike and disconnected

--ar 16:9 --style raw --v 7 --s 500
```

### 4. 王家卫·窗口独白

```
Wong Kar-wai, In the Mood for Love
handheld, shallow focus drifting, partial framing

character reflected in rain-wet window
double image, reality and reflection overlapping
warm amber interior light, cold blue exterior

solitary figure in cramped Hong Kong apartment
1960s nostalgic color grading, Kodak Vision3 500T

melancholic anticipation, unspoken words
time suspended, isolated in their own moment

--ar 16:9 --style raw --v 7 --s 500
```

### 5. 北野武·暴力沉默

```
Takeshi Kitano style, Hana-bi inspired
extreme minimalist composition, vast negative space

quiet seaside at dusk, single figure on rocky shore
cold blue-grey tones, desaturated, shallow depth

natural ambient light, overcast sky
figure small against enormous sea and sky

stillness after violence, existential solitude
no movement, time frozen,屏息以待

--ar 16:9 --style raw --v 7 --s 400
```

### 6. 白梦客通用线·融合配方

```
King Hu × Wong Kar-wai × Takeshi Kitano
白梦客通用线 Universal Aesthetic

modern interpretation of classical Chinese aesthetics
融合比例：King Hu earth tones 50% + WKW amber neon 30% + Kitano blue-grey 20%

contemporary young creator in traditional space
earth tone foundation, pale cyan undertones
occasional amber neon accent, smoke and mist

side-backlighting, cinematic
foreground obstruction, minimalist composition
negative space 60%, contemplative pace

长镜头留白70% + 抽帧慢动作20% + 硬切断刀10%
film grain, Kodak Ektachrome 1970s color science

--ar 2.35:1 --style raw --v 7 --s 600
```

### 7. 高定线·品牌广告

```
high-end fashion editorial, Chanel/Dior meets Kitano
black and white 40% + earth grey 20% + cold white 20% + muted gold 20%

minimalist product or model in stark white studio
single directional light source, dramatic shadow
60%+ negative space, extreme simplicity

16mm film grain, slight overexposure +1/3 stop
long take stillness, no quick cuts
silence as luxury, restraint as elegance

contemporary luxury brand aesthetic
still life or single figure, monumental composition

--ar 4:5 --style raw --v 7 --s 400
```

---

## 八、短视频封面模板

### 情绪人像类

```
[王家卫风格]
close-up portrait, Wong Kar-wai aesthetic
low-key lighting, single warm amber light source
smoke in frame, shallow depth of field

face partially in shadow, contemplative expression
handheld slightly unstable, intimate
Kodak Vision3 500T film, nostalgic color
melancholic, emotionally charged, 1990s Hong Kong

--ar 4:5 --style raw --v 7 --s 500
```

### 场景氛围类

```
[胡金铨风格]
wide cinematic shot, King Hu earth tones
bamboo forest temple at dawn, morning mist
earth green + pale cyan + warm white
side-backlighting through mist, smoke scattering

solitary figure in vast landscape, negative space 70%
figure small in frame, S-curve path composition
meditative atmosphere, zen like stillness

1970s Kodak Ektachrome color science
no digital sharpness, film grain authentic

--ar 4:5 --style raw --v 7 --s 650
```

---

## 九、违禁词处理

| 禁用词 | 替换词 |
|--------|--------|
| blood, bleeding | dark red痕迹, energy residue glow |
| death, dead body | stillness, slumber, unconscious |
| violence, beating | impact, collision, strong strike |
| horror, terrifying | tension, suspense, unease |
| gore, bloody | dark liquid, energy burst |

---

## 十、工作流程

1. **确定内容方向**：情绪短片 / 品牌复刻 / 测试片
2. **选择美学配方**：通用线 / 高定线 / 融合线
3. **挑选场景类型**：胡金铨山林 / 王家卫街道 / 北野武海边
4. **组装提示词**：按模板结构填入元素
5. **调整参数**：--ar 比例、--s 风格化值
6. **生成并迭代**：根据结果微调关键词

---

---

## 第十一章 · 图片逆向提取（迭代 ≥90 分时执行）

> 从好结果反推成功因子，沉淀为可复用的提示词模式。

### 核心流程

```
好图片 → 拆解成功因子 → 归类到白梦客美学维度 → 入库到 prompt-patterns.json
```

### 逆向提取矩阵

| 成功因子类型 | 分析问题 | 归类维度 |
|-------------|---------|---------|
| **色调** | 画面偏暖还是偏冷？有没有撞色？大地色比例？ | 色调体系 |
| **光影** | 侧逆光/正面光/散射光？体积光强度？ | 光影系统 |
| **构图** | 前景遮挡比例？留白比例？黄金分割？ | 构图体系 |
| **氛围** | 禅意/都市孤独/暴力沉默/温暖怀旧？ | 情绪类型 |
| **质感** | 胶片颗粒？过曝？焦外散景？ | 质感参数 |

### 提取步骤

**Step 1：画面解构**
- 色调：从主色调判断属于哪个配方（大地色/霓虹/黑白）
- 光影：识别光源位置和类型（侧逆光/散射光/体积光）
- 构图：计算前景遮挡和负空间比例
- 氛围：对照四种情绪类型（禅意留白/都市孤独/暴力沉默/温暖怀旧）

**Step 2：因子评分**
每个维度 0-25 分，总分 100：
| 维度 | 满分 | 得分标准 |
|------|------|---------|
| 色调 | 25 | 符合配方 + 无杂色 + 有层次 |
| 光影 | 25 | 体积光强 + 粒子可见 + 方向正确 |
| 构图 | 25 | 前景遮挡 + 负空间 + 黄金点 |
| 氛围 | 25 | 情绪准确 + 意境到位 |

**Step 3：成功因子提取**

对照原提示词，找出贡献最大的片段：

```
原提示词中的片段 → 为什么好 → 提取可复用模式
```

**Step 4：生成入库报告**

```markdown
### 成功因子提取报告

**场景ID/角色ID**: [ID]
**迭代版本**: iteration-N
**得分**: [分数]

**色调成功因子**:
- [具体描述] → [归类]

**光影成功因子**:
- [具体描述] → [归类]

**构图成功因子**:
- [具体描述] → [归类]

**可复用模式**:
```json
{
  "pattern": "模式名称",
  "prompt_fragment": "提示词片段",
  "score_boost": "+N分",
  "applies_to": ["场景类型1", "场景类型2"]
}
```
```

### 入库操作

当迭代得分 ≥90 时：
1. 在对应 `case-library/[ID]/` 目录创建 `reverse-report.md`
2. 将可复用模式追加到 `knowledge-base/prompt-patterns.json`
3. 在 `iteration-report.json` 的 `learned_optimizations` 字段记录

### prompt-patterns.json 格式

```json
{
  "patterns": [
    {
      "id": "pattern-001",
      "name": "暮色渐变层次",
      "category": "色调",
      "prompt_fragment": "暮色渐浓，天边最后一抹橙红",
      "score_boost": "+8分",
      "applies_to": ["古桥", "山林", "废墟"],
      "extracted_from": "B7-L-T iteration-13",
      "extracted_at": "2026-04-13"
    }
  ]
}
```

---

**版本**：v1.0
**适用模型**：Midjourney v7 + niji7
**核心参考**：白梦客知识库·东方美学体系
