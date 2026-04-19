#!/usr/bin/env python3
"""
行业媒体RSS监控系统 v1.4
定期抓取行业媒体最新内容，生成摘要存入知识库
支持：RSSHub、动态UA、失败自动降级、告警机制
新增：中文摘要、精准分类、案例沉淀、洞察摘要
"""

import json
import time
import random
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from xml.etree import ElementTree as ET
import urllib.request
import urllib.error
import re

# status-writer integration
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from status_writer import write_task_status
except ImportError:
    write_task_status = None
    update_stats = None

# 知识库根目录
KB_ROOT = Path("/Users/baimengke/Documents/白梦客知识库")
INTAKE_DIR = KB_ROOT / "intake" / "媒体监控"
ARCHIVE_DIR = INTAKE_DIR / "archive"
LOG_DIR = Path("/tmp/knowledge-evolution")

# ========== 核心配置 ==========

# 动态 User-Agent 池
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
]

# RSSHub 备用源（当原生RSS失效时使用）
RSSHUB_SOURCES = {
    # 格式: "源名": "RSSHub路径"
    # RSSHub 公共实例: https://rsshub.app
    "WWD": "/wwd/feed",
    "Vogue": "/vogue/feed",
    "Harper's Bazaar": "/harpersbazaar/feed",
    "Elle": "/elle/feed",
    "Campaign Brief": "/campaignbrief/feed",
    "The Drum": "/thedrum/feed",
}

# 行业媒体RSS源（已验证稳定的源）
RSS_SOURCES = {
    "广告行业": [
        {"name": "Campaign Brief", "url": "https://campaignbrief.com/feed/", "category": "广告案例", "fail_count": 0},
        {"name": "Nowness", "url": "https://www.nowness.com/rss", "category": "创意影像", "fail_count": 0},
        {"name": "数英网", "url": "https://www.digitaling.com/rss", "category": "广告创意", "fail_count": 0},
    ],
    "奢侈品服装": [
        {"name": "WWD", "url": "https://wwd.com/feed/", "category": "时尚行业", "fail_count": 0},
        {"name": "Vogue", "url": "https://www.vogue.com/feed/rss", "category": "奢侈品时尚", "fail_count": 0},
        {"name": "Harper's Bazaar", "url": "https://www.harpersbazaar.com/rss/all.xml", "category": "奢侈品时尚", "fail_count": 0},
        {"name": "Elle", "url": "https://www.elle.com/rss/all.xml", "category": "时尚美容", "fail_count": 0},
    ],
    "服装行业": [
        {"name": "Fashionista", "url": "https://fashionista.com/feed", "category": "服装行业", "fail_count": 0},
        {"name": "Who What Wear", "url": "https://www.whowhatwear.com/rss", "category": "服装搭配", "fail_count": 0},
    ],
}

# ========== v1.4 新增：精准分类关键词 ==========

# 针对白梦客关注领域的精准分类关键词
CATEGORY_KEYWORDS = {
    "服装": [
        "dress", "gown", "collection", "ready-to-wear", "runway", "fashion show",
        "couture", "silhouette", "fabric", "textile", "blouse", "skirt", "pants",
        "jacket", "coat", "sweater", "shirt", "fashion", "clothing", "apparel",
        "设计师", "时装", "服装", "裙装", "外套", "面料"
    ],
    "箱包": [
        "bag", "handbag", "tote", "clutch", "purse", "leather goods", "luggage",
        "accessories", "wallets", "backpack", "shoulder bag", "bucket bag",
        "包", "手袋", "皮具", "行李", "钱包", "背包", "LV", "Hermès", "Gucci", "Prada"
    ],
    "香水": [
        "perfume", "fragrance", "scent", "cologne", "eau de parfum", "flacon",
        "nose", "perfumer", "notes", "accord", "botanical", "olfactory",
        "香水", "香氛", "香调", "调香师", "香原料", "Chanel", "Dior", "Jo Malone", "Le Labo", "Byredo"
    ],
    "配饰": [
        "jewelry", "jewellery", "ring", "bracelet", "necklace", "earring", "brooch",
        "watch", "timepiece", "sunglasses", "eyewear", "hat", "scarf", "belt", "gloves",
        "珠宝", "腕表", "眼镜", "围巾", "腰带", "戒指", "项链", "耳环", "手镯"
    ],
    "广告创意": [
        "campaign", "advertising", "advertorial", "commercial", "brand film", "spot",
        "creative direction", "art direction", "photography", "campaign brief",
        "广告", "创意", "品牌影片", "广告片", "宣传片", "大片"
    ],
    "联名限定": [
        "collaboration", "collab", "limited edition", "exclusive", "capsule",
        "联名", "限定", "合作", "限量", "独家", "胶囊系列"
    ]
}

