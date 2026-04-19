#!/usr/bin/env python3
"""
知识库自动进化扫描器
每7天自动运行，检查知识库健康度并生成进化报告
"""

import os
import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# status-writer integration
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from status_writer import write_task_status, update_stats
except ImportError:
    write_task_status = None
    update_stats = None

KB_ROOT = Path("/Users/baimengke/Documents/白梦客知识库")
REPORT_PATH = KB_ROOT / "🏠 知识库进化日志.md"
EVOLUTION_DIR = KB_ROOT / ".evolution"

METADATA_FILE = KB_ROOT / ".evolution" / "metadata.json"


def get_file_hash(filepath: Path) -> str:
    """获取文件MD5哈希"""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()


def scan_duplicates():
    """扫描重复文件（按哈希和按名称）"""
    files_by_hash = defaultdict(list)
    files_by_name = defaultdict(list)

    for md_file in KB_ROOT.rglob("*.md"):
        if ".evolution" in str(md_file) or ".brv" in str(md_file):
            continue

        # 按哈希查重
        file_hash = get_file_hash(md_file)
        files_by_hash[file_hash].append(md_file)

        # 按名称查重（不同路径下的同名文件）
        files_by_name[md_file.name].append(md_file)

    # 只返回有重复的
    duplicate_hashes = {h: paths for h, paths in files_by_hash.items() if len(paths) > 1}
    duplicate_names = {n: paths for n, paths in files_by_name.items() if len(paths) > 1}

    return duplicate_hashes, duplicate_names


def scan_file_health():
    """扫描文件健康度"""
    files_info = []

    for md_file in KB_ROOT.rglob("*.md"):
        if ".evolution" in str(md_file) or ".brv" in str(md_file):
            continue

        stat = md_file.stat()
        rel_path = md_file.relative_to(KB_ROOT)

        # 读取文件获取行数
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
        except:
            lines = 0

        # 获取修改时间
        mtime = datetime.fromtimestamp(stat.st_mtime)
        days_old = (datetime.now() - mtime).days

        files_info.append({
            "path": str(rel_path),
            "size_kb": round(stat.st_size / 1024, 1),
            "lines": lines,
            "modified_days_ago": days_old,
            "modified_date": mtime.strftime("%Y-%m-%d")
        })

    return sorted(files_info, key=lambda x: x["size_kb"], reverse=True)


def load_metadata():
    """加载或创建元数据"""
    if METADATA_FILE.exists():
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "last_scan": None,
        "total_scans": 0,
        "access_counts": {},
        "quality_scores": {},
        "created": datetime.now().isoformat()
    }


def save_metadata(metadata: dict):
    """保存元数据"""
    metadata["last_scan"] = datetime.now().isoformat()
    metadata["total_scans"] += 1
    METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def update_quality_scores(metadata: dict, files_info: list):
    """更新质量分数"""
    for file_info in files_info:
        path = file_info["path"]

        # 基础分数 = 文件大小分 + 行数分
        base_score = min(file_info["size_kb"] / 10, 50) + min(file_info["lines"] / 50, 30)

        # 访问次数加权
        access_count = metadata["access_counts"].get(path, 0)
        access_score = min(access_count * 5, 20)

        # 综合分数
        metadata["quality_scores"][path] = round(min(base_score + access_score, 100), 1)


def generate_evolution_report(metadata: dict, duplicates: tuple, files_info: list):
    """生成进化报告"""
    dup_hashes, dup_names = duplicates

    # 找出最大/最老的文件
    largest_files = files_info[:10]
    oldest_files = sorted(files_info, key=lambda x: x["modified_days_ago"], reverse=True)[:10]

    report = f"""# 知识库进化报告

> 生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M")} | 第 {metadata['total_scans']} 次扫描

---

## 健康度概览

| 指标 | 数值 |
|------|------|
| 总文件数 | {len(files_info)} |
| 重复文件（哈希） | {len(dup_hashes)} 组 |
| 重复文件（名称） | {len(dup_names)} 组 |
| 扫描总次数 | {metadata['total_scans']} |
| 最后扫描 | {metadata.get('last_scan', '从未')[:10] if metadata.get('last_scan') else '从未'} |

---

## 需要关注的文件

### 最大文件 TOP10

| 文件 | 大小 | 行数 |
|------|------|------|
"""

    for f in largest_files:
        report += f"| {f['path']} | {f['size_kb']}KB | {f['lines']} |\n"

    report += f"""
### 最久未更新 TOP10

| 文件 | 天数未更新 |
|------|----------|
"""

    for f in oldest_files:
        report += f"| {f['path']} | {f['modified_days_ago']}天 |\n"

    if dup_hashes:
        report += f"""
## 重复文件（哈希相同，建议合并）

"""
        for h, paths in dup_hashes.items():
            report += f"**哈希：** `{h[:12]}...`\n"
            for p in paths:
                report += f"- {p}\n"
            report += "\n"

    if dup_names:
        report += f"""
## 重复文件（名称相同，需检查）

"""
        for name, paths in dup_names.items():
            report += f"**{name}**\n"
            for p in paths:
                report += f"- {p}\n"
            report += "\n"

    report += """---

## 建议操作

"""

    suggestions = []
    if dup_hashes:
        suggestions.append(f"1. 合并 {len(dup_hashes)} 组哈希重复文件")
    if dup_names:
        suggestions.append(f"2. 检查 {len(dup_names)} 组同名文件，确认是否重复")
    if len(files_info) > 300:
        suggestions.append("3. 文件数量较多，考虑归档清理")
    if not suggestions:
        suggestions.append("✅ 知识库状态良好，无紧急操作")

    report += "\n".join(suggestions)

    report += f"""

---

*本报告由知识库自动进化系统生成*
"""

    return report


def run_evolution():
    """执行进化扫描"""
    start_time = time.time()
    dup_count = 0
    files_count = 0

    try:
        print(f"🚀 开始知识库进化扫描...")
        print(f"   知识库路径: {KB_ROOT}")

        # 确保evolution目录存在
        EVOLUTION_DIR.mkdir(parents=True, exist_ok=True)

        # 加载元数据
        metadata = load_metadata()
        print(f"   已加载元数据，扫描次数: {metadata['total_scans']}")

        # 执行扫描
        print("   扫描重复文件...")
        duplicates = scan_duplicates()
        dup_count = len(duplicates[0]) + len(duplicates[1])
        print(f"   发现 {dup_count} 组重复")

        print("   检查文件健康度...")
        files_info = scan_file_health()
        files_count = len(files_info)
        print(f"   扫描了 {files_count} 个文件")

        # 更新质量分数
        print("   更新质量分数...")
        update_quality_scores(metadata, files_info)

        # 保存元数据
        save_metadata(metadata)

        # 生成报告
        print("   生成进化报告...")
        report = generate_evolution_report(metadata, duplicates, files_info)

        # 追加到进化日志
        with open(REPORT_PATH, 'a', encoding='utf-8') as f:
            f.write("\n\n---\n\n")
            f.write(report)

        print(f"✅ 进化扫描完成")
        print(f"   报告已追加到: {REPORT_PATH}")

        # Write status on success
        duration = int(time.time() - start_time)
        if write_task_status:
            write_task_status("scanner", "success", duration, None, files_count)

        return duplicates, files_info

    except Exception as e:
        duration = int(time.time() - start_time)
        if write_task_status:
            write_task_status("scanner", "fail", duration, str(e), files_count)
        raise


if __name__ == "__main__":
    run_evolution()
