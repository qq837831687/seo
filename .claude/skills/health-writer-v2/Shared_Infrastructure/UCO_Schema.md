# 统一内容对象 (UCO) Schema

> Unified Content Object - 中老年养生内容工厂的数据传输标准

## 版本信息

- **版本**: 2.0
- **创建日期**: 2026-01-20
- **状态**: 生产就绪

---

## 核心概念

### 什么是UCO？

UCO (Unified Content Object) 是内容工厂的"工单"，记录了一篇文章从选题到发布的完整生命周期。

**类比**:
- 📦 就像工厂流水线上的产品，每个环节的工人都往上面添加东西
- 📝 就像医院的病历，记录诊断、治疗、恢复的全过程
- 🎫 就像快递的运单，追踪包裹的每一个状态变化

**为什么需要UCO？**
1. **统一数据格式**: 所有Agent用同一种语言交流
2. **状态追踪**: 随时知道文章到哪一步了
3. **可追溯**: 每个修改都有记录，可回滚
4. **可并发**: 多篇文章同时处理不会混乱

---

## 完整JSON Schema

```json
{
  "uco": {
    "uco_id": "UUID-v4",
    "article_id": "UUID-v4",
    "session_id": "UUID-v4",
    "version": "2.0",
    "created_at": "ISO8601",
    "updated_at": "ISO8601",

    "status": {
      "current": "ENUM值",
      "previous": "ENUM值",
      "history": [
        {
          "from": "INIT",
          "to": "TRENDING",
          "timestamp": "2026-01-20T10:00:00Z",
          "agent": "Orchestrator",
          "reason": "用户输入关键词：春天养肝"
        }
      ]
    },

    "revision_count": 0,
    "max_revisions": 3,

    "context": {
      "user_input": {
        "keyword": "春天养肝",
        "target_audience_hint": "中老年人",
        "content_type_hint": "食疗推荐"
      },
      "target_audience": {
        "age_range": "45-70",
        "gender": "不限",
        "city_tier": "全国",
        "health_concerns": ["慢性病", "养生", "饮食"]
      },
      "topic": {
        "primary": "春季养肝饮食",
        "secondary": ["食疗", "中医养生"],
        "keywords": ["春天", "养肝", "饮食", "食疗"]
      }
    },

    "research_payload": {
      "hot_trends": {
        "agent": "Agent_1_TrendSpotter",
        "timestamp": "ISO8601",
        "data": {
          "trending_topics": [...]
        }
      },
      "viral_analysis": {
        "agent": "Agent_2_DeconstructionAnalyst",
        "timestamp": "ISO8601",
        "data": {
          "analyzed_articles": [...],
          "success_patterns": [...]
        }
      },
      "fact_check_points": [...]
    },

    "structure": {
      "agent": "Agent_3_ChiefArchitect",
      "timestamp": "ISO8601",
      "article_type": "ENUM",
      "core_logic": "SCQA",
      "outline": {
        "headline_options": [...],
        "introduction": {...},
        "body": [...],
        "conclusion": {...},
        "total_word_count": 1500
      },
      "persona_alignment": {...}
    },

    "content": {
      "full_text": {
        "markdown": "...",
        "word_count": 1856,
        "metadata": {...}
      },
      "golden_sentences": [...],
      "headlines": {...},
      "annotations": [...]
    },

    "qa_report": {
      "overall_status": "APPROVED",
      "timestamp": "ISO8601",
      "agent": "Agent_5_ChiefReviewer",
      "diagnostics": [...],
      "routing_decision": {...},
      "checks": {...},
      "virality_assessment": {...}
    },

    "optimization": {
      "agent": "Agent_6_ViralityForecaster",
      "timestamp": "ISO8601",
      "seo_keywords": {...},
      "optimization_suggestions": [...]
    },

    "publication": {
      "platforms": ["wechat_public"],
      "scheduled_at": "ISO8601",
      "published_at": null,
      "urls": {...},
      "metrics": {...}
    },

    "feedback_loop": {
      "initial_24h": null,
      "day_7": null,
      "day_30": null,
      "final_classification": "SUCCESS",
      "lessons_learned": "..."
    }
  }
}
```

---

## 状态枚举值

### 状态列表

