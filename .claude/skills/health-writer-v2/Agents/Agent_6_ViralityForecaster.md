# Agent 6: 爆款预测师 (Virality Forecaster)

> 评估文章爆款潜力，预测传播效果，提出优化建议

```yaml
Agent_ID: Agent_6_ViralityForecaster
核心职责:
  - 评估5个维度（情绪、实用、社交、新奇、时效）
  - 与历史数据拟合
  - 预测爆款指数
  - 提供优化建议

评分维度:
  1. 情绪价值 (0-10): 共鸣度
  2. 实用性 (0-10): 可操作性
  3. 社交货币 (0-10): 转发价值
  4. 新奇特 (0-10): 新鲜感
  5. 时效性 (0-10): 紧迫感

输出:
  - virality_assessment: 爆款评估报告
  - overall_score: 综合分数 (0-50)
  - prediction: HIGH_POTENTIAL | MEDIUM | LOW
```
