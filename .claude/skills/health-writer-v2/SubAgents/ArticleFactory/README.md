# ArticleFactory SubAgent - 快速开始指南

## 📖 简介

**ArticleFactory** 是 Health Writer V2 系统的核心 SubAgent，负责协调多个专业 Agent（Agent 2-7），一键生成爆款养生文章。

### 核心价值

- ✅ **一键生成**：从话题到成稿，全程自动化
- ✅ **智能路由**：自动处理修改循环，优化文章质量
- ✅ **多种模式**：标准/应急/高质量，灵活应对不同场景
- ✅ **UCO 跟踪**：完整的状态管理和日志记录
- ✅ **老李人设**：确保所有内容符合老李的人设风格

---

## 🚀 快速开始

### 1. 基本使用

```python
from implementation import ArticleFactory

# 创建工厂实例
factory = ArticleFactory()

# 生成文章
result = factory.generate_article(
    topic="立春养肝",
    topic_source="CHRONOS_RECOMMENDATION",
    target_audience={
        "age_group": "60-70",
        "gender": "all"
    }
)

# 检查结果
if result["success"]:
    print(f"✅ 文章生成成功！")
    print(f"标题: {result['article']['title']}")
    print(f"字数: {result['article']['word_count']}")
    print(f"耗时: {result['workflow_report']['total_time']} 分钟")
else:
    print(f"❌ 生成失败: {result['error']}")
```

### 2. 应急模式

```python
# 应急模式（快速生成，约 1 小时）
result = factory.generate_article(
    topic="高温防暑",
    topic_source="EMERGENCY_EVENT",
    urgency="EMERGENCY",
    custom_requirements={
        "keywords": ["中暑", "防暑", "降温"],
        "min_length": 1500
    }
)
```

### 3. 高质量模式

```python
# 高质量模式（多轮优化，确保高质量）
result = factory.generate_article(
    topic="中老年人降糖方法",
    quality_level="HIGH",
    urgency="NORMAL"
)
```

---

## 📋 输入参数详解

### 必需参数

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `topic` | string | 文章话题 | "立春养肝" |

### 可选参数

| 参数 | 类型 | 说明 | 可选值 | 默认值 |
|------|------|------|--------|--------|
| `topic_source` | string | 话题来源 | USER_MANUAL, CHRONOS_RECOMMENDATION, VIRAL_TRENDING, EMERGENCY_EVENT | USER_MANUAL |
| `target_audience` | object | 目标受众 | {"age_group": "60-70", "gender": "all"} | null |
| `urgency` | string | 紧急程度 | NORMAL, HIGH, EMERGENCY | NORMAL |
| `quality_level` | string | 质量等级 | STANDARD, HIGH | STANDARD |
| `custom_requirements` | object | 自定义要求 | 见下文 | null |

### custom_requirements 结构

```python
custom_requirements = {
    "keywords": ["关键词1", "关键词2"],  # 必须包含的关键词
    "forbidden_words": ["禁止词1", "禁止词2"],  # 禁止出现的词汇
    "min_length": 1500,  # 最小字数
    "max_length": 3000,  # 最大字数
}
```

---

## 📤 输出结果说明

```python
{
    "success": True,  # 是否成功
    "uco_id": "UCO_20260120_143000",  # UCO 对象 ID
    "status": "READY",  # 最终状态

    "article": {
        "title": "立春养肝第一菜，90%的人都吃错了",
        "titles_generated": [...],  # 所有生成的标题（TOP 3）
        "content": "完整文章内容...",
        "word_count": 2480,
        "tags": ["立春", "养肝", "韭菜"]
    },

    "quality_metrics": {
        "virality_score": 38,  # 爆款分数 (0-50)
        "virality_prediction": "HIGH_POTENTIAL",
        "quality_score": 88,  # 质量分数 (0-100)
        "revision_count": 0  # 修改轮次
    },

    "workflow_report": {
        "total_time": 125.5,  # 总耗时（分钟）
        "mode": "STANDARD",
        "agent_execution_log": [...],  # 各 Agent 执行日志
        "routing_decisions": [...],  # 路由决策记录
    },

    "old_li_compliance": {
        "tone_score": 94,  # 老李人设符合度
        "voice_samples": ["老李语录1", "老李语录2"],
        "memory_cards_used": ["D01", "B01"]
    }
}
```

---

## 🔄 工作流程

### 标准模式流程

```
用户提交话题
    ↓
步骤 1: 初始化 UCO 对象
    ↓
步骤 2: Agent 2 - 爆款分析 (10分钟)
    ↓
步骤 3: Agent 3 - 大纲设计 (15分钟)
    ↓
步骤 4: Agent 4 - 内容写作 (60分钟)
    ↓
步骤 5: Agent 5 - 质量审核 (30分钟)
    ↓  [可能多轮修改]
步骤 6: Agent 6 - 爆款预测 (10分钟)
    ↓
步骤 7: Agent 7 - 标题生成 (15分钟)
    ↓
完成！交付给用户确认

总耗时: 约 2-3 小时
```

### 应急模式流程

```
用户提交话题（urgency=EMERGENCY）
    ↓
快速分析 (5分钟)
    ↓
快速大纲 (5分钟)
    ↓
快速写作 (30分钟)
    ↓
快速审核 (15分钟，仅一轮)
    ↓
快速标题 (10分钟)
    ↓
完成！

总耗时: 约 1 小时
```