| 状态值 | 说明 | 所属阶段 | Agent |
|--------|------|----------|-------|
| INIT | 初始状态 | 输入 | Orchestrator |
| TRENDING | 选题中 | 输入 | Agent_1 |
| TOPIC_SELECTED | 选题已确认 | 输入（人工介入点） | User |
| ANALYZING | 分析爆款中 | 研究 | Agent_2 |
| ANALYZED | 分析完成 | 研究 | Agent_2 |
| OUTLINING | 设计大纲中 | 创作 | Agent_3 |
| OUTLINED | 大纲完成 | 创作（人工介入点） | User |
| DRAFTING | 撰写中 | 创作 | Agent_4 |
| DRAFTED | 初稿完成 | 创作 | Agent_4 |
| REVIEWING | 审查中 | 质控 | Agent_5 |
| REVIEWED | 审查完成 | 质控 | Agent_5 |
| OPTIMIZING | 优化中 | 质控 | Agent_6+7 |
| OPTIMIZED | 优化完成 | 质控 | Agent_6+7 |
| READY | 准备发布 | 输出（人工介入点） | User |
| PUBLISHED | 已发布 | 输出 | Agent_8 |
| ARCHIVED | 已归档 | 结束 | System |
| BLOCKED | 异常阻塞 | 异常 | Orchestrator |
| ERROR | 错误 | 异常 | Orchestrator |

### 状态流转规则

```
正常流程:
INIT → TRENDING → TOPIC_SELECTED → ANALYZING → ANALYZED
→ OUTLINING → OUTLINED → DRAFTING → DRAFTED → REVIEWING → REVIEWED
→ OPTIMIZING → OPTIMIZED → READY → PUBLISHED → ARCHIVED

异常流程:
REVIEWED → DRAFTING (打回重写)
REVIEWED → OUTLINING (结构有问题)
REVIEWED → BLOCKED (revision_count > 3)
任何状态 → ERROR (严重错误)
```

---

## 字段详解

### 1. 基础信息字段

```yaml
uco_id: "全局唯一标识符"
article_id: "文章ID"
session_id: "会话ID，关联所有操作"
created_at: "创建时间"
updated_at: "最后更新时间"
version: "UCO Schema版本"
```

### 2. 状态字段

```yaml
status.current: "当前状态"
status.previous: "上一个状态"
status.history: "状态变更历史记录"
revision_count: "当前修订次数"
max_revisions: "最大修订次数（默认3）"
```

### 3. 上下文字段

```yaml
context.user_input: "用户输入的原始需求"
context.target_audience: "目标受众画像"
context.topic: "文章主题信息"
```

### 4. 研究载荷字段

```yaml
research_payload.hot_trends: "热点趋势数据（Agent_1写入）"
research_payload.viral_analysis: "爆款分析数据（Agent_2写入）"
research_payload.fact_check_points: "事实核查点"
```

### 5. 结构字段

```yaml
structure.agent: "创建此结构的Agent"
structure.article_type: "文章类型"
structure.core_logic: "核心逻辑模型"
structure.outline: "详细大纲"
structure.persona_alignment: "人设对齐情况"
```

### 6. 内容字段

```yaml
content.full_text: "完整正文（Markdown）"
content.golden_sentences: "金句列表"
content.headlines: "标题数据"
content.annotations: "元数据标注（来源标注）"
```

### 7. QA报告字段

```yaml
qa_report.overall_status: "总状态（APPROVED/REJECTED）"
qa_report.diagnostics: "诊断列表"
qa_report.routing_decision: "路由决策"
qa_report.checks: "各项检查结果"
qa_report.virality_assessment: "爆款潜力评估"
```

### 8. 优化字段

```yaml
optimization.seo_keywords: "SEO关键词"
optimization.optimization_suggestions: "优化建议"
```

### 9. 发布字段

```yaml
publication.platforms: "发布平台列表"
publication.scheduled_at: "计划发布时间"
publication.published_at: "实际发布时间"
publication.urls: "各平台URL"
publication.metrics: "发布后数据"
```

### 10. 反馈闭环字段

```yaml
feedback_loop.initial_24h: "24小时数据"
feedback_loop.day_7: "7天数据"
feedback_loop.day_30: "30天数据"
feedback_loop.final_classification: "最终分类（SUCCESS/AVERAGE/FAILURE）"
feedback_loop.lessons_learned: "经验教训"
```

