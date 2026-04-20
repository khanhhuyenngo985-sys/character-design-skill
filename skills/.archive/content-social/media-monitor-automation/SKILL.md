---
name: media-monitor-automation
description: 自动化行业媒体 RSS 监控系统，抓取并整理广告创意、奢侈品时尚、营销趋势等内容，沉淀到知识库。支持反爬适应和自动进化。
origin: ECC
version: 1.4
---

# Media Monitor Automation

自动化行业媒体 RSS 监控系统，定期抓取内容并智能沉淀到知识库。支持反爬适应和自动进化。

## 核心功能

1. **RSS 监控** — 监控多个已验证的媒体源
2. **内容摘要** — 自动生成每日摘要
3. **智能分类** — 按行业/品牌自动归档
4. **知识晋升** — 评估内容价值，晋升到知识库
5. **自动进化** — 监测失败源、发现新源、适应反爬机制

---

## 自动进化机制

### 进化检查清单（每周执行）

当监控源失败时，自动触发进化流程：

- [ ] **Step 1**: 记录失败源 URL、失败时间、错误类型
- [ ] **Step 2**: 搜索同类型可替代 RSS 源
- [ ] **Step 3**: 测试新源稳定性（连续 3 天）
- [ ] **Step 4**: 更新配置并记录到本技能文件
- [ ] **Step 5**: 删除失效源配置

### 反爬适应策略

当 RSS 返回验证码或 HTML 时：

1. **检测信号**：连续 3 次返回非 XML 内容
2. **尝试方案**：
   - 更换 User-Agent
   - 添加 Referer 头
   - 降低请求频率
   - 寻找镜像站或替代源
3. **记录结论**：更新 DEPRECATED_SOURCES

### 新源发现流程

主动发现新 RSS 源：

1. 搜索媒体官网底部 RSS 链接
2. 检查 RSSHub (rsshub.app) 是否有该站
3. 检查 Feedly、Inoreader 等聚合器的源
4. 测试并验证稳定性

---

## 监控的媒体分类

| 分类 | 来源 | 内容类型 |
|------|------|----------|
| 广告行业 | Campaign Brief, Nowness | 国际广告案例、创意影像 |
| 服装行业 | Fashionista, Who What Wear | 服装行业、服装搭配 |
| 奢侈品服装 | WWD, Vogue, Harper's Bazaar, Elle | 时尚行业、奢侈品动态 |
| 商业科技 | 爱范儿 | 科技评论（待修复） |

---

## 使用方式

### 查看监控状态
```bash
python3 ~/.claude/agents/knowledge-evolution/media-monitor.py
```

### 查看 Cron 配置
```bash
bash ~/.claude/agents/knowledge-evolution/setup-cron.sh status
```

### 手动触发抓取
```bash
python3 ~/.claude/agents/knowledge-evolution/media-monitor.py
```

### 检查源健康度（每周）
```bash
# 检查所有配置的源是否可用
for url in "campaignbrief.com" "nowness.com" "ifanr.com" "digitaling.com" "wwd.com" "vogue.com"; do
  status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "https://$url/feed")
  echo "$url: $status"
done
```

---

## 配置来源

编辑 `~/.claude/agents/knowledge-evolution/media-monitor.py` 中的 `RSS_SOURCES`：

```python
RSS_SOURCES = {
    "分类名称": [
        {"name": "媒体名", "url": "RSS地址", "category": "内容类型"},
    ],
}
```

---

## 已知来源状态

### 稳定可用（已验证）
- ✅ Campaign Brief (`https://campaignbrief.com/feed/`)
- ✅ Nowness (`https://www.nowness.com/rss`)
- ✅ Fashionista (`https://fashionista.com/feed`) — v1.4新增
- ✅ Who What Wear (`https://www.whowhatwear.com/rss`) — v1.4新增
- ✅ WWD (`https://wwd.com/feed/`)
- ✅ Vogue (`https://www.vogue.com/feed/rss`)
- ✅ Harper's Bazaar (`https://www.harpersbazaar.com/rss/all.xml`)
- ✅ Elle (`https://www.elle.com/rss/all.xml`)
- ❌ 爱范儿 (`https://www.ifanr.com/feed`) — 被墙
- ❌ 数英网 (`https://www.digitaling.com/rss`) — 被墙

### 已废弃（网络不通/被墙/需验证）
- ❌ Socialbeta — 网络不通
- ❌ 36kr — 验证码拦截
- ❌ 广告门、麦迪逊邦、虎嗅、亿邦动力 — 无效
- ❌ Cannes Lions、Ads of the World — 无公开 RSS

### 待测试（有潜力）
- ⏳ The Drum — 返回 HTML，需进一步测试
- ⏳ Designboom — 301 重定向，需测试新 URL
- ⏳ BoF (Business of Fashion) — 无内容返回

---

## 输出位置

- 每日摘要 → `~/Documents/白梦客知识库/intake/媒体监控/`
- 晋升内容 → `~/Documents/白梦客知识库/04-行业知识/AI视频提示词库/auto-promoted/`
- 状态追踪 → `/tmp/knowledge-evolution/media-tracking.json`
- 进化日志 → `~/Documents/白梦客知识库/🏠 知识库进化日志.md`

---

## Cron 任务

