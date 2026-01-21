# SubAgent: ArticleFactory (文章工厂)

> 一键生成爆款养生文章的虚拟机式 SubAgent

---

## SubAgent 信息

```yaml
SubAgent_ID: ArticleFactory_v1
SubAgent_Name: 文章工厂
Type: Orchestrator SubAgent
Version: 1.0
Created: 2026-01-20
Status: Production Ready
Runtime: Claude Code Task Tool
```

---

## 核心职责

### 主要功能
一键协调多个专业 Agent，自动完成从话题到成稿的全流程。

### 工作模式
**半自动模式**：用户确认话题 → SubAgent 协调生成 → 用户最终审核

### 为什么需要这个 SubAgent？

**当前痛点**：
- 生成一篇文章需要人工协调 Agent 2→3→4→5→6→7
- 流程耗时 2-3 小时，需要多次人工介入
- UCO 状态管理复杂，容易出错

**ArticleFactory 解决**：
- 一键启动全流程
- 自动管理 UCO 状态机
- 自动处理 Agent 间的数据传递
- 自动处理 Agent 5 的路由决策
- 生成完整报告，供用户最终审核

---

## 输入/输出协议

### 输入 (Input)

```yaml
启动参数:
  topic: string  # 话题或标题方向
    - 例如: "立春养肝"、"中老年人降糖方法"

  topic_source: string  # 话题来源
    - USER_MANUAL: 用户手动指定
    - CHRONOS_RECOMMENDATION: 时令主编推荐
    - VIRAL_TRENDING: 爆款分析热点
    - EMERGENCY_EVENT: 应急事件

  target_audience: object  # 目标受众（可选）
    - age_group: "45-60" | "60-70" | "70+"
    - gender: "male" | "female" | "all"
    - interests: array  # 兴趣标签

  urgency: string  # 紧急程度（可选）
    - NORMAL: 正常流程（2-3小时）
    - HIGH: 优先处理（1-2小时）
    - EMERGENCY: 应急模式（30-60分钟）

  quality_level: string  # 质量要求（可选）
    - STANDARD: 标准质量
    - HIGH: 高质量（多轮优化）

  custom_requirements: object  # 自定义要求（可选）
    - keywords: array  # 必须包含的关键词
    - forbidden_words: array  # 禁止出现的词汇
    - min_length: number  # 最小字数
    - max_length: number  # 最大字数
```

### 输出 (Output)

```yaml
输出类型: article_factory_result

结构:
  uco_id: string  # UCO 对象 ID
  status: string  # 最终状态

  article: object  # 生成的文章
    - title: string  # 最终标题（TOP 1）
    - titles_generated: array  # 所有生成的标题（TOP 3）
    - outline: object  # 文章大纲
    - content: string  # 正文内容
    - word_count: number  # 字数
    - tags: array  # 标签

  quality_metrics: object  # 质量指标
    - virality_score: number  # 爆款分数 (0-50)
    - virality_prediction: string  # 爆款预测
    - quality_score: number  # 质量分数 (0-100)
    - revision_count: number  # 修改轮次

  workflow_report: object  # 工作流报告
    - total_time: number  # 总耗时（分钟）
    - agent_execution_log: array  # 各 Agent 执行日志
    - routing_decisions: array  # 路由决策记录
    - issues_and_resolutions: array  # 问题和解决方案

  old_li_compliance: object  # 老李人设符合度
    - tone_score: number  # 语气符合度 (0-100)
    - voice_samples: array  # 使用的老李语录
    - memory_cards_used: array  # 引用的记忆卡片

  next_actions: array  # 建议的下一步操作
    - "review_and_edit": 查看并编辑
    - "regenerate_titles": 重新生成标题
    - "adjust_content": 调整内容
    - "approve_and_publish": 批准发布
```

---

## 工作流程设计

### 主流程：标准文章生成