# 高价值评分关键词（叠加加分）
HIGH_VALUE_KEYWORDS = [
    "campaign", "advertising", "brand film", "creative direction",
    "联名", "限定", "限量", "合作系列", "艺术家联名",
    "Chanel", "Dior", "Louis Vuitton", "Hermès", "Gucci", "Prada", "Balenciaga",
    "sustainable", "innovation", "heritage", "craftsmanship"
]

# ========== 已确认不可用的源（保留作参考）
DEPRECATED_SOURCES = {
    "广告门": "https://www.adquan.com/RSS.aspx - URL错误（网络不通）",
    "麦迪逊邦": "https://www.madison.com.cn/feed - URL错误",
    "虎嗅": "https://www.huxiu.com/rss/ - RSS格式特殊",
    "亿邦动力": "https://www.ebrun.com/feed/ - 403禁止",
    "派代": "https://www.paidai.com/feed - URL错误",
    "优设": "https://www.uisdc.com/feed - RSS解析失败",
    "站酷": "https://www.zcool.com.cn/feed - 404不存在",
    "Socialbeta": "https://www.socialbeta.com.cn/feed - 网络不通/超时",
    "36kr": "https://36kr.com/feed - 验证码拦截（被墙）",
    "The Drum": "https://www.thedrum.com/rss - 返回HTML非RSS",
    "Designboom": "https://designboom.com/feed/ - 301重定向",
    "Ads of the World": "无公开RSS（需付费订阅）",
    "Cannes Lions": "无公开RSS（需注册）",
    "BoF (Business of Fashion)": "https://www.businessoffashion.com/feed - 无内容返回",
}

# 追踪文件
TRACKING_FILE = LOG_DIR / "media-tracking.json"
FAILURE_LOG_FILE = LOG_DIR / "media-failures.json"

# 失败阈值
FAIL_THRESHOLD = 3  # 连续失败3次后切换RSSHub
RSSHUB_INSTANCE = "https://rsshub.app"


# ========== 核心函数 ==========

def get_random_ua() -> str:
    """随机获取一个 User-Agent"""
    return random.choice(USER_AGENTS)


