---
name: workflow-metrics
description: 创意工作流量化评分系统，评估项目进度和质量指标。触发词：「评分」「量化」「进度」「质量指标」。
---

# 创意工作流量化评分系统

## 功能

自动评估创意工作流的执行质量，输出可量化的指标分数和改进建议。

## 评估触发时机

- 每个 Phase 完成后
- 项目交付时
- 每周自动汇总

## 核心指标

| 指标 | 描述 | 目标 | 计算方式 |
|------|------|------|----------|
| decision_log_completeness | 决策日志完整率 | >95% | 实际记录数/应记录数 |
| discussion_rounds_avg | 平均讨论轮次 | <3轮 | 总轮次/讨论次数 |
| reference_chain_coverage | 引用链覆盖率 | 100% | 有引用链的工件数/总工件数 |
| skill_routing_accuracy | 技能路由准确率 | >80% | 用户接受次数/推荐次数 |
| quality_gate_first_pass | 质量门首次通过率 | >70% | 首次通过/总提交 |
| user_intervention_rate | 用户干预率 | <30% | 干预次数/总阶段 |

## 评分计算方法

### 单项得分转换

```
decision_log_completeness: raw * 100
reference_chain_coverage: raw * 100
skill_routing_accuracy: raw * 100
quality_gate_first_pass: raw * 100
user_intervention_rate: (1 - raw) * 100  # 越低越好

discussion_rounds_avg: max(0, (5 - raw) / 5 * 100)  # 越少越好，<3轮得满分
```

### 权重

```json
{
  "decision_log_completeness": 0.2,
  "discussion_rounds_avg": 0.15,
  "reference_chain_coverage": 0.2,
  "skill_routing_accuracy": 0.15,
  "quality_gate_first_pass": 0.2,
  "user_intervention_rate": 0.1
}
```

### 综合得分

```python
overall = sum(single_score[k] * weight[k] for k in weight)
return round(overall, 1)  # 0-100
```

## 评分等级

| 等级 | 分数 | 说明 |
|------|------|------|
| A | 90-100 | 优秀，符合最佳实践 |
| B | 80-89 | 良好，有小幅改进空间 |
| C | 70-79 | 一般，存在明显问题 |
| D | 60-69 | 较差，需要重大改进 |
| F | <60 | 不合格，需立即整改 |

## 输出格式

### JSON 格式

```json
{
  "project": "[项目名]",
  "evaluated_at": "[ISO时间戳]",
  "phase": "[当前阶段]",
  "metrics": {
    "decision_log_completeness": 0.95,
    "discussion_rounds_avg": 2.3,
    "reference_chain_coverage": 1.0,
    "skill_routing_accuracy": 0.85,
    "quality_gate_first_pass": 0.75,
    "user_intervention_rate": 0.2
  },
  "scores": {
    "decision_log_completeness": 95.0,
    "discussion_rounds_avg": 54.0,
    "reference_chain_coverage": 100.0,
    "skill_routing_accuracy": 85.0,
    "quality_gate_first_pass": 75.0,
    "user_intervention_rate": 80.0
  },
  "overall_score": 85.5,
  "grade": "B",
  "issues": [
    { "metric": "discussion_rounds_avg", "severity": "medium", "detail": "Phase 3 讨论了4轮" }
  ],
  "recommendations": [
    "建议在 Phase 3 增加预讨论，减少正式讨论轮次"
  ]
}
```

### 人类可读格式

```
## 项目评分报告：[项目名]

**综合得分：85.5 (B)**

### 指标详情
| 指标 | 数值 | 得分 |
|------|------|------|
| 决策日志完整率 | 95% | 95.0 |
| 平均讨论轮次 | 2.3轮 | 54.0 |
| 引用链覆盖率 | 100% | 100.0 |
| 技能路由准确率 | 85% | 85.0 |
| 质量门首次通过率 | 75% | 75.0 |
| 用户干预率 | 20% | 80.0 |

### 问题
- [中] Phase 3 讨论了4轮，建议增加预讨论

### 优化建议
1. 建议在 screenwriter agent 指令中增加决策日志检查点
```

## 使用方法

1. 在 Phase 结束时，AI 自动运行评分
2. 读取 project_state.json 和 decision_log.md
3. 计算各项指标
4. 输出评分报告
5. 如有严重问题（等级D/F），暂停项目并要求整改

## 自动触发

在以下节点自动触发评分：
- Phase 2 完成后（创意方向确认）
- Phase 3-4 完成后（前期创作完成）
- Phase 5 完成后（剧本定稿）
- Phase 6 完成后（质量门通过）
- Phase 8 完成后（项目交付）