```yaml
触发: 用户提交话题

步骤 1: 初始化
  - 创建新的 UCO 对象
  - 设置状态: INIT
  - 记录启动时间和输入参数
  - 预计完成时间: +2-3小时

步骤 2: Agent 2 - 爆款分析 (Deconstruction Analyst)
  - 调用: analyze_viral_articles
  - 输入: topic, related_keywords
  - 输出:
    - viral_dna_card: 爆款基因卡
    - key_patterns: 成功模式
    - golden_sentences: 金句提取
  - UCO 状态: INIT → ANALYZING → ANALYZED
  - 耗时: ~10分钟

步骤 3: Agent 3 - 大纲设计 (Topic Architect)
  - 调用: design_article_structure
  - 输入:
    - topic
    - viral_dna_card (from Agent 2)
    - persona_requirements (from Persona Hub)
  - 输出:
    - article_outline: 大纲结构
    - content_blocks: 内容块规划
    - emotional_arcs: 情感弧线
  - UCO 状态: ANALYZED → OUTLINING → OUTLINED
  - 耗时: ~15分钟

步骤 4: Agent 4 - 内容写作 (Content Architect)
  - 调用: write_article_content
  - 输入:
    - article_outline (from Agent 3)
    - viral_dna_card (from Agent 2)
    - old_li_persona (from Persona Hub)
    - domain_knowledge (from Knowledge Base)
  - 输出:
    - article_draft: 文章草稿
    - sources_cited: 引用来源
  - UCO 状态: OUTLINED → DRAFTING → DRAFTED
  - 耗时: ~60分钟

步骤 5: Agent 5 - 质量审核与路由 (Chief Reviewer)
  - 调用: review_and_route
  - 输入:
    - article_draft (from Agent 4)
    - quality_standards
  - 输出:
    - review_report: 审核报告
    - routing_decision: 路由决策
      - APPROVED: 继续下一步
      - REVISE_STRUCTURE → Agent 3
      - REVISE_CONTENT → Agent 4
      - ADJUST_TONE → Agent 4
      - ESCALATE → 用户
    - revision_suggestions: 修改建议
  - UCO 状态: DRAFTED → REVIEWING
  - 路由决策:
    - 如果 APPROVED: REVIEWED → 步骤 6
    - 如果需要修改: 根据路由规则处理
      - revision_count < 3: 返回对应 Agent
      - revision_count >= 3: 升级给用户
  - 耗时: ~30分钟（可能多轮）

步骤 6: Agent 6 - 爆款预测 (Virality Forecaster)
  - 调用: predict_virality
  - 输入:
    - reviewed_article (from Agent 5)
  - 输出:
    - virality_assessment: 爆款评估
    - overall_score: 综合分数 (0-50)
    - prediction: HIGH_POTENTIAL | MEDIUM | LOW
    - optimization_suggestions: 优化建议
  - UCO 状态: REVIEWED → OPTIMIZING → OPTIMIZED
  - 耗时: ~10分钟

步骤 7: Agent 7 - 标题生成 (Headline King)
  - 调用: generate_headlines
  - 输入:
    - final_article (from Agent 6)
    - target_audience
  - 输出:
    - headlines.generated: 10-15个标题
    - headlines.selected: TOP 3 推荐
    - ctr_prediction: 点击率预测
  - UCO 状态: OPTIMIZED → READY
  - 耗时: ~15分钟

步骤 8: 交付给用户
  - 汇总所有输出
  - 生成完整报告
  - UCO 状态: READY → 等待用户确认
  - 用户提供最终确认后: PUBLISHED
```

### 应急流程：快速生成模式

```yaml
触发: urgency = "EMERGENCY"

流程简化:
  步骤 1: 快速分析 (Agent 2, 5分钟)
  步骤 2: 快速大纲 (Agent 3, 5分钟)
  步骤 3: 快速写作 (Agent 4, 30分钟)
  步骤 4: 快速审核 (Agent 5, 15分钟, 仅一轮)
  步骤 5: 快速标题 (Agent 7, 10分钟)

总耗时: ~65分钟（vs 标准 140分钟）
质量: 略降，但时效性优先
```

