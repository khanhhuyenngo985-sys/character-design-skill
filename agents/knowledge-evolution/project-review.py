#!/usr/bin/env python3
"""
项目复盘Agent - 自动学习进化系统

触发方式：
1. 项目交付后自动触发
2. 用户说"复盘"手动触发

功能：
1. 收集项目所有产出物
2. 分析成功和失败点
3. 生成复盘报告
4. 沉淀到知识库
5. 通知相关Agent更新
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 知识库路径
KNOWLEDGE_BASE = Path("/Users/baimengke/Documents/白梦客知识库")
PROJECT_REVIEW_DIR = KNOWLEDGE_BASE / "项目复盘"
SUCCESS_PROMPTS = KNOWLEDGE_BASE / "04-行业知识/AI视频提示词库/优秀提示词范例.md"
FAILURE_CASES = KNOWLEDGE_BASE / "01-导演组/失败案例库.md"
EVOLUTION_LOG = KNOWLEDGE_BASE / "🏠 知识库进化日志.md"
METRICS_FILE = KNOWLEDGE_BASE / "03-选题与运营/agent-metrics.json"

# 项目复盘目录
PROJECT_REVIEW_DIR.mkdir(exist_ok=True)


class BenchmarkMetrics:
    """追踪 Creative Team Agent 任务完成率"""

    def __init__(self):
        self.metrics_file = METRICS_FILE
        self.data = self._load()

    def _load(self) -> Dict:
        if self.metrics_file.exists():
            return json.loads(self.metrics_file.read_text())
        return {"projects": [], "agent_stats": {}}

    def _save(self):
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        self.metrics_file.write_text(json.dumps(self.data, ensure_ascii=False, indent=2))

    def record_project(self, project_name: str, phase: str, success: bool,
                      retries: int = 0, cost_tokens: int = 0):
        """记录单个项目的完成情况"""
        entry = {
            "project": project_name,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "phase": phase,
            "success": success,
            "retries": retries,
            "cost_tokens": cost_tokens
        }
        self.data["projects"].append(entry)
        self._update_agent_stats(phase, success, retries)
        self._save()

    def _update_agent_stats(self, phase: str, success: bool, retries: int):
        if phase not in self.data["agent_stats"]:
            self.data["agent_stats"][phase] = {
                "total": 0, "success": 0, "retries_sum": 0
            }
        stats = self.data["agent_stats"][phase]
        stats["total"] += 1
        if success:
            stats["success"] += 1
        stats["retries_sum"] += retries

    def get_stats(self, phase: str = None) -> Dict:
        """获取统计数据"""
        if phase:
            stats = self.data["agent_stats"].get(phase, {})
            if stats["total"] == 0:
                return {"pass@1": 0, "avg_retries": 0, "total": 0}
            return {
                "pass@1": stats["success"] / stats["total"],
                "avg_retries": stats["retries_sum"] / stats["total"],
                "total": stats["total"]
            }
        # 全局统计
        all_projects = self.data["projects"]
        if not all_projects:
            return {"overall_pass@1": 0, "total_projects": 0}
        successes = sum(1 for p in all_projects if p["success"])
        return {
            "overall_pass@1": successes / len(all_projects),
            "total_projects": len(all_projects)
        }


class ProjectReviewAgent:

    def collect_artifacts(self) -> Dict[str, List[Path]]:
        """收集项目产出物"""
        artifacts = {
            "scripts": [],      # 脚本文件
            "prompts": [],      # 提示词文件
            "boards": [],       # 分镜文件
            "videos": [],       # 视频文件
            "feedback": []      # 用户反馈
        }

        if not self.project_path.exists():
            return artifacts

        for f in self.project_path.rglob("*"):
            if f.is_file():
                ext = f.suffix.lower()
                if ext in [".md"]:
                    if "脚本" in f.name or "script" in f.name.lower():
                        artifacts["scripts"].append(f)
                    elif "提示词" in f.name or "prompt" in f.name.lower():
                        artifacts["prompts"].append(f)
                    elif "分镜" in f.name or "board" in f.name.lower():
                        artifacts["boards"].append(f)
                elif ext in [".mp4", ".mov", ".avi"]:
                    artifacts["videos"].append(f)
                elif ext in [".txt", ".json"]:
                    if "反馈" in f.name or "feedback" in f.name.lower():
                        artifacts["feedback"].append(f)

        return artifacts

    def analyze_success_prompts(self, prompts: List[Path]) -> List[Dict]:
        """分析成功的提示词"""
        success_list = []

        for p in prompts:
            # 简单分析：读取提示词内容
            # 实际应该让Agent判断效果
            content = p.read_text() if p.exists() else ""

            # 这里可以调用Agent来做更深入的分析
            # 暂时简单处理
            if len(content) > 50:  # 有实质内容的
                success_list.append({
                    "source": str(p),
                    "summary": content[:200] + "..." if len(content) > 200 else content
                })

        return success_list

    def analyze_failure_cases(self, artifacts: Dict) -> List[Dict]:
        """分析失败案例"""
        failures = []

        # 从反馈文件中读取失败点
        for fb in artifacts.get("feedback", []):
            content = fb.read_text() if fb.exists() else ""
            if content:
                failures.append({
                    "source": str(fb),
                    "issue": content
                })

        # 从项目路径中查找是否有失败记录
        failure_file = self.project_path / "失败记录.md"
        if failure_file.exists():
            failures.append({
                "source": str(failure_file),
                "issue": failure_file.read_text()
            })

        return failures

    def generate_improvements(self, artifacts: Dict) -> List[str]:
        """生成改进建议"""
        improvements = []

        # 基于分析生成建议
        if len(artifacts.get("prompts", [])) == 0:
            improvements.append("下次项目中提示词要及时保存")

        if len(artifacts.get("videos", [])) > 0:
            improvements.append("生成的视频片段要及时归档")

        # 可以让Agent基于项目实际情况生成更具体的建议
        improvements.append("下次项目开始前先查阅失败案例库")

        return improvements

    def deposit_to_knowledge_base(self):
        """沉淀到知识库"""
        deposits = []

        # 1. 沉淀好提示词
        if self.review_report["success"]:
            self._deposit_success_prompts()
            deposits.append("好提示词 → 优秀提示词范例.md")

        # 2. 沉淀失败案例
        if self.review_report["failure"]:
            self._deposit_failure_cases()
            deposits.append("失败案例 → 失败案例库.md")

        # 3. 生成复盘报告
        self._generate_review_report()

        # 4. 更新进化日志
        self._update_evolution_log()

        self.review_report["deposits"] = deposits
        return deposits

    def _deposit_success_prompts(self):
        """沉淀成功提示词到知识库"""
        if not SUCCESS_PROMPTS.exists():
            # 创建文件
            SUCCESS_PROMPTS.parent.mkdir(parents=True, exist_ok=True)
            content = "# 优秀提示词范例\n\n"
        else:
            content = SUCCESS_PROMPTS.read_text()

        # 追加新提示词
        content += f"\n---\n\n## {self.project_name} ({self.date})\n\n"
        for item in self.review_report["success"]:
            content += f"### 来源：{item['source']}\n\n"
            content += f"```\n{item['summary']}\n```\n\n"

        SUCCESS_PROMPTS.write_text(content)

    def _deposit_failure_cases(self):
        """沉淀失败案例到知识库"""
        if not FAILURE_CASES.exists():
            # 创建文件
            FAILURE_CASES.parent.mkdir(parents=True, exist_ok=True)
            content = "# 失败案例库\n\n> 记录每个项目的失败点和教训，避免重复踩坑\n\n"
        else:
            content = FAILURE_CASES.read_text()

        # 追加新失败案例
        content += f"\n---\n\n## {self.project_name} ({self.date})\n\n"
        for item in self.review_report["failure"]:
            content += f"### 问题：{item['source']}\n\n"
            content += f"{item['issue']}\n\n"

        FAILURE_CASES.write_text(content)

    def _generate_review_report(self):
        """生成复盘报告"""
        report_path = PROJECT_REVIEW_DIR / f"{self.project_name}_{self.date}.md"

        content = f"""# 项目复盘报告：{self.project_name}

