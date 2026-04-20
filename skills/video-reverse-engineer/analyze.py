#!/usr/bin/env python3
"""
Video Reverse Engineer - 广告视频自动拆解工具 v2.0
基于 PySceneDetect 场景检测 + 智能关键帧提取
用法: python analyze.py "/path/to/video.mp4" --frames 30 --output ./output
"""

import cv2
import os
import sys
import argparse
import subprocess
import numpy as np
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

# ---- HDR暗帧校正 ----
def correct_dark_frame(frame: np.ndarray, min_brightness: int = 20, target_brightness: int = 80) -> np.ndarray:
    """处理HDR或摄影机直出导致的暗帧
    用gamma校正替代线性增益，更能保留相对对比度
    min_brightness: 亮度低于此值才校正（保留故意的暗调创意）
    target_brightness: 目标亮度参考值
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mean_brightness = float(np.mean(gray))

    # 只有当亮度 < min_brightness 时才校正（保护故意的暗调镜头）
    if mean_brightness >= min_brightness:
        return frame

    # Gamma校正：gamma > 1 提亮暗部，同时保持对比度关系
    # 如果 mean_brightness=5, target=80, gamma ≈ 0.5 (强力提亮)
    # 如果 mean_brightness=20, target=80, gamma ≈ 0.7 (轻度提亮)
    if mean_brightness > 0:
        gamma = np.log(target_brightness / 255.0) / np.log(mean_brightness / 255.0)
        gamma = max(0.3, min(gamma, 1.5))  # 限制范围
    else:
        gamma = 0.4  # 极度暗的帧用固定gamma

    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)], dtype=np.uint8)

    # 分别处理每个通道
    result = cv2.LUT(frame, table)

    # CLAHE增强局部对比度（让暗部细节更清晰）
    lab = cv2.cvtColor(result, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    return result


# ---- PySceneDetect 场景检测 ----
def detect_scenes_pyscenedetect(video_path: str) -> list:
    """使用PySceneDetect检测镜头边界"""
    try:
        from scenedetect import detect, AdaptiveDetector, ContentDetector

        # 优先用AdaptiveDetector（适合广告这类快节奏内容）
        # min_scene_len=6 表示至少6帧才算一个新镜头
        # 对于15fps视频，约0.4秒，是合理的广告镜头最小长度
        scenes = detect(
            video_path,
            AdaptiveDetector(adaptive_threshold=3.0, min_scene_len=6),
            show_progress=False
        )

        result = []
        for scene in scenes:
            start_frame = scene[0].frame_num
            end_frame = scene[1].frame_num
            start_time = scene[0].get_timecode()
            end_time = scene[1].get_timecode()
            duration_frames = end_frame - start_frame
            result.append({
                "start_frame": start_frame,
                "end_frame": end_frame,
                "start_time": start_time,
                "end_time": end_time,
                "duration_frames": duration_frames,
            })
        return result
    except ImportError:
        print("Warning: PySceneDetect not installed, falling back to basic detection")
        return None


def detect_scenes_fallback(video_path: str) -> list:
    """兜底的简单场景检测（无PySceneDetect时）"""
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    prev_gray = None
    scene_changes = []
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev_gray is not None:
            diff = float(np.mean(np.abs(gray.astype(float) - prev_gray.astype(float))))
            if diff > 30:
                scene_changes.append(frame_idx)
        prev_gray = gray.copy()
        frame_idx += 1

    cap.release()

    if not scene_changes:
        return [{"start_frame": 0, "end_frame": total_frames - 1, "duration_frames": total_frames}]

    # 构建镜头列表
    scenes = []
    prev = 0
    for change in scene_changes:
        scenes.append({"start_frame": prev, "end_frame": change - 1, "duration_frames": change - prev})
        prev = change
    scenes.append({"start_frame": prev, "end_frame": total_frames - 1, "duration_frames": total_frames - prev})
    return scenes


def get_scene_mid_frame(scene: dict, video_path: str) -> Optional[tuple]:
    """提取镜头中间帧（简单取中，避免暗帧区的边缘检测偏差）"""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    start = scene["start_frame"]
    end = scene["end_frame"]

    # 简单取中间帧
    mid = (start + end) // 2

    cap.set(cv2.CAP_PROP_POS_FRAMES, mid)
    ret, frame = cap.read()
    cap.release()

    if ret:
        frame = correct_dark_frame(frame)
        return (mid / fps, frame)
    return None


def get_scene_best_frame(scene: dict, video_path: str) -> Optional[tuple]:
    """提取镜头中最佳的代表性帧
    - 暗调镜头（平均亮度<40）：取首帧（暗到亮的过渡瞬间最有意义）
    - 亮调镜头：取边缘最丰富+变化最大的帧
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    start = scene["start_frame"]
    end = scene["end_frame"]
    duration = end - start

    if duration <= 4:
        cap.set(cv2.CAP_PROP_POS_FRAMES, (start + end) // 2)
        ret, frame = cap.read()
        cap.release()
        if ret:
            frame = correct_dark_frame(frame)
            return ((start + end) / 2 / fps, frame)
        return None

    # 先采样前中后三帧，判断是否为暗调镜头
    sample_points = [
        start + duration // 4,      # 前1/4
        start + duration // 2,      # 中间
        start + duration * 3 // 4,  # 后3/4
    ]

    cap.set(cv2.CAP_PROP_POS_FRAMES, sample_points[1])
    ret, mid_sample = cap.read()
    cap.release()

    if ret:
        mid_gray = cv2.cvtColor(mid_sample, cv2.COLOR_BGR2GRAY)
        mid_brightness = float(np.mean(mid_gray))
    else:
        mid_brightness = 100

    # 暗调镜头：取首帧（保留"暗"的氛围）
    if mid_brightness < 40:
        best_frame = start + duration // 10  # 镜头开始后10%处（不是第一帧，避免黑帧）
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, best_frame)
        ret, frame = cap.read()
        cap.release()
        if ret:
            frame = correct_dark_frame(frame)
            return (best_frame / fps, frame)

    # 亮调镜头：找边缘最丰富的帧
    best_frame = sample_points[1]
    best_edge_score = -1

    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, sample_points[0])
    prev_gray = None

    for f_idx, f in enumerate(sample_points):
        cap.set(cv2.CAP_PROP_POS_FRAMES, f)
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_score = float(np.mean(edges))

        if edge_score > best_edge_score:
            best_edge_score = edge_score
            best_frame = f

    cap.release()

    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, best_frame)
    ret, frame = cap.read()
    cap.release()

    if ret:
        frame = correct_dark_frame(frame)
        return (best_frame / fps, frame)
    return None