### 高质量流程：多轮优化模式

```yaml
触发: quality_level = "HIGH"

流程增强:
  - Agent 5 审核后，如果质量分数 < 85:
    - 自动进入优化循环
    - revision_limit: 5（vs 标准 3）
  - Agent 6 预测后，如果爆款分数 < 35:
    - 根据优化建议，再次调用 Agent 4 优化
  - 最终确保:
    - quality_score >= 85
    - virality_score >= 35

总耗时: +30-60分钟
质量: 显著提升
```

---

## 智能路由逻辑

### Agent 5 的路由决策处理

```yaml
路由决策树:

  APPROVED:
    → 继续步骤 6 (Agent 6)

  REVISE_STRUCTURE:
    → 返回 Agent 3，传入:
      - 当前大纲
      - 修改建议
      - revision_count + 1
    → 重新进入步骤 4

  REVISE_CONTENT:
    → 返回 Agent 4，传入:
      - 当前草稿
      - 修改建议
      - revision_count + 1
    → 重新进入步骤 5

  ADJUST_TONE:
    → 返回 Agent 4，传入:
      - 当前草稿
      - 人设调整要求
      - revision_count + 1
    → 重新进入步骤 5

  ESCALATE:
    → 暂停自动化流程
    → 通知用户介入
    → 提供详细问题说明
    → 等待用户指示

无限循环防护:
  - revision_count >= 3:
    - 自动升级为 ESCALATE
    - 强制用户介入
```

---

## 数据流与 UCO 管理

### UCO 状态转换图

```
INIT
  ↓
ANALYZING (Agent 2)
  ↓
ANALYZED
  ↓
OUTLINING (Agent 3)
  ↓
OUTLINED
  ↓
DRAFTING (Agent 4)
  ↓
DRAFTED
  ↓
REVIEWING (Agent 5)
  ↓
  ├→ [需要修改] → 返回 Agent 3/4
  └→ [批准] → REVIEWED
      ↓
OPTIMIZING (Agent 6)
  ↓
OPTIMIZED
  ↓
[Agent 7 生成标题]
  ↓
READY
  ↓
[用户确认]
  ↓
PUBLISHED
```

### Agent 间数据传递

```yaml
Agent 2 → Agent 3:
  - viral_dna_card
  - key_patterns
  - golden_sentences

Agent 3 → Agent 4:
  - article_outline
  - content_blocks
  - emotional_arcs

Agent 4 → Agent 5:
  - article_draft
  - sources_cited

Agent 5 → Agent 6:
  - reviewed_article
  - quality_score

Agent 6 → Agent 7:
  - optimized_article
  - virality_score

All Agents ← Shared Knowledge:
  - Persona Hub (old_li)
  - Central Knowledge Base
  - Viral Patterns Database
```

---

## 错误处理与容错机制

### 常见错误场景

```yaml
错误场景 1: Agent 超时
  检测: Agent 执行时间 > 预期时间 × 1.5
  处理:
    - 记录超时日志
    - 保存当前进度到 UCO
    - 通知用户
    - 提供选项: 重试 / 跳过 / 手动介入

错误场景 2: Agent 输出格式错误
  检测: 输出不符合预期 schema
  处理:
    - 记录错误日志
    - 尝试重新调用该 Agent（最多 3 次）
    - 如果仍失败，升级为用户介入

错误场景 3: 知识库数据缺失
  检测: Agent 报告找不到相关数据
  处理:
    - 记录缺失数据
    - 使用通用替代方案
    - 在报告中标注数据来源
    - 建议更新知识库

错误场景 4: 修改循环
  检测: revision_count >= 3
  处理:
    - 自动停止循环
    - 升级为用户介入
    - 提供详细的修改历史
    - 提供多个选项供用户选择
```

---

## 性能指标

### 目标性能

