# Agent-Knowledge API 交互协议

> 定义Agent如何程序化地访问人设库和知识库

---

## API设计原则

1. **RESTful风格**: 使用标准HTTP方法
2. **JSON格式**: 所有数据JSON序列化
3. **版本控制**: API路径包含版本号
4. **错误处理**: 统一错误码和错误信息

---

## API端点定义

### 1. 读取人设 (Read Persona)

```
GET /api/v1/persona/{field}

参数:
  - field: 要读取的字段路径
    示例: "linguistic_style.forbidden_words"
    支持通配符: "linguistic_style.*"

返回:
{
  "status": "success",
  "data": {
    "forbidden_words": ["yyds", "绝绝子", "666"]
  },
  "timestamp": "2026-01-20T10:00:00Z"
}
```

**使用示例**:
```yaml
Agent 4 (王牌写手) 写作前:
  GET /api/v1/persona/linguistic_style
  → 获取老李语言风格

  GET /api/v1/persona/linguistic_style/forbidden_words
  → 获取禁用词列表

  GET /api/v1/persona/expertise_areas
  → 获取专业领域
```

---

### 2. 读取知识库 (Read Knowledge)

```
GET /api/v1/knowledge/{collection}/{query}

参数:
  - collection: fact_base | opinion_bank | story_database | success_archives
  - query: 查询条件
    支持关键词、标签、ID等

返回:
{
  "status": "success",
  "data": {
    "results": [...],
    "count": 5
  },
  "timestamp": "2026-01-20T10:00:00Z"
}
```

**使用示例**:
```yaml
Agent 4 (王牌写手) 撰写时:
  GET /api/v1/knowledge/story_database?tag=脾胃虚寒
  → 获取相关故事

  GET /api/v1/knowledge/fact_base?keyword=山药
  → 获取山药功效事实

  GET /api/v1/knowledge/opinion_bank/quotations
  → 获取金句列表
```

---

### 3. 写入知识库 (Write Knowledge)

```
POST /api/v1/knowledge/{collection}

Body:
{
  "record_type": "viral_pattern | performance | lesson",
  "data": {...},
  "agent": "Agent_2_DeconstructionAnalyst"
}

返回:
{
  "status": "success",
  "record_id": "pattern_001",
  "timestamp": "2026-01-20T10:00:00Z"
}
```

**使用示例**:
```yaml
Agent 2 (爆文分析师) 分析完成后:
  POST /api/v1/knowledge/viral_patterns_database
  Body: {
    "record_type": "viral_pattern",
    "data": {
      "headline_formula": "[数字]种[功效]食材",
      "success_rate": 0.85
    }
  }
  → 写入新模式

Agent 8 (增长黑客) 发布后:
  POST /api/v1/knowledge/feedback_loop
  Body: {
    "record_type": "performance",
    "data": {
      "article_id": "art_001",
      "views": 10000,
      "shares": 500
    }
  }
  → 写入性能数据
```

---

### 4. 更新人设 (Update Persona)

```
PATCH /api/v1/persona/{field}

Body:
{
  "operation": "add | remove | replace",
  "value": {...},
  "agent": "Agent_10_ChiefAITrainer"
}

返回:
{
  "status": "success",
  "previous_value": {...},
  "new_value": {...},
  "timestamp": "2026-01-20T10:00:00Z"
}
```

**使用示例**:
```yaml
Agent 10 (首席AI训练师) 优化时:
  PATCH /api/v1/persona/linguistic_style/forbidden_words
  Body: {
    "operation": "add",
    "value": ["新发现的网络用语"]
  }
  → 添加新的禁用词
```

---

### 5. 批量操作 (Batch Operations)

```
POST /api/v1/batch

Body:
{
  "operations": [
    {
      "method": "GET",
      "path": "/persona/linguistic_style"
    },
    {
      "method": "GET",
      "path": "/knowledge/story_database?tag=脾胃虚寒"
    }
  ]
}

返回:
{
  "status": "success",
  "results": [
    {...},
    {...}
  ],
  "timestamp": "2026-01-20T10:00:00Z"
}
```

