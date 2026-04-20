#!/usr/bin/env python3
"""
Style Fusion Engine — B×A Matrix Prompt Generator
输入两个风格代码，自动融合并输出平台化提示词
"""

import json
import sys
import os
import argparse
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "style-database.json")


class StyleFusion:
    def __init__(self, db_path: str = DB_PATH):
        with open(db_path, "r", encoding="utf-8") as f:
            self.db = json.load(f)

    def get_b_style(self, code: str):
        return self.db["b_styles"].get(code.upper())

    def get_a_style(self, code: str):
        return self.db["a_styles"].get(code.upper())

    def get_combination(self, b_code: str, a_code: str):
        key = f"{b_code.upper()}×{a_code.upper()}"
        return self.db["combinations"].get(key)

    def get_fusion(self, b_code: str, a_code: str):
        """Get fusion params — exact match preferred, fallback to interpolation."""
        combo = self.get_combination(b_code, a_code)
        if combo:
            return {"source": "exact", "data": combo}
        # Interpolation fallback
        b_style = self.get_b_style(b_code)
        a_style = self.get_a_style(b_code)
        if not b_style or not a_style:
            return None
        return {"source": "interpolated", "data": self._interpolate(b_style, a_style)}

    def _interpolate(self, b_style: dict, a_style: dict) -> dict:
        """Weighted blend: B 60% + A 40%."""
        def blend_str(b: str, a: str) -> str:
            return f"{b} × {a}"

        return {
            "fusion_core": blend_str(b_style.get("category", ""), a_style.get("fusion_core", "")),
            "palette": {
                "primary": b_style["palette"].get("primary", ""),
                "secondary": b_style["palette"].get("secondary", ""),
                "accent": a_style["palette"].get("accent", ""),
            },
            "lighting": blend_str(b_style.get("lighting", ""), a_style.get("lighting", "")),
            "composition": blend_str(b_style.get("composition", ""), a_style.get("composition", "")),
            "rhythm": blend_str(b_style.get("rhythm", ""), a_style.get("rhythm", "")),
            "texture": blend_str(b_style.get("texture", ""), a_style.get("texture", "")),
            "mj_params": b_style.get("mj_params", {}),
        }

    def to_schema(self, fusion: dict, title: str = "Style Fusion") -> dict:
        """Convert fusion to video-prompt-schema JSON."""
        data = fusion["data"]
        mj = data.get("mj_params", {})
        s_range = mj.get("s_range", [200, 300])
        s_mid = (s_range[0] + s_range[1]) // 2

        return {
            "meta": {
                "title": title,
                "platform": "seedance",
                "duration": 15,
                "style_line": data.get("category", "通用线"),
                "director_style": [data.get("directors", [""])[0]] if isinstance(data.get("directors"), list) else [],
                "fusion_core": data.get("fusion_core", ""),
                "source": fusion.get("source", "unknown"),
            },
            "palette": data.get("palette", {}),
            "lighting": data.get("lighting", ""),
            "composition": data.get("composition", ""),
            "rhythm": data.get("rhythm", ""),
            "texture": data.get("texture", ""),
            "mj_params": {
                "ar": mj.get("ar", "2.35:1"),
                "s": s_mid,
                "s_range": s_range,
                "c_range": mj.get("c_range"),
                "weird_range": mj.get("weird_range"),
            },
            "sample_prompts": data.get("sample_prompts", []),
        }

    def to_seedance(self, schema: dict) -> str:
        """Generate Seedance 2.0 formatted prompt."""
        meta = schema["meta"]
        pal = schema["palette"]
        mj = schema["mj_params"]
        s_range = mj.get("s_range", [200, 300])
        s_mid = (s_range[0] + s_range[1]) // 2

        # Build palette string
        primary = pal.get("primary", "")
        secondary = pal.get("secondary", "")
        accent = pal.get("accent", "")

        palette_str = f"{primary}"
        if secondary:
            palette_str += f"，{secondary}"
        if accent:
            palette_str += f"，{accent}"

        # Pick a sample prompt or build one
        samples = schema.get("sample_prompts", [])
        if samples:
            sample_en = samples[0]
        else:
            sample_en = f"{meta.get('fusion_core', 'cinematic scene')}"

        lines = [
            f"白梦客[{meta.get('style_line', '通用线')}]，{meta.get('fusion_core', '')}。",
            "",
            f"[核心场景]: {sample_en}",
            "",
            f"色调：{palette_str}",
            f"光影：{schema.get('lighting', '')}",
            f"构图：{schema.get('composition', '')}",
            f"质感：{schema.get('texture', '')}",
            f"节奏：{schema.get('rhythm', '')}",
            "",
            f"参考：{', '.join(meta.get('director_style', []))}",
            f"格式：2.35:1，{mj.get('ar', '2.35:1')}，{s_mid}风格值",
        ]

        return "\n".join(lines)

    def to_vidu(self, schema: dict) -> str:
        """Generate Vidu formatted prompt (中英混合)."""
        meta = schema["meta"]
        pal = schema["palette"]

        palette_str = f"{pal.get('primary', '')}, {pal.get('secondary', '')}, {pal.get('accent', '')}"
        samples = schema.get("sample_prompts", [])
        sample = samples[1] if len(samples) > 1 else (samples[0] if samples else "")

        lines = [
            f"{meta.get('fusion_core', 'cinematic scene')}",
            "",
            f"[Style] {meta.get('director_style', ['cinematic'])[0] if meta.get('director_style') else 'cinematic'} aesthetic",
            f"[Palette] {palette_str}",
            f"[Lighting] {schema.get('lighting', '')}",
            f"[Texture] {schema.get('texture', '')}",
            "",
            f"{sample}",
        ]
        return "\n".join(lines)

    def to_hairui(self, schema: dict) -> str:
        """Generate 海螺 formatted prompt (中文，图像转视频)."""
        meta = schema["meta"]
        pal = schema["palette"]
        samples = schema.get("sample_prompts", [])
        sample_cn = samples[0] if samples else ""

        lines = [
            f"【{meta.get('title', '风格融合')}】",
            f"融合核心：{meta.get('fusion_core', '')}",
            f"风格线：{meta.get('style_line', '通用线')}",
            "",
            f"[画面描述]",
            f"{sample_cn}",
            "",
            f"[色调] {pal.get('primary', '')}",
            f"[光影] {schema.get('lighting', '')}",
            f"[质感] {schema.get('texture', '')}",
            f"[构图] {schema.get('composition', '')}",
            "",
            f"动态预期：缓慢推进，氛围感强，色调统一",
        ]
        return "\n".join(lines)

    def to_mj_prompt(self, schema: dict) -> str:
        """Generate MidJourney prompt string."""
        mj = schema["mj_params"]
        samples = schema.get("sample_prompts", [])
        sample = samples[0] if samples else ""

        ar = mj.get("ar", "2.35:1")
        s_range = mj.get("s_range", [200, 300])
        c_range = mj.get("c_range")
        weird_range = mj.get("weird_range")

        parts = [sample] if sample else []

        params = [f"--ar {ar}", f"--s {s_range[0]}-{s_range[1]}"]
        if c_range:
            params.append(f"--chaos {c_range[0]}-{c_range[1]}")
        if weird_range:
            params.append(f"--weird {weird_range[0]}-{weird_range[1]}")

        return ", ".join(parts + params)