| 任务 | 时间 | 命令 |
|------|------|------|
| 媒体监控 | 每天 8:00 | `python3 media-monitor.py` |
| 健康检查 | 每周日 2:00 | `python3 scanner.py` |

---

## 添加新的 RSS 源

### 快速添加流程

1. **验证 RSS 有效性**：
```bash
curl -s --max-time 10 -A "Mozilla/5.0" "RSS地址" | head -20
```

2. **确认返回 XML 内容**（不是 HTML 或验证码）

3. **测试连续 3 天稳定性**

4. **添加到配置**：
```python
RSS_SOURCES["新分类"].append({
    "name": "媒体名",
    "url": "RSS地址",
    "category": "内容类型"
})
```

5. **更新本技能文件的"稳定可用"列表**

6. **运行测试**：
```bash
python3 ~/.claude/agents/knowledge-evolution/media-monitor.py
```

---

## 故障排查

### 抓取返回 0 条
- 检查 RSS 是否返回 XML（不是 HTML）
- 检查是否需要验证码（36kr 会被拦截）
- 使用 `curl -v` 查看完整响应

### 内容解析失败
- 大多数 RSS 有格式问题，脚本会自动尝试宽松解析
- 如果持续失败，检查 RSS 是否仍是有效 XML

### 日志位置
- `/tmp/knowledge-evolution/media.log`

---

## 参考学习项目

### TrendRadar (⭐50k)
AI驱动的舆情监控系统，聚合多平台热点 + RSS订阅，支持关键词筛选、AI翻译和推送。

- GitHub: https://github.com/sansan0/TrendRadar
- 亮点：MCP架构支持、Docker部署、多渠道推送

### Apify MCP Server (⭐1k)
用现成的爬虫抓取社交媒体、搜索引擎、电商等。

- GitHub: https://github.com/apify/apify-mcp-server
- 亮点：数千个现成爬虫覆盖主要平台

### RSS Feed Monitor (Python)
简单的 RSS 监控工具，带重试逻辑和内容下载。

- GitHub: https://github.com/daquino94/rss-telegram
- 亮点：Telegram 推送、定期检查、去重

---

## 相关文件

| 文件 | 路径 |
|------|------|
| 监控脚本 | `~/.claude/agents/knowledge-evolution/media-monitor.py` |
| 晋升脚本 | `~/.claude/agents/knowledge-evolution/knowledge-auto-promoter.py` |
| Cron 设置 | `~/.claude/agents/knowledge-evolution/setup-cron.sh` |
| 进化日志 | `~/Documents/白梦客知识库/🏠 知识库进化日志.md` |

---

## 进化记录

| 日期 | 版本 | 更新内容 |
|------|------|----------|
| 2026-04-02 | v1.0 | 初始版本，8个稳定RSS源 |
| 2026-04-02 | v1.1 | 添加自动进化机制、参考项目 |
| 2026-04-02 | v1.2 | **高优先级修复**：动态UA池、RSSHub备用源、失败自动降级、趋势分析、告警机制 |
| 2026-04-03 | v1.4 | **深化升级**：精准分类（服装/箱包/香水/配饰/广告）、案例自动沉淀、洞察摘要 |

---

## v1.3 新增功能

### 1. 内容价值评分 (0-100)
```python
def score_article(item) -> int:
    # 基础分 50
    # + 高价值词: campaign, 品牌, 奢侈品, 联名, 限定...
    # - 招聘/求职类
    # + 标题长度适中
```

### 2. 相似度去重
```python
def deduplicate_articles(items, threshold=0.8):
    # 基于词集合相似度 > 0.8 去重
```

### 3. 精选内容 TOP 3
- 🔥 70+ 分 | 📌 60-69分 | 📄 60-分
- 自动生成精选内容版块

---

## v1.2 修复详情

### 1. 动态 User-Agent 池
每次请求随机选择 5 个不同 UA，避免被识别。

### 2. RSSHub 备用源
连续失败3次后自动切换到 RSSHub 备用。

### 3. 失败追踪 + 自动降级
记录失败次数，成功后自动重置。

### 4. 趋势分析
摘要新增**高频关键词统计**，自动提取内容趋势。

### 5. 告警机制
连续失败超过6次时发送告警（可扩展到 Slack/钉钉）。

---

## v1.4 深化升级

### 1. 精准子分类
新增针对白梦客关注领域的精准分类关键词库：

| 分类 | 关键词示例 |
|------|-----------|
| 服装 | dress, gown, runway, 时装, 裙装 |
| 箱包 | bag, handbag, leather goods, 手袋, LV, Hermès |
| 香水 | perfume, fragrance, scent, 香水, 香调, Chanel, Dior |
| 配饰 | jewelry, watch, sunglasses, 珠宝, 腕表 |
| 广告创意 | campaign, advertising, brand film, 广告, 创意 |
| 联名限定 | collaboration, limited edition, 联名, 限定 |

### 2. 案例自动沉淀
- 65分以上优质内容自动生成案例卡片
- 存入 `~/Documents/白梦客知识库/intake/广告案例沉淀/`
- 包含：广告类型、视觉风格、色调倾向、情感诉求分析模板

### 3. 洞察摘要
- 今日内容子分类分布统计
- 高频关键词升级为20+关键词跟踪
- 自动生成今日洞察摘要

---

*最后更新：2026-04-03 v1.4*