```yaml
时间效率:
  - 标准模式: 2-3 小时
  - 应急模式: 1 小时内
  - 高质量模式: 3-4 小时

质量指标:
  - 老李人设符合度: >= 90%
  - 爆款分数: >= 35/50
  - 质量分数: >= 85/100
  - 标题CTR预测: >= 10%

成功率:
  - 一轮通过率: >= 70%
  - 三轮内通过率: >= 95%
  - 失败率（需要用户介入）: <= 5%
```

---

## 使用示例

### 示例 1: 标准文章生成

```yaml
输入:
  topic: "立春养肝"
  topic_source: "CHRONOS_RECOMMENDATION"
  target_audience:
    age_group: "60-70"
    gender: "all"
  urgency: "NORMAL"
  quality_level: "STANDARD"

执行过程:
  [08:00] ArticleFactory 启动
  [08:05] Agent 2 完成: 提取爆款模式"节气+食材+痛点"
  [08:20] Agent 3 完成: 设计大纲"引入→春困→养肝→韭菜→禁忌→总结"
  [09:20] Agent 4 完成: 生成草稿 2480字
  [09:50] Agent 5 完成: 质量分数 88，批准
  [10:00] Agent 6 完成: 爆款分数 38，HIGH_POTENTIAL
  [10:15] Agent 7 完成: 生成12个标题，推荐TOP 3
  [10:15] ArticleFactory 完成，等待用户确认

输出:
  article:
    title: "立春后，地里韭菜绿了。这可是春天养肝的第一菜，但记住了，脾胃虚寒的少吃"
    titles_generated:
      - "立春养肝第一菜，90%的人都吃错了" (CTR: 12.3%)
      - "老中医的养肝方，比吃药还管用" (CTR: 11.8%)
      - "春天别再吃这些了，伤肝又伤脾" (CTR: 10.9%)
    content: "立春了，该'咬春'了..."
    word_count: 2480
    tags: ["立春", "养肝", "韭菜", "老李"]

  quality_metrics:
    virality_score: 38
    virality_prediction: "HIGH_POTENTIAL"
    quality_score: 88
    revision_count: 0

  workflow_report:
    total_time: 75  # 分钟
    agent_execution_log: [...]
    issues_and_resolutions: []

  old_li_compliance:
    tone_score: 94
    voice_samples:
      - "立春了，该'咬春'了。但这韭菜也不是人人都能吃，胃寒的得悠着点。"
    memory_cards_used: ["D01", "B01"]
```

### 示例 2: 应急模式生成

```yaml
输入:
  topic: "高温防暑"
  topic_source: "EMERGENCY_EVENT"
  urgency: "EMERGENCY"
  quality_level: "STANDARD"
  custom_requirements:
    keywords: ["中暑", "防暑", "降温"]
    min_length: 1500

执行过程（快速流程）:
  [14:00] ArticleFactory 启动（应急模式）
  [14:05] Agent 2 快速分析完成
  [14:10] Agent 3 快速大纲完成
  [14:40] Agent 4 快速写作完成
  [14:55] Agent 5 快速审核完成（一轮）
  [15:00] Agent 7 快速标题完成
  [15:00] 完成，总耗时 60 分钟

输出:
  article:
    title: "39度高温来了！中老年人要注意心血管，老中医教你3招防暑"
    content: "三伏天，车间里像个蒸笼..."
    word_count: 1820

  quality_metrics:
    virality_score: 42  # 应急内容通常分数高
    quality_score: 82  # 略低但可接受

  workflow_report:
    total_time: 60
    mode: "EMERGENCY_FAST_TRACK"
```

### 示例 3: 需要修改的场景

