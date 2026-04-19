#!/usr/bin/env python3
"""
竞品广告库自动采集脚本
定期采集各行业竞品最新广告，更新到知识库
"""

import os
import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import re

# status-writer integration
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from status_writer import write_task_status, update_stats
except ImportError:
    write_task_status = None
    update_stats = None

# 知识库根目录
KB_ROOT = Path("/Users/baimengke/Documents/白梦客知识库")
COMPETITOR_DIR = KB_ROOT / "04-行业知识" / "竞品广告库"

# 竞品配置：各行业主要竞品
COMPETITORS = {
    "服装": {
        "高端": ["ICICLE之禾", "EP雅莹", "Marisfrolg", "JNBY"],
        "大众": ["MO&Co.", "Lily", "太平鸟", "UR"],
        "新锐": ["内外", "Ubras", "蕉内"]
    },
    "美妆": {
        "高端": ["CHANEL", "Dior", " Lancôme", "YSL"],
        "国货高端": ["花西子", "完美日记", "珀莱雅", "薇诺娜"],
        "新锐": ["夸迪", "肌活", "逐本", "HBN"]
    },
    "快消": {
        "饮料": ["元气森林", "农夫山泉", "娃哈哈", "怡宝"],
        "零食": ["三只松鼠", "良品铺子", "百草味", "卫龙"],
        "乳制品": ["伊利", "蒙牛", "安慕希", "金典"]
    },
    "电子": {
        "手机": ["Apple", "华为", "小米", "OPPO", "vivo"],
        "电脑": ["Apple", "联想", "华为", "戴尔"],
        "耳机": ["Apple", "Sony", "Bose", "华为"]
    },
    "奢侈品": {
        "顶级": ["Louis Vuitton", "Chanel", "Dior", "Hermès", "Gucci", "Prada", "Balenciaga", "Saint Laurent"],
        "高端": ["Burberry", "Givenchy", "Valentino", "Bottega Veneta", "Loewe", "Celine", "Maison Margiela"],
        "轻奢": ["Coach", "Michael Kors", "Kate Spade", "Tory Burch", "Ralph Lauren", "Max Mara"]
    },
    "香水": {
        "顶级": ["Chanel No.5", "Dior J'adore", "Tom Ford", "Jo Malone", "Le Labo", "Byredo", "Maison Margiela", "Creed"],
        "大众": ["YSL Black Opium", "Gucci Bloom", "Versace", "Calvin Klein", "Burberry Hero"]
    },
    "箱包": {
        "顶级": ["Louis Vuitton", "Hermès Birkin", "Chanel", "Dior Lady", "Gucci Jackie", "Prada Nylon", "Bottega Cassette", "Celine Belt"],
        "轻奢": ["Coach", "Michael Kors", "Tory Burch", "Kate Spade", "Furla", "Longchamp", "Radley"]
    }
}

TRACKING_FILE = COMPETITOR_DIR / ".tracking.json"


def get_tracking_data() -> Dict:
    """获取追踪数据"""
    if TRACKING_FILE.exists():
        with open(TRACKING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "last_scan": None,
        "ads": {},
        "brands_tracked": list(COMPETITORS.keys())
    }


def save_tracking_data(data: Dict):
    """保存追踪数据"""
    data["last_scan"] = datetime.now().isoformat()
    TRACKING_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TRACKING_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_ad_archive_path(industry: str, brand: str, ad_title: str) -> Path:
    """生成广告存档路径"""
    brand_dir = COMPETITOR_DIR / industry / brand.replace(" ", "_")
    brand_dir.mkdir(parents=True, exist_ok=True)

    # 生成安全文件名
    safe_title = re.sub(r'[^\w\s-]', '', ad_title)[:50]
    safe_title = safe_title.replace(' ', '_')

    return brand_dir / f"{safe_title}.md"


def create_ad_archive(industry: str, brand: str, ad_info: Dict) -> Path:
    """创建广告存档"""
    filepath = generate_ad_archive_path(industry, brand, ad_info.get("title", "untitled"))

    content = f"""# {ad_info.get('title', '竞品广告')}

> 品牌：{brand} | 行业：{industry}
> 来源：{ad_info.get('source', '未知')}
> 采集时间：{datetime.now().strftime('%Y-%m-%d')}
> 标签：{', '.join(ad_info.get('tags', []))}

---

## 广告信息

| 字段 | 内容 |
|------|------|
| 广告标题 | {ad_info.get('title', '-')} |
| 投放渠道 | {ad_info.get('channel', '-')} |
| 广告类型 | {ad_info.get('type', '-')} |
| 投放时间 | {ad_info.get('date', '-')} |
| 链接 | {ad_info.get('url', '-')} |

---

## 内容分析

### 核心信息
{ad_info.get('core_message', '待填写')}

### 视觉风格
{ad_info.get('visual_style', '待填写')}

### 创意亮点
{ad_info.get('highlights', '待填写')}

### 目标受众
{ad_info.get('target_audience', '待填写')}

---

## 我们的借鉴

### 可以学习的地方
- 待填写

### 需要避免的地方
- 待填写

---

## 原始素材

{ad_info.get('raw_content', '无原始素材')}

"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath


def generate_brand_index(industry: str, brand: str) -> Path:
    """生成品牌索引"""
    brand_dir = COMPETITOR_DIR / industry / brand.replace(" ", "_")
    brand_dir.mkdir(parents=True, exist_ok=True)
    ads = list(brand_dir.glob("*.md"))

    content = f"""# {brand} - 竞品广告库