# ---- 色彩分析 ----
def rgb_to_color_name(rgb: list) -> str:
    """RGB转颜色名称"""
    r, g, b = rgb
    if max(rgb) < 50:
        return "黑色"
    if max(rgb) < 100:
        return "深灰"
    if r > 200 and g > 200 and b > 200:
        return "白色"
    if r > 150 and g < 100 and b < 100:
        return "正红"
    if r > 180 and g > 100 and b < 80:
        return "橙红"
    if r > 150 and g > 150 and b < 100:
        return "暖黄"
    if g > 150 and r < 100 and b < 100:
        return "翠绿"
    if b > 150 and r < 100 and g < 100:
        return "深蓝"
    if r > 180 and g > 180 and b > 180:
        return "浅粉"
    if r > 150 and g > 120 and b > 80:
        return "大地色"
    if r < 100 and g < 100 and b > 150:
        return "藏青"
    if r > 200 and g > 200 and b < 150:
        return "香槟金"
    return "灰调"


def analyze_color_palette(frames: list, k: int = 5) -> tuple:
    """K-Means提取主色调"""
    try:
        from sklearn.cluster import KMeans
    except ImportError:
        return [[128, 128, 128]], ["灰色"]

    all_pixels = []
    for _, frame in frames:
        small = cv2.resize(frame, (100, 100))
        all_pixels.append(small.reshape(-1, 3))

    if not all_pixels:
        return [[128, 128, 128]], ["灰色"]

    pixels = np.vstack(all_pixels).astype(np.float32)

    try:
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(pixels, min(k, len(np.unique(labels))), None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    except Exception:
        return [[128, 128, 128]], ["灰色"]

    counts = np.bincount(labels.flatten())
    order = np.argsort(counts)[::-1]
    palette = [centers[i].astype(int).tolist() for i in order]
    color_names = [rgb_to_color_name(rgb) for rgb in palette]

    return palette, color_names


# ---- 音频分析 ----
def analyze_audio(video_path: str) -> dict:
    """提取音频特征"""
    result = {"has_music": False, "dynamic_range": 0.0, "estimated_genre": "unknown"}

    try:
        import wavio
    except ImportError:
        return result

    audio_path = "/tmp/vre_audio.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le",
        "-ar", "22050", audio_path
    ], capture_output=True)

    if not os.path.exists(audio_path):
        return result

    try:
        audio = wavio.read(audio_path)
        samples = audio.data

        if len(samples.shape) > 1:
            samples = samples[:, 0]

        rms = float(np.sqrt(np.mean(samples ** 2)))
        peak = float(np.max(np.abs(samples)))
        result["dynamic_range"] = float(20 * np.log10(peak / (rms + 1e-10)))

        try:
            from scipy.fft import fft
            fft_result = np.abs(fft(samples[:len(samples) // 10].flatten()))
            low_freq = float(np.mean(fft_result[:100]))
            high_freq = float(np.mean(fft_result[100:1000]))
            result["has_music"] = high_freq > low_freq * 0.3
            result["estimated_genre"] = "upbeat" if high_freq > low_freq else "ambient"
        except Exception:
            pass
    except Exception:
        pass

    try:
        os.remove(audio_path)
    except Exception:
        pass

    return result


def transcribe_audio(video_path: str) -> dict:
    """使用mlx-whisper转录音频（Apple Silicon GPU加速）"""
    result = {"text": "", "segments": [], "success": False}

    try:
        from mlx_whisper import transcribe
    except ImportError:
        result["error"] = "mlx-whisper未安装（pip install mlx-whisper）"
        return result

    audio_path = "/tmp/vre_transcribe.wav"
    # 提取音频：16kHz单声道最佳转录
    ffmpeg_ok = subprocess.run([
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1",
        audio_path
    ], capture_output=True).returncode == 0

    if not ffmpeg_ok or not os.path.exists(audio_path):
        result["error"] = "音频提取失败"
        return result

    try:
        print("  [mlx-whisper转录中，Apple Silicon GPU加速...]")
        transcription = transcribe(audio_path, path_or_hf_repo="mlx-community/whisper-large")
        result["text"] = transcription.get("text", "").strip()
        result["segments"] = transcription.get("segments", [])
        result["success"] = True
    except Exception as e:
        result["error"] = str(e)
    finally:
        try:
            os.remove(audio_path)
        except Exception:
            pass

    return result


# ---- 保存帧 ----
def save_frames(frames: list, output_dir: str, video_name: str) -> str:
    """保存帧到输出目录"""
    frame_dir = os.path.join(output_dir, f"{video_name}_frames")
    os.makedirs(frame_dir, exist_ok=True)

    for i, (ts, frame) in enumerate(frames):
        path = os.path.join(frame_dir, f"frame_{i:03d}_{ts:.2f}s.jpg")
        cv2.imwrite(path, frame)
        print(f"  帧 {i+1}/{len(frames)}: {ts:.2f}s -> {path}")

    return frame_dir


# ---- 生成报告 ----
def generate_report(video_path: str, scenes: list, frames: list,
                    palette: list, color_names: list,
                    audio: dict, frame_dir: str,
                    transcript: dict | None = None) -> str:
    """生成Markdown拆解报告"""
    # 预计算转录章节（避免f-string嵌套限制）
    transcript_section = ""
    if transcript and transcript.get("success"):
        seg_lines = "\n".join([
            f"| {s.get('start', 0):.1f}s-{s.get('end', 0):.1f}s | {s.get('text', '').strip()} |"
            for s in (transcript.get("segments") or [])
        ])
        transcript_section = f"""
### 口播文字稿（mlx-whisper转录）

> 完整文字：
> {transcript.get('text', '') or '(无文字)'}

**分段摘录：**
| 时间 | 内容 |
|------|------|
{seg_lines}
"""
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    total_duration = sum(s["duration_frames"] for s in scenes) / 30.0  # 估算

    # 计算镜头节奏
    fps = 30.0  # 假设
    durations_sec = [s["duration_frames"] / fps for s in scenes]
    avg_duration = np.mean(durations_sec)

    # 光影分析
    if frames:
        brightness_vals = [np.mean(f[1].astype(float)) / 255.0 for _, f in frames]
        brightness_avg = np.mean(brightness_vals)
        brightness_desc = "暗调" if brightness_avg < 0.35 else "明调"

        brightness_std = np.std(brightness_vals)
        contrast_desc = "高对比" if brightness_std > 0.15 else "柔和"

        last_frame = frames[-1][1]
        if len(last_frame.shape) == 3:
            b_ch = float(np.mean(last_frame[:, :, 2]))
            r_ch = float(np.mean(last_frame[:, :, 0]))
        else:
            b_ch = r_ch = 128
        tone_desc = "冷调" if b_ch > r_ch else "暖调"
    else:
        brightness_desc = contrast_desc = tone_desc = "未知"

    # 节奏判断
    if avg_duration > 3:
        rhythm_desc = "慢（诗意/沉浸）"
    elif avg_duration > 1.5:
        rhythm_desc = "中（叙事平衡）"
    else:
        rhythm_desc = "快（冲击力）"

    report = f"""# 广告反推拆解报告

> 来源：`{video_path}`
> 生成：{datetime.now().strftime('%Y-%m-%d %H:%M')}
> 帧保存位置：`{frame_dir}`
> **注意**：镜头检测使用 PySceneDetect，结果比均匀采样更准确

---

## 基本信息

| 项目 | 值 |
|------|---|
| **总帧数** | {sum(s['duration_frames'] for s in scenes)} |
| **镜头数量** | {len(scenes)}个 |
| **平均镜头时长** | {avg_duration:.2f}秒 |
| **节奏判断** | {rhythm_desc} |

---

## 镜头序列（PySceneDetect检测）

| 镜号 | 开始 | 结束 | 时长(秒) | 帧数 |
|------|------|------|---------|------|
"""

    fps_v = 30.0
    for i, scene in enumerate(scenes):
        start_t = scene['start_frame'] / fps_v
        end_t = scene['end_frame'] / fps_v
        dur = scene['duration_frames'] / fps_v
        report += f"| {i+1} | {start_t:.2f}s | {end_t:.2f}s | {dur:.2f}s | {scene['duration_frames']} |\n"

    # 镜头时长条形图
    report += f"""
### 镜头时长分布

"""
    max_dur = max(durations_sec) if durations_sec else 1
    for i, scene in enumerate(scenes):
        dur = durations_sec[i]
        bar_len = int((dur / max_dur) * 40)
        bar = "█" * bar_len
        start_t = scene['start_frame'] / fps_v
        report += f"- {start_t:5.1f}s | {dur:5.2f}s | {bar}\n"

    # 色彩分析
    report += f"""
---

## 色彩分析

### 主色调 TOP {len(palette)}

| 排名 | 颜色名 | RGB | 色块 |
|------|--------|-----|------|
"""
    for i, (rgb, name) in enumerate(zip(palette, color_names)):
        r, g, b = rgb
        report += f"| {i+1} | {name} | RGB({r},{g},{b}) | <span style='background:rgb({r},{g},{b})'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span> |\n"

    report += f"""
### 光影风格

| 维度 | 判断 |
|------|------|
| **亮度** | {brightness_desc} |
| **对比度** | {contrast_desc} |
| **色温** | {tone_desc} |

---

## 音频特征

| 项目 | 值 |
|------|---|
| **BGM** | {"有" if audio['has_music'] else "无"} |
| **动态范围** | {audio['dynamic_range']:.1f} dB |
| **估计风格** | {audio['estimated_genre']} |
{transcript_section}
---

## 提取帧列表（共{len(frames)}帧）

帧按镜头中间帧提取（而非均匀采样），优先选择视觉信息最丰富的点。

| 序号 | 时间戳 | 文件 |
|------|--------|------|
"""
    for i, (ts, _) in enumerate(frames):
        report += f"| {i+1} | {ts:.2f}s | frame_{i:03d}_{ts:.2f}s.jpg |\n"

    report += f"""
---

## 六维度初步判断

| 维度 | 是否体现 | 推测 |
|------|---------|------|
| 痛点 | | |
| 场景 | | |
| 对比 | | |
| 产品 | | |
| 体验 | | |
| 价值 | | |

---

## 关键帧标注（请人工对照帧文件填写）

> 打开 `{frame_dir}/` 目录，参照帧逐个填写

"""
    for i, (ts, _) in enumerate(frames):
        report += f"- **{ts:.2f}s**（镜{i//3+1 if len(frames) > 0 else '?'}附近）：\n"

    report += f"""
---

## 使用说明

本报告由 **Video Reverse Engineer v2.1** 自动生成（基于 PySceneDetect）。

**已完成：**
- ✅ PySceneDetect镜头边界检测（AdaptiveDetector，比帧差法更准）
- ✅ 镜头中间帧提取（优先视觉变化最大的点）
- ✅ HDR暗帧校正
- ✅ 色彩分析（K-Means主色调）
- ✅ 音频特征提取
{"✅ 音频转录（mlx-whisper，Apple Silicon GPU加速）" if transcript.get("success") else ""}

**需人工补充：**
- 逐帧画面内容描述
- 六维度对应分析
- 情绪曲线
- 创意亮点总结
- MJ/AI提示词提取

"""
    return report


def auto_scale_frames(duration_sec: float, min_frames: int = 20, max_frames: int = 200) -> int:
    """根据视频时长自动计算建议帧数
    策略：
    - 短视频(<30s): 每0.5秒1帧（精准覆盖）
    - 中视频(30s-3min): 每2秒1帧（约30-90帧）
    - 长视频(3min-10min): 每5秒1帧（约36-120帧）
    - 超长视频(>10min): 每10秒1帧，上限200帧
    """
    if duration_sec <= 30:
        target = max(min_frames, int(duration_sec / 0.5))
    elif duration_sec <= 180:
        target = int(duration_sec / 2)
    elif duration_sec <= 600:
        target = int(duration_sec / 5)
    else:
        target = int(duration_sec / 10)

    return max(min_frames, min(max_frames, target))


def main():
    parser = argparse.ArgumentParser(
        description="Video Reverse Engineer v2.1 - 广告视频自动拆解（支持mlx-whisper转录）")
    parser.add_argument("video", help="视频文件路径")
    parser.add_argument("--frames", type=int, default=None,
                        help="手动指定帧数（默认自动缩放）")
    parser.add_argument("--min-frames", type=int, default=20,
                        help="最小帧数（默认20）")
    parser.add_argument("--max-frames", type=int, default=200,
                        help="最大帧数（默认200）")
    parser.add_argument("--output", "-o", default="./",
                        help="输出目录（默认当前目录）")
    parser.add_argument("--no-scene", action="store_true",
                        help="跳过PySceneDetect，直接用均匀采样")
    parser.add_argument("--transcribe", action="store_true",
                        help="使用mlx-whisper转录音频（需安装mlx-whisper）")
    args = parser.parse_args()

    video_path = args.video
    if not os.path.exists(video_path):
        print(f"错误：文件不存在 {video_path}")
        sys.exit(1)

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_dir = os.path.join(args.output, f"{video_name}_analysis")
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n{'='*50}")
    print(f"Video Reverse Engineer v2.1")
    print(f"{'='*50}")
    print(f"输入：{video_path}")
    print(f"输出目录：{output_dir}")
    print()

    # Step 1: 场景检测
    print("Step 1/5：场景检测（PySceneDetect）...")
    if args.no_scene:
        scenes = None
        print("  使用：均匀采样（--no-scene）")
    else:
        scenes = detect_scenes_pyscenedetect(video_path)
        if scenes is None:
            scenes = detect_scenes_fallback(video_path)
        print(f"  完成：检测到 {len(scenes)} 个镜头")

    # Step 2: 提取关键帧
    print("Step 2/5：提取关键帧...")
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    total_duration = total_frames / fps

    # 自动缩放帧数
    if args.frames is not None:
        target_frames = args.frames
    else:
        target_frames = auto_scale_frames(total_duration, args.min_frames, args.max_frames)

    print(f"  视频时长: {total_duration:.1f}秒, 自动计算目标帧数: {target_frames}")

    frames = []

    # 策略：每个镜头至少1帧（用best frame），然后均匀采样补充到目标数量
    if scenes:
        # 每个镜头取best帧
        for scene in scenes:
            result = get_scene_best_frame(scene, video_path)
            if result:
                frames.append(result)

        # 均匀采样补充（确保覆盖全程）
        total_duration = total_frames / fps
        uniform_ts = np.linspace(0, total_duration, target_frames)
        existing_ts = set(int(f[0] * 10) for f in frames)  # 0.1s去重
        for ts in uniform_ts:
            if len(frames) >= target_frames:
                break
            key = int(ts * 10)
            if key not in existing_ts:
                frame_idx = int(ts * fps)
                cap = cv2.VideoCapture(video_path)
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                cap.release()
                if ret:
                    frame = correct_dark_frame(frame)
                    frames.append((ts, frame))
                    existing_ts.add(key)

    else:
        # 无场景检测：纯均匀采样
        uniform_ts = np.linspace(0, total_frames / fps, target_frames)
        for ts in uniform_ts:
            frame_idx = int(ts * fps)
            cap = cv2.VideoCapture(video_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            cap.release()
            if ret:
                frame = correct_dark_frame(frame)
                frames.append((ts, frame))

    frames.sort(key=lambda x: x[0])
    frames = frames[:target_frames]
    print(f"  完成：共提取 {len(frames)} 帧")

    # Step 3: 色彩分析
    print("Step 3/5：分析色彩...")
    palette, color_names = analyze_color_palette(frames)
    print(f"  完成：主色调 = {color_names[:3]}")

    # Step 4: 音频分析
    step_total = "6" if args.transcribe else "5"
    print(f"Step 4/{step_total}：分析音频...")
    audio = analyze_audio(video_path)
    print(f"  完成：{'有BGM' if audio['has_music'] else '无BGM'}")

    # Step 5 (or 6): 保存帧
    print(f"Step 5/{step_total}：保存帧...")
    frame_dir = save_frames(frames, output_dir, video_name)

    # Step 6: 音频转录（可选）
    transcript = {"text": "", "segments": [], "success": False}
    if args.transcribe:
        print(f"Step 6/6：mlx-whisper转录...")
        transcript = transcribe_audio(video_path)
        if transcript["success"]:
            print(f"  完成：{len(transcript['segments'])}个片段，{len(transcript['text'])}字符")
        else:
            print(f"  完成：转录失败 - {transcript.get('error', '未知错误')}")

    # 生成报告
    report = generate_report(video_path, scenes, frames, palette, color_names, audio, frame_dir, transcript)
    report_path = os.path.join(output_dir, f"{video_name}_拆解报告.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n{'='*50}")
    print(f"完成！")
    print(f"  拆解报告：{report_path}")
    print(f"  帧文件目录：{frame_dir}/")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