def main():
    parser = argparse.ArgumentParser(description="Style Fusion: B×A Matrix Prompt Generator")
    parser.add_argument("b_code", help="B-style code (B1-B5)")
    parser.add_argument("a_code", help="A-style code (A1-A4)")
    parser.add_argument("--platform", default="all", choices=["seedance", "vidu", "hairui", "mj", "all"],
                        help="Target platform (default: all)")
    parser.add_argument("--duration", type=int, default=15, help="Video duration in seconds")
    parser.add_argument("--output", default="both", choices=["schema", "prompt", "both"],
                        help="Output format (default: both)")
    parser.add_argument("--title", default="Style Fusion", help="Project title")

    args = parser.parse_args()

    engine = StyleFusion()

    # Validate codes
    b_upper = args.b_code.upper()
    a_upper = args.a_code.upper()

    if b_upper not in ["B1", "B2", "B3", "B4", "B5"]:
        print(f"Error: B-code must be B1-B5, got '{args.b_code}'", file=sys.stderr)
        sys.exit(1)
    if a_upper not in ["A1", "A2", "A3", "A4"]:
        print(f"Error: A-code must be A1-A4, got '{args.a_code}'", file=sys.stderr)
        sys.exit(1)

    fusion = engine.get_fusion(b_upper, a_upper)
    if not fusion:
        print("Error: Could not resolve fusion", file=sys.stderr)
        sys.exit(1)

    schema = engine.to_schema(fusion, args.title)
    schema["meta"]["duration"] = args.duration

    combo_key = f"{b_upper}×{a_upper}"

    # Header
    print(f"{'='*60}")
    print(f"  STYLE FUSION: {combo_key}")
    print(f"  融合核心: {schema['meta']['fusion_core']}")
    print(f"  来源: {fusion['source']}")
    print(f"{'='*60}")
    print()

    # Schema output
    if args.output in ["schema", "both"]:
        print("--- SCHEMA (JSON) ---")
        print(json.dumps(schema, ensure_ascii=False, indent=2))
        print()

    # Platform prompts
    if args.output in ["prompt", "both"]:
        if args.platform in ["seedance", "all"]:
            print("--- SEEDANCE 提示词 ---")
            print(engine.to_seedance(schema))
            print()

        if args.platform in ["vidu", "all"]:
            print("--- VIDU 提示词 ---")
            print(engine.to_vidu(schema))
            print()

        if args.platform in ["hairui", "all"]:
            print("--- 海螺 提示词 ---")
            print(engine.to_hairui(schema))
            print()

        if args.platform in ["mj", "all"]:
            print("--- MidJourney Prompt ---")
            print(engine.to_mj_prompt(schema))
            print()


if __name__ == "__main__":
    main()