> 行业：{industry} | 品牌：{brand}
> 广告数量：{len(ads)} | 最后更新：{datetime.now().strftime('%Y-%m-%d')}

---

## 广告列表

| 序号 | 广告标题 | 采集时间 | 标签 |
|------|---------|---------|------|
"""

    for i, ad in enumerate(sorted(ads), 1):
        content += f"| {i} | {ad.stem.replace('_', ' ')} | {datetime.fromtimestamp(ad.stat().st_mtime).strftime('%Y-%m-%d')} | 待添加 |\n"

    content += f"""
---

## 品牌分析

### 品牌定位
待填写

### 视觉调性
待填写

### 广告策略
待填写

### 目标受众
待填写

---

*本索引由竞品广告库自动系统生成*
"""

    index_path = brand_dir / "INDEX.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return index_path


def generate_industry_index() -> Path:
    """生成行业索引"""
    content = f"""# 竞品广告库 - 行业总览

> 更新时间：{datetime.now().strftime('%Y-%m-%d')}

---

## 行业分布

| 行业 | 品牌数 | 广告数 |
|------|--------|--------|
"""

    for industry, tiers in COMPETITORS.items():
        industry_path = COMPETITOR_DIR / industry
        if industry_path.exists():
            brands = [d for d in industry_path.iterdir() if d.is_dir()]
            total_ads = sum(len(list(b.glob("*.md"))) for b in brands)
            content += f"| {industry} | {len(brands)} | {total_ads} |\n"

    content += """
---

## 最近更新

| 时间 | 行业 | 品牌 | 广告 |
|------|------|------|------|
"""

    # 获取最近更新的广告
    all_ads = []
    for md_file in COMPETITOR_DIR.rglob("*.md"):
        if md_file.name == "INDEX.md":
            continue
        all_ads.append(md_file)

    for ad in sorted(all_ads, key=lambda x: x.stat().st_mtime, reverse=True)[:10]:
        parts = ad.relative_to(COMPETITOR_DIR).parts
        if len(parts) >= 2:
            industry = parts[0]
            brand = parts[1].replace("_", " ")
            mtime = datetime.fromtimestamp(ad.stat().st_mtime).strftime('%Y-%m-%d')
            content += f"| {mtime} | {industry} | {brand} | {ad.stem.replace('_', ' ')[:30]} |\n"

    content += """
---

## 使用说明

### 目的
收集竞品广告，分析学习，用于：
1. 了解行业趋势
2. 学习创意手法
3. 发现差异化机会

### 更新频率
建议每周更新一次主要竞品的新广告

### 如何贡献
1. 发现竞品好广告 → 手动添加到对应品牌目录
2. 运行脚本自动采集 → `python3 competitor-scraper.py`
3. 定期复盘整理 → 每月底更新品牌分析

---

*本索引由竞品广告库自动系统生成*
"""

    index_path = COMPETITOR_DIR / "INDEX.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return index_path


def run_scan():
    """运行采集扫描"""
    start_time = time.time()

    try:
        print(f"🚀 开始竞品广告库扫描...")
        print(f"   目录: {COMPETITOR_DIR}")

        # 确保目录存在
        COMPETITOR_DIR.mkdir(parents=True, exist_ok=True)

        # 加载追踪数据
        tracking = get_tracking_data()
        print(f"   上次扫描: {tracking.get('last_scan', '从未')[:10] if tracking.get('last_scan') else '从未'}")

        # 创建行业索引
        print("   生成行业索引...")
        generate_industry_index()

        # 为每个行业品牌生成索引
        for industry, tiers in COMPETITORS.items():
            for tier, brands in tiers.items():
                for brand in brands:
                    generate_brand_index(industry, brand)

        print(f"✅ 扫描完成")
        print(f"   竞品广告库已更新")
        print(f"   请手动添加新发现的竞品广告到对应目录")

        # Write status on success (this script generates indexes, not new content)
        duration = int(time.time() - start_time)
        if write_task_status:
            write_task_status("competitor", "success", duration, None, 0)

        return tracking

    except Exception as e:
        duration = int(time.time() - start_time)
        if write_task_status:
            write_task_status("competitor", "fail", duration, str(e), 0)
        raise


if __name__ == "__main__":
    run_scan()