## 基本信息
- 日期：{self.date}
- 项目名：{self.project_name}
- 项目路径：{self.project_path}

## ★ 成功了什么？

"""
        for item in self.review_report["success"]:
            content += f"### 来源：{item['source']}\n"
            content += f"```\n{item['summary']}\n```\n\n"

        content += "\n## ★ 失败了什么？\n\n"
        for item in self.review_report["failure"]:
            content += f"### 问题：{item['source']}\n"
            content += f"{item['issue']}\n\n"

        content += "\n## ★ 下次注意什么？\n\n"
        for i, imp in enumerate(self.review_report["improvements"], 1):
            content += f"{i}. {imp}\n"

        content += "\n## 沉淀清单\n\n"
        for dep in self.review_report["deposits"]:
            content += f"- {dep}\n"

        report_path.write_text(content)
        print(f"复盘报告已生成：{report_path}")

    def _update_evolution_log(self):
        """更新进化日志"""
        if not EVOLUTION_LOG.exists():
            return

        content = EVOLUTION_LOG.read_text()

        # 追加新记录
        new_entry = f"""
### {self.date} - {self.project_name} 复盘完成

**成功沉淀：**
"""
        for dep in self.review_report["deposits"]:
            new_entry += f"- {dep}\n"

        new_entry += "\n**改进建议：**\n"
        for imp in self.review_report["improvements"]:
            new_entry += f"- {imp}\n"

        # 在最后一行前插入
        content += new_entry

        EVOLUTION_LOG.write_text(content)

    def run(self) -> Dict:
        """运行复盘"""
        print(f"\n{'='*60}")
        print(f"  项目复盘Agent - {self.project_name}")
        print(f"{'='*60}\n")

        # 1. 收集产出物
        print("→ 收集项目产出物...")
        artifacts = self.collect_artifacts()
        print(f"  找到 {len(artifacts['prompts'])} 个提示词文件")
        print(f"  找到 {len(artifacts['scripts'])} 个脚本文件")
        print(f"  找到 {len(artifacts['videos'])} 个视频文件")

        # 2. 分析成功点
        print("\n→ 分析成功提示词...")
        self.review_report["success"] = self.analyze_success_prompts(
            artifacts.get("prompts", [])
        )
        print(f"  发现 {len(self.review_report['success'])} 个成功提示词")

        # 3. 分析失败点
        print("\n→ 分析失败案例...")
        self.review_report["failure"] = self.analyze_failure_cases(artifacts)
        print(f"  发现 {len(self.review_report['failure'])} 个失败点")

        # 4. 生成改进建议
        print("\n→ 生成改进建议...")
        self.review_report["improvements"] = self.generate_improvements(artifacts)
        for imp in self.review_report["improvements"]:
            print(f"  - {imp}")

        # 5. 沉淀到知识库
        print("\n→ 沉淀到知识库...")
        deposits = self.deposit_to_knowledge_base()
        for dep in deposits:
            print(f"  ✓ {dep}")

        # 6. 记录 Benchmark 指标
        print("\n→ 记录完成率指标...")
        metrics = BenchmarkMetrics()
        metrics.record_project(
            project_name=self.project_name,
            phase="project_review",
            success=len(self.review_report["failure"]) == 0,
            retries=0,  # 复盘阶段不计算 retries
            cost_tokens=0  # 暂不追踪 token 成本
        )
        stats = metrics.get_stats()
        print(f"  总体通过率: {stats['overall_pass@1']:.1%}")

        print(f"\n{'='*60}")
        print("  ✅ 复盘完成！")
        print(f"{'='*60}\n")

        return self.review_report


def main():
    if len(sys.argv) < 2:
        print("用法：python3 project-review.py <项目名称> [项目路径]")
        print("示例：python3 project-review.py 便利店广告 ./projects/便利店广告")
        sys.exit(1)

    project_name = sys.argv[1]
    project_path = sys.argv[2] if len(sys.argv) > 2 else f"./projects/{project_name}"

    agent = ProjectReviewAgent(project_name, project_path)
    result = agent.run()

    # 输出JSON格式结果（便于程序处理）
    print("\n--- 复盘结果（JSON）---")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