---

## Agent读写权限表

| Agent | 读取字段 | 写入字段 | 状态变更 |
|-------|---------|---------|---------|
| **Agent_1** | context.user_input<br>persona.value_system<br>knowledge.feedback_loop | research_payload.hot_trends | INIT → TRENDING |
| **Agent_2** | context.topic<br>knowledge.success_archives | research_payload.viral_analysis | TOPIC_SELECTED → ANALYZED |
| **Agent_3** | research_payload.viral_analysis<br>persona.linguistic_style<br>knowledge.opinion_bank | structure | ANALYZED → OUTLINED |
| **Agent_4** | structure.outline<br>persona.linguistic_style<br>knowledge.story_database | content.full_text<br>content.annotations | OUTLINED → DRAFTED |
| **Agent_5** | content.full_text<br>persona.full<br>knowledge.fact_base | qa_report | DRAFTED → REVIEWED |
| **Agent_6** | content.full_text<br>knowledge.success_archives | qa_report.virality_assessment<br>optimization | REVIEWED → OPTIMIZED |
| **Agent_7** | context.topic<br>content.full_text<br>knowledge.success_archives | content.headlines | OPTIMIZED → READY |
| **Agent_8** | content.full_text<br>content.headlines.selected | publication.urls<br>feedback_loop | READY → PUBLISHED |

---

## 使用示例

### 示例1: 创建新UCO

```json
{
  "uco": {
    "uco_id": "uco-2026-01-20-001",
    "article_id": "art-001",
    "session_id": "sess-001",
    "created_at": "2026-01-20T10:00:00Z",
    "updated_at": "2026-01-20T10:00:00Z",

    "status": {
      "current": "INIT",
      "previous": null,
      "history": []
    },

    "revision_count": 0,

    "context": {
      "user_input": {
        "keyword": "春天养肝",
        "target_audience_hint": "中老年人",
        "content_type_hint": "食疗推荐"
      }
    }
  }
}
```

### 示例2: Agent_1完成工作

```json
{
  "status": {
    "current": "TRENDING",
    "previous": "INIT",
    "history": [
      {
        "from": "INIT",
        "to": "TRENDING",
        "timestamp": "2026-01-20T10:05:00Z",
        "agent": "Agent_1_TrendSpotter",
        "reason": "生成了5个选题"
      }
    ]
  },

  "research_payload": {
    "hot_trends": {
      "agent": "Agent_1_TrendSpotter",
      "timestamp": "2026-01-20T10:05:00Z",
      "data": {
        "trending_topics": [
          {
            "topic": "春天养肝吃什么",
            "hotness_score": 8.5,
            "competition_level": "medium"
          }
        ]
      }
    }
  }
}
```

### 示例3: 用户确认选题

```json
{
  "status": {
    "current": "TOPIC_SELECTED",
    "previous": "TRENDING",
    "history": [...]
  },

  "context": {
    "topic": {
      "primary": "春季养肝饮食",
      "selected": true,
      "selected_by": "User",
      "selected_at": "2026-01-20T10:10:00Z"
    }
  }
}
```

---

## 版本控制

### 版本历史

- **v1.0** (2026-01-15): 初始版本
- **v2.0** (2026-01-20): 增加反馈闭环、病毒式营销模式

### 向后兼容性

- 新增字段不影响旧版本Agent
- Agent应忽略未知字段
- 废弃字段保留2个版本后移除

---

## 最佳实践

### 1. 字段命名

- 使用snake_case
- 使用复数形式表示数组
- 使用布尔值命名：is_xxx, has_xxx

### 2. 时间格式

- 统一使用ISO8601格式
- 时区使用UTC
- 包含毫秒精度

### 3. 数据验证

- Agent写入前必须验证字段类型
- Agent读取前必须检查字段存在性
- 缺失必需字段时记录错误

### 4. 元数据标注

- 所有AI生成内容必须标注来源
- 格式: `<!-- source: source_id -->`
- 示例: `<!-- source: story_db_001 -->`

### 5. 版本控制

- 每次状态变化保存快照
- 保留最近5个版本
- 支持回滚到任意版本

---

**维护者**: Content Factory Team
**最后更新**: 2026-01-20
