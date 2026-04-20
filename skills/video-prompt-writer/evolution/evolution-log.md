# Video Prompt Writer 进化日志

技能迭代记录，每次汇总分析后更新。

---

## 进化触发条件

满足以下任一条件时，执行进化汇总：
1. **案例积累**：成功模式记录 ≥ 5 条新案例
2. **时间触发**：距上次进化 ≥ 1个月
3. **重大失败**：出现 2 条以上同类型失败记录

---

## 进化流程

```
1. 读取 evolution/cases.md 中的所有案例
2. 读取 evolution/learnings.md 中的学习总结
3. 分析：
   - 成功模式中哪些技巧被重复验证？
   - 失败模式中哪些问题反复出现？
   - 有哪些新的过门方式/镜头类型组合？
4. 更新 evolution/learnings.md
5. 必要时更新 SKILL.md 主体内容
6. 记录本次进化日志
```

---

## 进化记录

### v1.4 — 2026-04-02
**触发原因**：建立白梦客影调库

**新增文件**：[grade.md](grade.md) 白梦客影调库

**影调库内容（17个影调）**：

| # | 影调 | 原典 | 核心 | AI速写参数 |
|---|------|------|------|------------|
| 1 | Kodak Vision3 500T | 《1917》Deakins | 冷阴影暖高光、青橙 | teal-orange + warm highlight + film grain |
| 2 | Fuji Pro 400H | 富士400H | 青绿调、瓷白肤色 | cream highlight + teal shadow + soft |
| 3 | Leica M9 CCD | 徕卡M9 | CCD油画、浓郁红黄 | orange-red + vignette + painterly |
| 4 | ARRI Alexa 青橙 | 《银翼杀手2049》 | 青橙互补色对比 | teal-orange + log contrast + cinematic |
| 5 | Wes Anderson | 《布达佩斯大饭店》 | 糖果粉蜡、童话感 | candy color + symmetry + pastel |
| 6 | Nolan IMAX | 《星际穿越》 | 漂白高光、冷蓝 | bleach bypass + cold blue + IMAX |
| 7 | Dune 沙丘 | 《沙丘》Greig Fraser | 自然光沙漠金 | desert gold + cold violet + muted |
| 8 | 王家卫 | 《花样年华》 | 失焦柔焦、霓虹 | soft focus + neon flare + vignette |
| 9 | 北野武 | 《坐头市物语》 | 高对比蓝冷、沉默 | high contrast + cold blue + crush |
| 10 | 岩井俊二 | 《情书》 | 柔光过曝、樱花 | soft diffusion + cool blue + overexpose |
| 11 | 滨口龙介 | 《驾驶意外》 | 自然主义、低对比 | natural contrast + neutral gray |
| 12 | Film Noir | 《双重赔偿》 | 高对比暗调、黑白 | B&W + high contrast + chiaroscuro |
| 13 | Cyberpunk | 《银翼杀手》 | 霓虹紫青、雨夜 | neon purple-cyan + wet reflection |
| 14 | 70s复古 | 70s Technicolor | 棕褐柔焦、怀旧 | sepia + soft focus + warm blow |
| 15 | 白梦客通用线 | 胡金铨+王家卫+北野武+李安 | 大地色+苍青+琥珀霓虹 | earth + cyan + amber neon |
| 16 | 白梦客高定线 | Apple+Chanel/Dior+北野武+李安 | 黑白灰+冷白+克制金 | BW gray + cold white + restrained gold |

**每个影调包含**：原典出处/色彩科学/色调配方/AI提示词参数

**速查系统**：按场景（15+场景）/情绪（16种情绪）选择影调

---

### v1.3 — 2026-04-02
**触发原因**：将抽象"电影感"转化为专业电影镜头/胶卷参数

**增量更新**：
- 新增机型系统（ARRI Alexa Mini LF/RED V-Raptor/Sony Venice 2等5种）
- 新增镜头焦段系统（14mm~135mm及适用场景）
- 新增胶卷/数字质感代号系统（F001~F006）
- 新增光圈与景深系统（T1.4~T16）
- 新增滤镜系统（Pro-Mist/Black Pro-Mist/Hollywood Black Magic）
- 新增标准电影质感参数包+复古胶片质感参数包
- STYLE模板改为具体参数行（机型/镜头/质感代号/滤镜/光圈/ISO/快门）

**来源**：参考 Seedance CSV 专业提示词 + 白梦客美学系统

---

### v1.2 — 2026-04-02
**触发原因**：分析 Seedance 2.0 CSV（9550条提示词）

**增量更新**：
- 标准化 FORMAT 头写法（时长/镜头数/类型/对话/画幅）
- 新增镜头时间编码规范（0:00–0:02 格式）
- 补充 STYLE 前置描述词写法
- 扩展镜头运动术语库（Steadicam/handheld/tracking/dolly zoom/orbit等）
- 新增声音设计分层结构（环境音+动效+音乐时间轴）
- 规范化禁止项表述
- 新增 Must-Show 锚点法
- 验证过门方式分类（硬切/子弹时间/拟音先入等）
- 补充质感参数库（电影级/超写实/动漫风/复古胶片）

**来源**：分析【seedance-2-0-prompts-20260331.csv】（读取1200+行）

---

### v1.1 — 2026-04-02
**触发原因**：吸收专业分镜脚本结构

**增量更新**：
- 新增镜头类型分类（D/E/F/A）
- 新增镜头元数据层（挂载/相机位置/起幅落幅/承接过门）
- 新增双版本锚（9:16 vs 16:9构图差异）
- 新增过门方式术语表（7种固定搭配）
- 新增提示词质量体系（Must-Show/成像个性/参照覆盖稳帧/钉子4行）
- 新增自动进化机制

**来源**：分析学习【分镜提示词---半血版本.txt】

---

### v1.0 — 初始版本
**创建日期**：2026-04-02

**核心结构**：
- 导演开场白
- 全局空间锚点卡
- FORMAT + STYLE
- 情绪曲线
- 镜头单元（主语锚点 + 视听法则 + 画面与动作 + 音效和台词）

**来源**：融合水墨星海灵界范例 + 白梦客美学系统 + Seedance 2.0模式