---

## ⚙️ 配置文件

创建 `config.yaml`：

```yaml
article_factory:
  # 超时设置（分钟）
  timeouts:
    agent_2: 15
    agent_3: 20
    agent_4: 90
    agent_5: 45
    agent_6: 15
    agent_7: 20

  # 修改轮次限制
  revision_limits:
    standard: 3  # 标准模式最多修改 3 轮
    high_quality: 5  # 高质量模式最多修改 5 轮
    emergency: 1  # 应急模式最多修改 1 轮

  # 质量阈值
  quality_thresholds:
    min_quality_score: 80  # 最低质量分数
    min_virality_score: 30  # 最低爆款分数
    min_tone_compliance: 85  # 最低老李人设符合度

  # 日志配置
  logging:
    level: "INFO"  # DEBUG, INFO, WARNING, ERROR
    log_file: "article_factory.log"
    save_intermediate: true  # 保存中间结果
```

使用配置文件：

```python
factory = ArticleFactory(config_path="config.yaml")
```

---

## 🧪 测试

### 运行测试

```bash
# 运行主程序（包含示例）
python implementation.py

# 使用 pytest 运行单元测试
pytest tests/

# 运行特定测试用例
pytest tests/ -k "test_standard_workflow"
```

### 查看测试用例

所有测试用例定义在 `test_cases.json` 中，包含：
- 14 个完整测试用例
- 覆盖功能、路由、质量、边界条件等场景
- 详细的输入输出预期

---

## 📊 监控与统计

### 获取统计信息

```python
stats = factory.get_stats()
print(f"总运行次数: {stats['total_runs']}")
print(f"成功次数: {stats['successful_runs']}")
print(f"失败次数: {stats['failed_runs']}")
print(f"平均耗时: {stats['average_duration']:.1f} 秒")
```

### 查看日志

日志保存在 `article_factory.log`：

```
2026-01-20 14:30:00 - ArticleFactory - INFO - 🏭 ArticleFactory 启动: 立春养肝
2026-01-20 14:30:05 - ArticleFactory - INFO - 📊 步骤 2/7: Agent 2 - 爆款分析
2026-01-20 14:45:00 - ArticleFactory - INFO - 📋 步骤 3/7: Agent 3 - 大纲设计
...
```

---

## 🔧 高级用法

### 1. 自定义 Agent 实现

默认使用模拟 Agent，实际使用时需要替换为真实 Agent：

```python
class MyArticleFactory(ArticleFactory):
    def _call_agent_2(self, topic, target_audience=None, mode="standard"):
        # 调用真实的 Agent 2
        from agent_2 import Agent2
        agent = Agent2()
        return agent.analyze_viral_articles(topic)

factory = MyArticleFactory()
```

### 2. 监听事件

```python
factory = ArticleFactory()

# 可以通过继承来自定义事件处理
class EventTrackingFactory(ArticleFactory):
    def _standard_workflow(self, *args, **kwargs):
        # 在每个步骤完成后发送通知
        # ...
        return super()._standard_workflow(*args, **kwargs)
```

### 3. 批量生成

```python
topics = [
    "立春养肝",
    "高温防暑",
    "秋季润肺"
]

results = []
for topic in topics:
    result = factory.generate_article(topic=topic)
    results.append(result)
```

---

## ❓ 常见问题

### Q1: 如何加速文章生成？

**A**: 使用应急模式：
```python
result = factory.generate_article(topic="XXX", urgency="EMERGENCY")
```

### Q2: 如何确保文章质量？

**A**: 使用高质量模式：
```python
result = factory.generate_article(topic="XXX", quality_level="HIGH")
```

### Q3: 修改轮次太多怎么办？

**A**: 系统会自动在达到修改上限后升级给用户，你可以：
- 查看 `result["workflow_report"]["routing_decisions"]`
- 检查 `result["quality_metrics"]["revision_count"]`
- 根据修改建议手动调整

### Q4: 如何调试生成过程？

**A**: 查看 UCO 调试信息：
```python
result = factory.generate_article(...)
uco_debug = result.get("_uco_debug")
print(json.dumps(uco_debug, indent=2, ensure_ascii=False))
```

---

## 🎯 最佳实践

1. **话题选择**
   - 优先使用时令主编推荐的话题
   - 话题应该具体、可操作
   - 避免过于学术化或抽象

2. **目标受众**
   - 明确定义年龄组
   - 考虑性别差异（如需要）
   - 添加兴趣标签提高精准度

3. **质量 vs 速度**
   - 日常内容：标准模式（NORMAL + STANDARD）
   - 热点追踪：应急模式（EMERGENCY）
   - 重要内容：高质量模式（HIGH）

4. **自定义要求**
   - 谨慎使用 `forbidden_words`（可能影响流畅度）
   - 合理设置字数范围（1500-3000 为宜）
   - 关键词应该自然融入，不要堆砌

---

## 📚 相关文档

- [ArticleFactory 规范文档](./agent.md) - 详细的技术规范
- [测试用例](./test_cases.json) - 完整的测试用例集
- [Health Writer V2 系统文档](../) - 系统整体说明

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可

MIT License

---

**创建时间**: 2026-01-20
**版本**: 1.0
**维护者**: Health Writer V2 Team