def load_failure_log() -> Dict:
    """加载失败日志"""
    if FAILURE_LOG_FILE.exists():
        with open(FAILURE_LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_failure_log(log: Dict):
    """保存失败日志"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(FAILURE_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def record_failure(source_name: str, error: str):
    """记录失败并检查是否需要切换到 RSSHub"""
    failure_log = load_failure_log()

    if source_name not in failure_log:
        failure_log[source_name] = {"count": 0, "last_error": "", "last_attempt": None, "rsshub_used": False}

    failure_log[source_name]["count"] += 1
    failure_log[source_name]["last_error"] = error[:100]
    failure_log[source_name]["last_attempt"] = datetime.now().isoformat()

    # 检查是否切换到 RSSHub
    if failure_log[source_name]["count"] >= FAIL_THRESHOLD and not failure_log[source_name].get("rsshub_used"):
        if source_name in RSSHUB_SOURCES:
            failure_log[source_name]["rsshub_used"] = True
            failure_log[source_name]["fallback_url"] = f"{RSSHUB_INSTANCE}{RSSHUB_SOURCES[source_name]}"
            print(f"   ⚠️ {source_name} 连续失败{failure_log[source_name]['count']}次，切换到RSSHub备用")

    save_failure_log(failure_log)


def reset_failure(source_name: str):
    """成功后重置失败计数"""
    failure_log = load_failure_log()
    if source_name in failure_log:
        failure_log[source_name]["count"] = 0
        save_failure_log(failure_log)


def get_fallback_url(source_name: str) -> Optional[str]:
    """获取备用 URL（RSSHub）"""
    failure_log = load_failure_log()
    if source_name in failure_log and failure_log[source_name].get("rsshub_used"):
        return failure_log[source_name].get("fallback_url")
    return None


def fetch_rss(url: str, timeout: int = 15, max_retries: int = 3, source_name: str = "") -> Optional[str]:
    """抓取RSS内容，支持动态UA、重试和错误处理"""
    import ssl

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # 每次请求随机选择 User-Agent
    ua = get_random_ua()
    # 中文站点用自身域名作 Referer，其他用 Google
    from urllib.parse import urlparse
    domain = urlparse(url).netloc
    referer = f"https://{domain}/" if any(d in domain for d in ['digitaling', 'ifanr', '36kr', 'huxiu']) else 'https://www.google.com/'
    headers = {
        'User-Agent': ua,
        'Accept': 'application/rss+xml, application/xml, text/xml, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Referer': referer,
    }

    for attempt in range(max_retries):
        try:
            # 如果有备用URL且原URL连续失败过，使用备用URL
            fetch_url = url
            if attempt == 0 and source_name:
                fallback = get_fallback_url(source_name)
                if fallback:
                    fetch_url = fallback

            req = urllib.request.Request(fetch_url, headers=headers)

            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
                content = response.read()

                # 检测是否返回了 HTML 或验证码页面（只检查开头500字符）
                try:
                    text = content.decode('utf-8')
                    head = text[:500].lower()
                    if head.startswith('<!doctype html') or head.startswith('<html') or 'captcha' in head or ('验证' in head and '<?xml' not in head):
                        if source_name:
                            record_failure(source_name, "返回HTML/验证码")
                        print(f"   ⚠️ {source_name} 返回了HTML或验证码")
                        return None
                except:
                    pass

                # 检测编码
                if content.startswith(b'\xef\xbb\xbf'):
                    content = content[3:]
                elif content.startswith(b'\xff\xfe'):
                    content = content[2:].decode('utf-16-le').encode('utf-8')

                return content.decode('utf-8')

        except urllib.error.HTTPError as e:
            if e.code == 404:
                if source_name:
                    record_failure(source_name, "404")
                return None
            if source_name:
                record_failure(source_name, f"HTTP {e.code}")
            if attempt == max_retries - 1:
                return None
            time.sleep(1 * (attempt + 1))

        except urllib.error.URLError as e:
            if source_name:
                record_failure(source_name, str(e.reason)[:50])
            if attempt == max_retries - 1:
                return None
            time.sleep(1 * (attempt + 1))

        except ssl.SSLError:
            if attempt == max_retries - 1:
                ctx = ssl._create_unverified_context()
                req = urllib.request.Request(fetch_url, headers=headers)
                try:
                    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
                        return response.read().decode('utf-8')
                except:
                    return None
            time.sleep(1 * (attempt + 1))

        except Exception as e:
            if source_name:
                record_failure(source_name, str(e)[:50])
            if attempt == max_retries - 1:
                return None
            time.sleep(1 * (attempt + 1))

    return None


def parse_rss(xml_content: str) -> List[Dict]:
    """解析RSS内容，支持非标准格式"""
    items = []
    import html

    xml_content = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', xml_content, flags=re.DOTALL)
    xml_content = html.unescape(xml_content)

    try:
        root = ET.fromstring(xml_content)
        for item in root.findall('.//item')[:10]:
            title = item.findtext('title', '无标题')
            link = item.findtext('link', '')
            description = item.findtext('description', '')[:200]
            pub_date = item.findtext('pubDate', '')
            description = re.sub(r'<[^>]+>', '', description)

            items.append({
                'title': title.strip() if title else '无标题',
                'link': link.strip() if link else '',
                'description': description.strip() if description else '',
                'pub_date': pub_date
            })
    except ET.ParseError:
        item_matches = re.findall(r'<item>(.*?)</item>', xml_content, re.DOTALL)
        for item_xml in item_matches[:10]:
            entry = {}
            for field, pattern in [
                ('title', r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>'),
                ('link', r'<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>'),
                ('description', r'<description>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>'),
                ('pub_date', r'<pubDate>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</pubDate>')
            ]:
                match = re.search(pattern, item_xml, re.DOTALL)
                entry[field] = match.group(1).strip() if match else ''
            entry['description'] = re.sub(r'<[^>]+>', '', entry.get('description', ''))[:200]
            if entry.get('title'):
                items.append({
                    'title': entry['title'],
                    'link': entry['link'],
                    'description': entry['description'],
                    'pub_date': entry.get('pub_date', '')
                })
    except Exception:
        pass

    return items


def get_tracking_data() -> Dict:
    """获取追踪数据"""
    if TRACKING_FILE.exists():
        with open(TRACKING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "last_scan": None,
        "feeds_tracked": list(RSS_SOURCES.keys()),
        "articles_collected": 0
    }


def save_tracking_data(data: Dict):
    """保存追踪数据"""
    data["last_scan"] = datetime.now().isoformat()
    INTAKE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(TRACKING_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def score_article(item: Dict) -> int:
    """对文章进行价值评分 (0-100)"""
    score = 50  # 基础分
    title = item.get('title', '').lower()
    description = item.get('description', '').lower()

    # v1.4: 使用精准关键词库
    for kw in HIGH_VALUE_KEYWORDS:
        if kw.lower() in title or kw.lower() in description:
            score += 10

    # 扣分项
    negative_keywords = ['job', '招聘', 'hiring', 'join us', 'career', 'jobs']
    for kw in negative_keywords:
        if kw.lower() in title:
            score -= 30

    # 标题长度适中给加分（太短可能信息不足）
    if 10 < len(title) < 60:
        score += 10

    return max(0, min(100, score))


def detect_subcategory(item: Dict) -> List[str]:
    """v1.4: 检测文章所属的细分子分类"""
    title = item.get('title', '').lower()
    description = item.get('description', '').lower()
    text = f"{title} {description}"

    detected = []
    for subcat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text:
                if subcat not in detected:
                    detected.append(subcat)
                break  # 匹配到一个关键词即可

    return detected if detected else ["其他"]


def generate_case_card(item: Dict, category: str) -> Optional[Path]:
    """v1.4: 为高价值广告案例生成案例沉淀卡片"""
    score = item.get('score', 0)
    if score < 65:  # 只为中高分以上内容生成案例卡
        return None

    # 确定案例类型
    title = item.get('title', '')
    subcategories = detect_subcategory(item)

    # 创建案例沉淀目录
    case_dir = INTAKE_DIR.parent / "广告案例沉淀"
    case_dir.mkdir(parents=True, exist_ok=True)

    # 生成文件名
    date_str = datetime.now().strftime('%Y%m%d')
    safe_title = re.sub(r'[^\w\s-]', '', title)[:40].replace(' ', '_')
    filename = f"{date_str}_{safe_title}.md"
    filepath = case_dir / filename

    # 提取品牌名
    brands = []
    brand_keywords = ["Chanel", "Dior", "Louis Vuitton", "LV", "Hermès", "Gucci", "Prada",
                      "Balenciaga", "Celine", "Versace", "YSL", "Saint Laurent", "Givenchy",
                      "Burberry", "Bottega Veneta", "Loewe", "Maison Margiela", "Vogue", "WWD"]
    for brand in brand_keywords:
        if brand.lower() in title.lower() or brand.lower() in item.get('description', '').lower():
            brands.append(brand)

    # 生成案例卡片
    content = f"""# {title}

> **品牌:** {', '.join(brands) if brands else '待识别'}
> **来源:** {item.get('source', '未知')}
> **原文链接:** {item.get('link', '')}
> **分类:** {' / '.join(subcategories)}
> **评分:** {score} / 100
> **抓取时间:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 原文摘要

{item.get('description', '无描述')}

---

## 案例分析

### 广告类型
- [ ] 品牌广告 Film/Brand Film
- [ ] 平面广告 Print Campaign
- [ ] 社交媒体 Social Campaign
- [ ] 联名合作 Collaboration
- [ ] 限定系列 Limited Edition

### 视觉风格
- [ ] 极简留白 Minimal / Negative Space
- [ ] 戏剧化场景 Dramatic Set
- [ ] 纪实风格 Documentary / Real Life
- [ ] 艺术装置 Art Installation
- [ ] 复古怀旧 Vintage / Retro

### 色调倾向
- [ ] 黑白 Black & White
- [ ] 大地色 Earth Tone
- [ ] 高饱和 High Saturation
- [ ] 冷调灰蓝 Cool Gray/Blue
- [ ] 暖调金铜 Warm Gold/Copper

### 情感诉求
- [ ] 欲望/性感 Desire / Sensuality
- [ ] 传承/Heritage Heritage / Legacy
- [ ] 工艺/Craftsmanship Craft / Artisanal
- [ ] 颠覆/反叛 Subversion / Rebellion
- [ ] 治愈/温暖 Healing / Warmth

---

## 创意亮点

_记录这篇文章中最值得借鉴的1-3个创意点_

1.

2.

3.

---

## 对我的启发

_记录这个案例如何应用到白梦客的项目中_

-

---

## 相关标签

{' '.join(['#'+c for c in subcategories])} #广告案例 #{' #'.join(brands) if brands else ''}

---

*本案例由媒体监控系统 v1.4 自动生成*
"""

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath
    except Exception:
        return None


def deduplicate_articles(items: List[Dict], threshold: float = 0.8) -> List[Dict]:
    """基于标题相似度去重"""
    if not items:
        return []

    unique = []
    for item in items:
        is_duplicate = False
        title1 = item.get('title', '').lower()
        for existing in unique:
            title2 = existing.get('title', '').lower()
            # 简单的词集合相似度
            words1 = set(title1.split())
            words2 = set(title2.split())
            if words1 and words2:
                intersection = len(words1 & words2)
                union = len(words1 | words2)
                similarity = intersection / union if union > 0 else 0
                if similarity > threshold:
                    is_duplicate = True
                    break
        if not is_duplicate:
            unique.append(item)
    return unique


def generate_daily_summary(category: str, sources: List[Dict], all_items: List[Dict]) -> tuple:
    """v1.4: 生成每日摘要 + 自动沉淀案例卡片"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"{date_str}_{category}.md"
    filepath = INTAKE_DIR / filename

    # 去重、评分、分类
    all_items = deduplicate_articles(all_items)
    case_cards_created = []

    for item in all_items:
        item['score'] = score_article(item)
        item['subcategories'] = detect_subcategory(item)
        # v1.4: 为高价值内容生成案例卡片
        if item.get('score', 0) >= 65:
            card_path = generate_case_card(item, category)
            if card_path:
                item['case_card'] = str(card_path)
                case_cards_created.append(card_path)

    # 按评分排序
    all_items.sort(key=lambda x: x.get('score', 0), reverse=True)

    # v1.4: 统计各子分类数量
    subcat_counts = {}
    for item in all_items:
        for subcat in item.get('subcategories', []):
            subcat_counts[subcat] = subcat_counts.get(subcat, 0) + 1

    # 趋势分析关键词扩展
    trend_keywords = list(CATEGORY_KEYWORDS.keys()) + list(CATEGORY_KEYWORDS.values())[:10]
    all_titles = ' '.join([i['title'] for i in all_items])
    all_descriptions = ' '.join([i['description'] for i in all_items])
    all_text = f"{all_titles} {all_descriptions}"

    content = f"""# {category} 媒体摘要

> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
> 来源数量：{len(sources)} 个媒体
> 文章数量：{len(all_items)} 篇（去重后）
> 优质内容：{len([i for i in all_items if i.get('score', 0) >= 70])} 篇
> 案例沉淀：{len(case_cards_created)} 张案例卡

---

## 今日概览

"""

    # v1.4: 按子分类展示
    for subcat, count in sorted(subcat_counts.items(), key=lambda x: x[1], reverse=True):
        content += f"- **{subcat}**: {count} 篇\n"

    content += "\n---\n\n"

    for source in sources:
        source_items = [i for i in all_items if source['name'] in i.get('source', '')]
        content += f"### {source['name']}\n"
        content += f"来源：{source['url']}\n\n"

        if source_items:
            for item in source_items[:5]:
                score_emoji = "🔥" if item.get('score', 0) >= 70 else "📌" if item.get('score', 0) >= 60 else "📄"
                subcats = ' '.join(['#'+c for c in item.get('subcategories', [])[:2]])
                content += f"- {score_emoji} **{item['title']}** [评分:{item.get('score', 0)}] {subcats}\n"
                content += f"  {item['description'][:80]}...\n"
                content += f"  [链接]({item['link']})\n\n"
        else:
            content += f"- （今日无更新）\n\n"

    # v1.4: 趋势洞察升级
    content += """---

## 趋势洞察

### 高频关键词
"""
    keyword_counts = {}
    for kw in trend_keywords[:20]:
        if isinstance(kw, str) and len(kw) > 2:
            count = all_text.lower().count(kw.lower())
            if count > 0:
                keyword_counts[kw] = count

    top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:8]
    for kw, count in top_keywords:
        if count > 0:
            content += f"- {kw}: {count}次\n"

    # v1.4: 洞察摘要
    content += """
### 今日洞察
"""
    # 根据高频词生成简单洞察
    top3cats = [c for c, _ in list(subcat_counts.items())[:3]]
    if top3cats:
        content += f"- 今日{top3cats[0]}相关内容最多，"
        if len(top3cats) > 1:
            content += f"其次是{'和'.join(top3cats[1:])}"
        content += "\n"

    # 优质内容 TOP 3
    top_items = [i for i in all_items if i.get('score', 0) >= 60][:3]
    if top_items:
        content += "\n### 精选内容 TOP 3\n"
        for i, item in enumerate(top_items, 1):
            subcats = ' / '.join(item.get('subcategories', [])[:2])
            content += f"{i}. **{item['title']}** (评分:{item.get('score', 0)}) [{subcats}]\n"
            content += f"   {item['description'][:100]}...\n"
            if item.get('case_card'):
                content += f"   📋 [案例卡]({item['case_card']})\n"

    # v1.4: 案例卡片汇总
    if case_cards_created:
        content += """
### 案例卡片
"""
        for card in case_cards_created:
            content += f"- 📋 `{card.name}`\n"

    content += """

---

## 重点关注

### 广告创意趋势
待填写

### 行业动态
待填写

---

*本摘要由行业媒体监控系统自动生成 v1.4*
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath, case_cards_created


def check_source_health() -> Dict[str, List[str]]:
    """检查所有源的健康状态"""
    issues = {}
    failure_log = load_failure_log()

    for category, sources in RSS_SOURCES.items():
        for source in sources:
            name = source['name']
            if name in failure_log:
                log = failure_log[name]
                if log.get('rsshub_used'):
                    issues.setdefault(category, []).append(f"{name} ⚠️(RSSHub) - {log.get('last_error', '')}")
                elif log.get('count', 0) >= FAIL_THRESHOLD:
                    issues.setdefault(category, []).append(f"{name} ❌ - {log.get('last_error', '')}")

    return issues


def send_alert(message: str):
    """发送告警（目前只打印，后续可扩展）"""
    print(f"\n🚨 告警: {message}\n")
    # 后续可扩展：发送到 Slack/钉钉/邮件


def run_monitor():
    """运行监控"""
    start_time = time.time()
    total_articles = 0
    all_items_by_category = {}

    try:
        print(f"🚀 开始行业媒体监控 v1.3...")
        print(f"   摄入目录: {INTAKE_DIR}")

        INTAKE_DIR.mkdir(parents=True, exist_ok=True)
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        LOG_DIR.mkdir(parents=True, exist_ok=True)

        # 健康检查
        issues = check_source_health()
        if issues:
            print("\n⚠️  源健康度警告:")
            for cat, warnings in issues.items():
                for w in warnings:
                    print(f"   {cat}: {w}")

        tracking = get_tracking_data()
        print(f"   上次扫描: {tracking.get('last_scan', '从未')[:10] if tracking.get('last_scan') else '从未'}")

        for category, sources in RSS_SOURCES.items():
            print(f"\n📰 监控 {category}...")
            all_items = []

            for source in sources:
                name = source['name']
                url = source['url']
                print(f"   📡 抓取 {name}...")

                xml_content = fetch_rss(url, source_name=name)
                if xml_content:
                    items = parse_rss(xml_content)
                    for item in items:
                        item['source'] = name
                        item['category'] = source['category']
                    all_items.extend(items)
                    reset_failure(name)  # 成功后重置失败计数
                    print(f"      ✅ 获取 {len(items)} 条")
                else:
                    # 检查是否有备用源
                    fallback = get_fallback_url(name)
                    if fallback:
                        print(f"      📡 尝试RSSHub备用...")
                        xml_content = fetch_rss(fallback, source_name=name)
                        if xml_content:
                            items = parse_rss(xml_content)
                            for item in items:
                                item['source'] = f"{name}(RSSHub)"
                                item['category'] = source['category']
                            all_items.extend(items)
                            print(f"      ✅ RSSHub获取 {len(items)} 条")

            if all_items:
                summary_path, case_cards = generate_daily_summary(category, sources, all_items)
                print(f"      📝 摘要已保存: {summary_path.name}")
                if case_cards:
                    print(f"      📋 案例卡片: {len(case_cards)} 张")
                all_items_by_category[category] = all_items
                total_articles += len(all_items)

        # 更新追踪数据
        tracking["articles_collected"] += total_articles
        save_tracking_data(tracking)

        # 触发知识晋升
        try:
            promoter_script = Path(__file__).parent / "knowledge-auto-promoter.py"
            if promoter_script.exists():
                result = os.system(f"python3 '{promoter_script}' >> /tmp/knowledge-evolution/promoter.log 2>&1")
                if result == 0:
                    print("  ✅ 知识自动晋升完成")
        except Exception as e:
            print(f"  ⚠️ 晋升过程有警告: {e}")

        # 检查是否需要发送告警
        failure_log = load_failure_log()
        critical_failures = [k for k, v in failure_log.items() if v.get('count', 0) >= FAIL_THRESHOLD * 2]
        if critical_failures:
            send_alert(f"以下源连续失败超过{FAIL_THRESHOLD * 2}次: {', '.join(critical_failures)}")

        print(f"\n✅ 监控完成")
        print(f"   本次抓取: {total_articles} 篇")
        print(f"   累计抓取: {tracking['articles_collected']} 篇")

        duration = int(time.time() - start_time)
        if write_task_status:
            write_task_status("media", "success", duration, None, total_articles)

        return all_items_by_category

    except Exception as e:
        duration = int(time.time() - start_time)
        if write_task_status:
            write_task_status("media", "fail", duration, str(e), total_articles)
        send_alert(f"媒体监控任务失败: {str(e)}")
        raise


if __name__ == "__main__":
    run_monitor()
