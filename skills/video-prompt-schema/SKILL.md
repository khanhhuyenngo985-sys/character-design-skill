---
name: video-prompt-schema
description: 将分镜脚本转换为结构化JSON Schema，再生成针对目标平台的优化提示词。触发词：「Schema」「分镜转提示词」「生成即梦提示词」「生成Seedance提示词」「生成Vidu提示词」「生成可灵提示词」「平台化提示词」。
---

# 视频提示词Schema技能

## 功能

将分镜脚本转换为结构化的JSON Schema格式，然后生成针对目标平台(Seedance/Vidu/海螺)的优化提示词。

## 核心价值

```
分镜脚本 → Schema(JSON) → 平台化提示词
```

**为什么比直接写提示词好：**
- 结构化捕捉所有创作参数
- 避免遗漏关键信息(色调/光影/节奏)
- 平台转换只需改output.platform
- 可版本控制，可审查，可复用

## 工作流程

### Step 1: 解析分镜脚本

读取导演/编剧产出的分镜脚本，提取：

```
- 场景数量和时长
- 主体描述
- 运镜指令
- 情绪目标
- 色调/光影偏好
```

### Step 2: 填充Schema

按 `schema.json` 结构填充：

```json
{
  "meta": {
    "title": "项目名称",
    "platform": "seedance",
    "duration": 15,
    "style_line": "高定线",
    "director_style": ["王家卫", "北野武"]
  },
  "palette": {
    "primary": "黑白40%",
    "secondary": "大地灰20%",
    "accent": "克制金20%"
  },
  "scenes": [...]
}
```

### Step 3: 生成平台化提示词

根据 `output.platform` 选择对应格式：

| 平台 | 语言 | 格式 |
|------|------|------|
| Seedance | 中文优先 | `[00:00-00:05] 镜头1描述...` |
| Vidu | 中英混合 | 风格词前置，`\|` 分隔 |
| 海螺 | 中文 | 图生视频，动态预期描述 |

### Step 4: 质量检查

对照 `quality_checklist` 逐项确认。

## Schema字段说明

### meta (必需)

| 字段 | 说明 | 示例 |
|------|------|------|
| title | 项目标题 | "香水广告-通用线" |
| platform | 目标平台 | seedance/vidu/hairui/kling |
| duration | 总时长(秒) | 15 |
| style_line | 白梦客风格线 | 高定线/通用线 |
| director_style | 导演风格引用 | ["王家卫", "北野武"] |

### palette (高定线推荐)

| 风格线 | primary | secondary | accent |
|--------|---------|-----------|--------|
| 高定线 | 黑白40% | 大地灰20% | 克制金20% |
| 通用线 | 大地色50% | 苍青20% | 琥珀霓虹20% |

### lighting (常用配置)

| 类型 | 方向 | 氛围 | 适用 |
|------|------|------|------|
| 自然光 | 侧逆光 | 干净利落 | 高定线产品 |
| 单一强光源 | 逆光 | 高对比 | 戏剧感 |
| 霓虹漫射 | 侧光 | 烟雾缭绕 | 通用线情感 |
| 冷蓝顶光 | 顶光 | 疏离感 | 恐惧/孤独 |

### scenes[].camera

| 字段 | 选项 |
|------|------|
| movement | 固定/推镜头/拉镜头/横移/摇镜头/升降/跟随/手持微动/环绕 |
| angle | 平视/俯拍/仰拍/低角度/鸟瞰/斜角 |
| distance | 远景/全景/中景/近景/特写/大特写 |
| composition | 中心对称/三分法/负空间60%+/前景遮挡/极简留白/打破构图 |

### rhythm (节奏分配)

```
高定线: long_take=60%, silence=30%, quick_cut=10%
通用线: long_take=70%, slow_motion=20%, quick_cut=10%
```

## 平台化输出示例

### Seedance (即梦)

```json
{
  "output": {
    "platform": "seedance",
    "language": "中文",
    "format": "timestamp_segmented"
  }
}
```

生成：

```
高定线香水广告，[女子在极简空间]，

[00:00-00:05] 远景建立，缓慢推近，女子穿过空旷画廊，自然光50%侧逆光，Kodak Ektachrome 1970s
然后切换到：
[00:05-00:10] 中景凝视，固定镜头，手腕喷洒香水，克制金色点缀光源，过曝1/3档，轻微颗粒
然后切换到：
[00:10-00:15] 远景拉远，背影剪影，烟雾缭绕，渐隐fade to black

黑白40% 大地灰20% 冷白20% 克制金20%，
侧逆光+烟雾缭绕，16mm胶片，2.35:1电影宽屏，
参考：Chanel N5, Dior J'adore
```

### Vidu Q2/Q3

```json
{
  "output": {
    "platform": "vidu",
    "language": "中英混合",
    "format": "structured"
  }
}
```

生成：

```
王家卫风格 电影感广告，优雅女子在极简空间，

Wong Kar-wai cinematic style, female subject in minimalist space,
缓慢推近 slow push-in, 中景 mid-shot, 侧逆光 side-backlight,
黑白60% 金铜20% 苍青20%, Kodak Portra 800,
overexposed 1/3 stop, light grain, smoky haze atmosphere,

| 烟雾弥漫 dreamy mist | 手部特写 wrist close-up | 凝视 gaze |
```

### 海螺 (图像转视频)

```json
{
  "output": {
    "platform": "hairui",
    "language": "中文",
    "format": "dynamic_description"
  }
}
```

生成：

```
极简空间女子侧影，
动态预期: 轻微横移跟拍，呼吸起伏，烟雾缓慢流动，
光影: 侧逆光打出发丝光，克制金色光泽，
氛围: 孤独疏离感，凝视感，
时长: 5s
```

## 使用场景

screenwriter/director 使用此技能时：

1. 完成A4/A5分镜脚本后
2. 调用此技能填充Schema
3. 生成目标平台的提示词
4. 如需调整平台，修改output.platform重新生成

## 案例参考

已有案例库: `~/.claude/case-library/`

案例中的有效手法可直接填入Schema对应字段。

## 质量检查清单

- [ ] meta.platform 与 output.platform 一致
- [ ] scenes总时长 ≈ meta.duration
- [ ] palette 已按风格线配置
- [ ] lighting.direction 具体化(不只是"好光")
- [ ] camera.movement + angle + distance 三者完整
- [ ] 每个scene有emotion.intensity
- [ ] rhythm百分比加起来≈100%
- [ ] output.language 符合平台要求

### Kling 3.0 (可灵)

```json
{
  "output": {
    "platform": "kling",
    "language": "英文为主",
    "format": "english_with_params"
  }
}
```

生成：

```
旗袍女子背影，雨夜上海街道，侧逆光，青灰与琥珀霓虹
handheld跟拍，中景，60%负空间，前景竹叶遮挡
earth tones 50%, teal 20%, amber neon 20%
long take 70%, step-printing slow motion 0.3x, rain drops visible
Kodak Portra 400 film grain, cinematic
dialogue lip_sync: true, melancholic whisper
ambient: rain on pavement, 30%
bgm: jazz saxophone, 65BPM

--duration 45
--motion MEDIUM
--camera handheld
--camera-path bezier
--focal-length 35mm
--style cinematic
--aspect 2.35:1
--texture 35mm-grain
--audio native_sync
```