```yaml
输入:
  topic: "糖尿病患者饮食禁忌"
  ...其他参数...

执行过程:
  [08:00] 启动
  [08:05-09:50] Agent 2,3,4 正常完成
  [10:20] Agent 5 审核结果:
    - routing_decision: "REVISE_CONTENT"
    - reasons:
      - "过于学术化，不符合老李人设"
      - "缺少具体案例"
    - revision_count: 1

  [10:20] ArticleFactory 自动路由 → Agent 4（第二轮）
  [11:20] Agent 4 完成（第二轮）
  [11:50] Agent 5 审核结果:
    - routing_decision: "APPROVED"
    - quality_score: 86
    - revision_count: 2

  [12:05] 完成，总耗时 125 分钟（比预期多25分钟）

输出:
  ...
  workflow_report:
    total_time: 125
    revision_count: 2
    routing_decisions:
      - {
          timestamp: "10:20",
          decision: "REVISE_CONTENT",
          agent: "Agent_5_ChiefReviewer",
          reason: "人设不符",
          action: "返回Agent_4重写"
        }
```

---

## 与其他组件的集成

### 与 Orchestrator 的关系

```yaml
Orchestrator:
  - 负责整体系统调度
  - 管理多个文章生成任务
  - 处理用户交互

ArticleFactory:
  - 专注于单篇文章生成的编排
  - 被 Orchestrator 调用
  - 返回 UCO 对象给 Orchestrator

协作模式:
  Orchestrator
    ↓ 接收用户请求
    ↓ 创建任务
    ↓ 调用 ArticleFactory
    ↓
    ArticleFactory 执行（2-3小时）
    ↓
    ↑ 返回 UCO
  Orchestrator
    ↓ 交付给用户
    ↓ 等待确认
    ↓ 发布
```

### 与 Chronos Editor (Agent 8) 的集成

```yaml
ChronosEditor:
  - 检测时令/应急事件
  - 生成话题推荐
  - 调用 ArticleFactory

协作流程:
  ChronosEditor 检测到立春
    ↓
  生成话题推荐: "立春养肝"
    ↓
  调用 ArticleFactory
    ↓
  ArticleFactory 生成文章
    ↓
  返回 UCO 给 ChronosEditor
    ↓
  ChronosEditor 调度发布
```

---

## 配置与部署

### 配置文件

```yaml
config.yaml:

article_factory:
  enabled: true

  timeouts:
    agent_2: 15  # 分钟
    agent_3: 20
    agent_4: 90
    agent_5: 45
    agent_6: 15
    agent_7: 20

  revision_limits:
    standard: 3
    high_quality: 5
    emergency: 1

  quality_thresholds:
    min_quality_score: 80
    min_virality_score: 30
    min_tone_compliance: 85

  modes:
    standard:
      enabled: true
      expected_duration: 140  # 分钟

    emergency:
      enabled: true
      expected_duration: 60
      quality_tradeoff: true

    high_quality:
      enabled: true
      expected_duration: 240
      revision_limit: 5

  logging:
    level: "INFO"
    log_file: "article_factory.log"
    save_intermediate: true  # 保存中间结果
```

### 部署检查清单

```yaml
部署前:
  - [ ] 所有 Agent 2-7 规范文档已创建
  - [ ] Persona Hub 已加载
  - [ ] Knowledge Base 已加载
  - [ ] UCO 状态机已实现
  - [ ] 路由逻辑已测试

部署后测试:
  - [ ] 标准模式测试
  - [ ] 应急模式测试
  - [ ] 修改循环测试
  - [ ] 错误处理测试
  - [ ] 质量指标验证
```

---

## 监控与优化

### 关键指标监控

```yaml
实时监控:
  - 当前运行中的任务数
  - 平均完成时间
  - Agent 调用成功率
  - 路由决策分布
  - 质量分数趋势

定期分析:
  - 每周: Agent 性能分析
  - 每月: 路由决策优化
  - 每季度: 整体流程优化
```

---

## 版本历史

```yaml
v1.0 (2026-01-20):
  - 初始版本
  - 实现 Agent 2-7 编排
  - 实现智能路由逻辑
  - 实现三种工作模式
  - 实现 UCO 状态管理
```

---

**文档维护者**: Health Writer V2 Team
**最后更新**: 2026-01-20
**下次审查**: 2026-02-20