---

## 错误处理

### 错误码定义

| 错误码 | 说明 | HTTP状态 | 处理方式 |
|--------|------|----------|----------|
| 404 | 字段不存在 | 404 | 使用默认值 |
| 400 | 请求格式错误 | 400 | 记录日志，返回错误 |
| 500 | 数据格式错误 | 500 | 跳过该字段，记录日志 |
| 503 | 知识库不可用 | 503 | 使用缓存数据 |

### 错误响应示例

```json
{
  "status": "error",
  "error_code": 404,
  "message": "Field not found: opinion_bank.new_tag",
  "fallback": "Using empty array",
  "timestamp": "2026-01-20T10:00:00Z"
}
```

---

## 性能优化

### 1. 缓存策略

```yaml
热点数据缓存:
  - Persona_Hub.json: 缓存1小时（很少变化）
  - Knowledge_Base: 缓存5分钟
  - UCO status: 实时（不缓存）

缓存失效:
  - 手动清除: PATCH /api/v1/cache/clear
  - 自动失效: 超时后自动刷新
```

### 2. 批量查询

```yaml
支持一次读取多个字段:
  POST /api/v1/batch
  → 减少网络往返

支持字段通配符:
  GET /api/v1/persona/linguistic_style.*
  → 返回所有子字段
```

### 3. 增量更新

```yaml
只更新变化的部分:
  PATCH /api/v1/knowledge/feedback_loop
  → 只更新新增的performance数据

不重新加载整个知识库
```

---

## Agent调用示例

### 完整工作流示例

```yaml
# Agent 4 (王牌写手) 完整写作流程

Step 1: 读取语言风格
  GET /api/v1/persona/linguistic_style
  → {sentence_length_pref: "short", preferred_words: [...]}

Step 2: 读取禁用词
  GET /api/v1/persona/linguistic_style/forbidden_words
  → ["yyds", "绝绝子", ...]

Step 3: 检索相关故事
  GET /api/v1/knowledge/story_database?tag=脾胃虚寒
  → [story_002: 山药粥调理脾胃]

Step 4: 验证事实
  GET /api/v1/knowledge/fact_base?keyword=山药功效
  → {yam_山药: {efficacy: "健脾养胃"}}

Step 5: 撰写正文
  (使用上述数据撰写)

Step 6: 添加元数据标注
  <!-- source: story_db_002 -->
  <!-- source: fact_base_nutrition -->
```

---

## 安全与权限

### API密钥

```yaml
每个Agent分配唯一API密钥:
  - Agent_1: key_agent_1_xxxxx
  - Agent_2: key_agent_2_xxxxx
  - ...

密钥用途:
  - 身份验证
  - 访问控制
  - 操作审计
```

### 访问控制

```yaml
读取权限: 所有Agent
写入权限: 仅特定Agent
  - viral_patterns: Agent_2, Agent_10
  - feedback_loop: Agent_8, Agent_10
  - persona: 仅Agent_10

管理权限: 仅人工管理员
```

---

## 监控与日志

### API调用日志

```json
{
  "timestamp": "2026-01-20T10:00:00Z",
  "agent": "Agent_4_AceWriter",
  "method": "GET",
  "path": "/api/v1/knowledge/story_database",
  "params": {"tag": "脾胃虚寒"},
  "response_time": "50ms",
  "status": "success"
}
```

### 性能监控

```yaml
监控指标:
  - API响应时间
  - 调用频率
  - 错误率
  - 缓存命中率

告警阈值:
  - 响应时间 > 1s
  - 错误率 > 5%
  - 缓存命中率 < 80%
```

---

**维护者**: Content Factory Team
**最后更新**: 2026-01-20
