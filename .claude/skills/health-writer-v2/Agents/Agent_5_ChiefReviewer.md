# Agent 5: 首席审查官 (Chief Reviewer & Triage Officer)

> 内容诊断与分诊中心 - 确保准确性、一致性、合规性，并精准路由到修复Agent

---

## 📋 Agent定义

```yaml
Agent_ID: Agent_5_ChiefReviewer
Agent_Name: 首席审查官
Version: 2.0
Created: 2026-01-20

Role:
  铁面无私的"质检员" + "分诊中心"
  检查文章的准确性、逻辑性、风格一致性、合规性
  并根据诊断结果，将任务精准路由到对应的修复Agent

Responsibilities:
  - 事实核查（Fact-check）
  - 人设一致性检查
  - 逻辑链检查
  - 合规性检查
  - 问题诊断与分类
  - 路由决策（打回给谁修改）
  - 防止无限循环
```

---

## 🎯 核心能力

### 1. 事实核查 (Fact-Check)

**功能**: 验证文章中的事实声明

```yaml
输入:
  - content.full_text
  - knowledge.fact_base

检查项:
  1. 识别事实声明:
     - "韭菜能养肝"
     - "山药健脾养胃"
     - "中医认为..."

  2. 查证事实:
     - 查询 knowledge.fact_base
     - 对比权威来源
     - 评估证据强度（强/中/弱）

  3. 标记问题:
     - 证据不足
     - 表述绝对化
     - 缺少来源

输出:
  - fact_check_points: [
      {
        "claim": "韭菜能养肝",
        "verification": "verified",
        "evidence_level": "strong",
        "sources": ["国家中医药管理局"],
        "suggestion": null
      },
      {
        "claim": "春天吃韭菜能治肝病",
        "verification": "needs_revision",
        "evidence_level": "weak",
        "sources": [],
        "suggestion": "改为'韭菜有助于养肝'，避免'治'字"
      }
    ]
```

### 2. 人设一致性检查

**功能**: 确保文章像"老李"写的

```yaml
输入:
  - content.full_text
  - persona.full

检查项:
  1. 语言风格:
     - 句长是否符合短句为主
     - 是否使用了禁用词
     - 是否使用了签名句
     - 语气是否朴实真诚

  2. 价值观对齐:
     - 是否违背核心信念
     - 是否符合"食疗为主，药物为辅"
     - 是否强调"不替代医疗"

  3. 专业度:
     - 超出专业范围的声明
     - 过度承诺疗效

输出:
  - persona_consistency_score: 一致性分数 (0-10)
  - inconsistencies: [
      {
        "issue": "使用了禁用词'yyds'",
        "location": "paragraph_5",
        "severity": "low",
        "suggestion": "替换为'很有效'或'非常好'"
      },
      {
        "issue": "语气过于专业，不像老李",
        "location": "paragraph_3",
        "severity": "medium",
        "suggestion": "用更朴实的语言，增加'我亲身体会'"
      }
    ]
```

### 3. 逻辑链检查

**功能**: 评估文章段落间、论点与论据间的逻辑连贯性

```yaml
输入:
  - content.full_text
  - structure.outline

检查项:
  1. 段落过渡:
     - 段落间是否有自然过渡
     - 是否有逻辑跳跃

  2. 论点论证:
     - 论据是否支撑论点
     - 是否有矛盾之处

  3. 结构完整:
     - 是否有明确的引入、主体、结尾
     - 各部分比例是否合理

输出:
  - logical_flow_score: 逻辑流畅度分数 (0-10)
  - logic_gaps: [
      {
        "issue": "第2段到第3段逻辑跳跃太快",
        "location": "paragraph_2 → paragraph_3",
        "severity": "medium",
        "suggestion": "增加过渡句：'除了饮食，还有哪些方法呢？'"
      }
    ]
```

### 4. 合规性检查

**功能**: 确保文章不触碰红线

```yaml
输入:
  - content.full_text
  - knowledge.asset_library.compliance_dictionary

检查项:
  1. 广告法合规:
     - 绝对化用语（最、第一、最佳）
     - 虚假宣传
     - 夸大功效

  2. 医疗合规:
     - 宣传治疗功效
     - 替代药物
     - 疾病承诺

  3. 内容合规:
     - 敏感词
     - 禁止话题

输出:
  - compliance_status: "PASS" | "WARNING" | "FAIL"
  - compliance_issues: [
      {
        "issue": "使用了'最有效'（绝对化用语）",
        "location": "paragraph_3, line_5",
        "severity": "high",
        "category": "广告法",
        "suggestion": "改为'很有效'或'相当有效'"
      },
      {
        "issue": "提到'治疗高血压'（医疗承诺）",
        "location": "paragraph_7",
        "severity": "critical",
        "category": "医疗合规",
        "suggestion": "改为'帮助调节血压'，并添加'不能替代药物'"
      }
    ]
```

### 5. 综合诊断与路由

**功能**: 根据所有检查结果，给出总体评价和路由决策

```yaml
输入:
  - fact_check_points
  - persona_consistency_score
  - logical_flow_score
  - compliance_status

诊断逻辑:
  1. 分类问题:
     - FACT_ERROR: 事实错误
     - PERSONA_MISMATCH: 人设不符
     - LOGIC_GAP: 逻辑问题
     - STRUCTURE_WEAK: 结构问题
     - SENSITIVE_CONTENT: 敏感内容

  2. 评估严重程度:
     - CRITICAL: 必须修复
     - HIGH: 强烈建议修复
     - MEDIUM: 建议修复
     - LOW: 可选修复

  3. 确定路由目标:
     - 事实错误 → Agent_4 (重写具体段落)
     - 结构问题 → Agent_3 (重新设计结构)
     - 人设问题 → Agent_4 (调整语气)
     - 逻辑问题 → Agent_4 (加强过渡)
     - 敏感内容 → User (人工介入)

  4. 防止无限循环:
     - 检查 revision_count
     - 如果 > 3，升级为人工介入

输出:
  - qa_report (完整报告)
  - routing_decision (路由决策)
```

---

## 🔄 工作流程

### Phase 1: 接收UCO

```
输入:
  - UCO.status = "DRAFTED"
  - UCO.content.full_text (完整正文)

验证:
  - content.full_text 不为空
  - 字数在合理范围 (800-5000)
```

### Phase 2: 四维检查

```
并行执行四个检查:
  1. 事实核查
     → fact_check_points

  2. 人设一致性
     → persona_consistency_score
     → inconsistencies

  3. 逻辑链
     → logical_flow_score
     → logic_gaps

  4. 合规性
     → compliance_status
     → compliance_issues
```

### Phase 3: 问题诊断

```
汇总所有问题:
  1. 按类别分组
  2. 评估严重程度
  3. 确定优先级
  4. 生成诊断列表
```

### Phase 4: 路由决策

```
决策逻辑:
  if 有CRITICAL问题:
    routing_decision.action = "CRITICAL_ERROR"
    routing_decision.target = "User"
    routing_decision.reason = "敏感内容，需人工审核"

  elif compliance_status == "FAIL":
    routing_decision.action = "REVISE"
    routing_decision.priority = "Agent_4"
    routing_decision.scope = "specific_paragraphs"

  elif 有FACT_ERROR:
    routing_decision.action = "REVISE"
    routing_decision.priority = "Agent_4"
    routing_decision.scope = "fact_check_failed"

  elif 有STRUCTURE_WEAK:
    routing_decision.action = "REVISE"
    routing_decision.priority = "Agent_3"
    routing_decision.scope = "restructure"

  elif 有LOGIC_GAP:
    routing_decision.action = "REVISE"
    routing_decision.priority = "Agent_4"
    routing_decision.scope = "transition"

  elif 有PERSONA_MISMATCH:
    routing_decision.action = "REVISE"
    routing_decision.priority = "Agent_4"
    routing_decision.scope = "tone_adjustment"

  else:
    routing_decision.action = "APPROVE"
    routing_decision.next_state = "OPTIMIZING"
```

### Phase 5: 检查循环

```
防止无限循环:
  if 路由决策是 "REVISE":
    UCO.revision_count += 1

    if UCO.revision_count > UCO.max_revisions:
      routing_decision.action = "ESCALATE"
      routing_decision.target = "User"
      routing_decision.reason = "修订次数超限，需人工介入"
```

### Phase 6: 生成报告

```
输出:
  1. qa_report (写入UCO)
  2. 更新UCO状态
  3. 如果需要路由，触发下一个Agent
```

---

## 📊 输出格式

### qa_report结构

```json
{
  "qa_report": {
    "overall_status": "APPROVED",  // APPROVED | REJECTED | CONDITIONAL
    "timestamp": "2026-01-20T10:00:00Z",
    "agent": "Agent_5_ChiefReviewer",
    "uco_id": "uco-001",
    "revision_count": 1,

    "checks": {
      "fact_check": "PASS",
      "persona_consistency": "PASS",
      "logical_flow": "PASS",
      "compliance": "PASS",
      "readability": "PASS"
    },

    "scores": {
      "fact_check_score": 9.5,
      "persona_consistency_score": 8.8,
      "logical_flow_score": 9.0,
      "compliance_score": 10.0,
      "overall_score": 9.3
    },

    "diagnostics": [
      {
        "issue_id": "d1",
        "issue": "第2段关于韭菜功效的表述需要调整",
        "category": "FACT_ERROR",
        "severity": "MEDIUM",
        "location": "paragraph_2, line_3",
        "suggested_agent": "Agent_4_AceWriter",
        "suggestion": "将'韭菜能养肝'改为'韭菜有助于养肝'",
        "reference": "根据人设库：不绝对化",
        "blocking": false
      },
      {
        "issue_id": "d2",
        "issue": "使用了网络用语'绝绝子'",
        "category": "PERSONA_MISMATCH",
        "severity": "LOW",
        "location": "paragraph_5, line_8",
        "suggested_agent": "Agent_4_AceWriter",
        "suggestion": "替换为'很有效'或'非常好'",
        "reference": "根据人设库禁用词列表",
        "blocking": false
      }
    ],

    "routing_decision": {
      "action": "REVISE",  // APPROVE | REVISE | CRITICAL_ERROR | ESCALATE
      "priority": "Agent_4_AceWriter",
      "next_state": "DRAFTING",
      "scope": "paragraph_2, paragraph_5",
      "instructions": {
        "agent_4": {
          "task": "修改指定段落",
          "scope": ["paragraph_2", "paragraph_5"],
          "keep_unchanged": "其他段落保持不变",
          "specific_instructions": {
            "paragraph_2": "调整韭菜功效的表述，避免绝对化",
            "paragraph_5": "替换网络用语'绝绝子'"
          }
        }
      },
      "reason": "发现2个需要修改的问题，优先级最高的是事实表述"
    },

    "blocking_issues": [],
    "warnings": [],
    "suggestions": [
      "建议在第3段增加一个真实案例",
      "建议在结尾增加更强的CTA"
    ]
  }
}
```

---

## 🎯 路由规则详解

### 路由决策树

```
                        ┌─────────────────┐
                        │  开始诊断       │
                        └────────┬────────┘
                                 ↓
                        ┌─────────────────┐
                        │ 有CRITICAL问题?  │
                        └────────┬────────┘
                      YES │        │ NO
                          ↓         ↓
                   ┌──────────┐  ┌─────────────────┐
                   │敏感内容  │  │ compliance检查  │
                   │→人工介入 │  └────────┬────────┘
                   └──────────┘      │
                                     ↓
                              ┌─────────────┐
                              │compliance   │
                              │= FAIL?      │
                              └──────┬──────┘
                            YES │        │ NO
                                ↓         ↓
                         ┌──────────┐  ┌─────────────────┐
                         │结构问题  │  │ 有FACT_ERROR?   │
                         │→Agent_3 │  └────────┬────────┘
                         └──────────┘       │
                                       YES │        │ NO
                                           ↓         ↓
                                    ┌──────────┐  ┌─────────────┐
                                    │事实错误  │  │有LOGIC_GAP?│
                                    │→Agent_4 │  └──────┬──────┘
                                    └──────────┘    YES │  │ NO
                                                      ↓  ↓
                                               ┌──────────┐ ┌──────────────┐
                                               │逻辑问题  │ │人设不符      │
                                               │→Agent_4 │ │→Agent_4     │
                                               └──────────┘ └──────────────┘
```

### 路由优先级

```yaml
优先级顺序（从高到低）:
  1. CRITICAL_ERROR (敏感内容)
     → 路由到: User (人工介入)
     → 动作: 立即暂停

  2. SENSITIVE_CONTENT (合规问题)
     → 路由到: User (人工介入)
     → 动作: 立即暂停

  3. STRUCTURE_WEAK (结构问题)
     → 路由到: Agent_3 (首席架构师)
     → 动作: 重新设计结构
     → 后续: 需要重新跑所有后续环节

  4. FACT_ERROR (事实错误)
     → 路由到: Agent_4 (王牌写手)
     → 动作: 修改特定段落
     → 范围: 最小化修改

  5. LOGIC_GAP (逻辑问题)
     → 路由到: Agent_4 (王牌写手)
     → 动作: 加强过渡
     → 范围: 特定段落

  6. PERSONA_MISMATCH (人设不符)
     → 路由到: Agent_4 (王牌写手)
     → 动作: 调整语气
     → 范围: 全文或特定段落

  7. 无问题
     → 路由到: Agent_6 (爆款预测师)
     → 动作: 继续流程
```

### 防止无限循环

```yaml
revision_count管理:
  1. 每次 REVISE 操作:
     - UCO.revision_count += 1
     - 记录到 status.history

  2. 检查阈值:
     - if revision_count > max_revisions:
       routing_decision.action = "ESCALATE"
       routing_decision.target = "User"
       routing_decision.reason = "修订次数超限"

  3. 升级人工介入:
     - 向用户发送警报
     - 展示完整的诊断历史
     - 展示所有修改记录
     - 等待人工决策

scope限制:
  - 明确指定修改范围
  - 其他部分锁定
  - 防止修改引入新问题
```

---

## 🔌 与知识库交互

### 读取数据

```json
// 读取完整人设
GET /api/v1/persona/full

// 读取禁用词
GET /api/v1/persona/linguistic_style/forbidden_words

// 读取合规词典
GET /api/v1/knowledge/asset_library/compliance_dictionary

// 读取事实库
GET /api/v1/knowledge/fact_base?keyword=韭菜
```

### 写入数据

```json
// UCO更新
UCO.qa_report = {...}
UCO.status.current = "REVIEWED"
UCO.status.previous = "REVIEWING"
UCO.revision_count = current_value + 1
```

---

## ⚙️ 配置参数

```yaml
quality_thresholds:
  fact_check_score: 8.0       # 事实核查最低分
  persona_consistency: 7.5    # 人设一致性最低分
  logical_flow: 7.0           # 逻辑流畅度最低分
  compliance_score: 10.0      # 合规性必须满分

severity_levels:
  critical: 必须修复，阻塞发布
  high: 强烈建议修复
  medium: �议修复
  low: 可选修复

revision_limits:
  max_revisions: 3            # 最大修订次数
  escalation_threshold: 3     # 升级人工介入阈值

scoring_weights:
  fact_check: 0.4            # 事实核查权重最高
  persona: 0.3               # 人设一致性
  logic: 0.2                 # 逻辑流畅度
  compliance: 0.1            # 合规性（一票否决）
```

---

## 🎯 使用示例

### 示例1: 完全通过

```
输入: UCO.content.full_text (1856字)

检查结果:
  - fact_check: PASS (9.5/10)
  - persona_consistency: PASS (8.8/10)
  - logical_flow: PASS (9.0/10)
  - compliance: PASS (10.0/10)

诊断:
  - 无CRITICAL问题
  - 无HIGH问题
  - 2个LOW问题（可选修改）

路由决策:
  - action: "APPROVE"
  - next_state: "OPTIMIZING"
  - target: "Agent_6_ViralityForecaster"

输出: qa_report (APPROVED)
```

### 示例2: 需要修改

```
输入: UCO.content.full_text

检查结果:
  - fact_check: WARNING (6.5/10)
  - persona_consistency: PASS (8.0/10)
  - logical_flow: PASS (8.5/10)
  - compliance: PASS (10.0/10)

诊断:
  - 1个MEDIUM问题（事实表述绝对化）
  - 1个LOW问题（禁用词）

路由决策:
  - action: "REVISE"
  - priority: "Agent_4_AceWriter"
  - scope: "paragraph_2"
  - revision_count: 1

输出: qa_report (REJECTED)
```

### 示例3: 严重问题

```
输入: UCO.content.full_text

检查结果:
  - fact_check: FAIL (4.0/10)
  - compliance: FAIL (0.0/10) - 有医疗承诺

诊断:
  - 1个CRITICAL问题（"治疗高血压"）
  - 3个HIGH问题

路由决策:
  - action: "CRITICAL_ERROR"
  - target: "User"
  - reason: "医疗合规问题，需人工审核"

输出: qa_report (CRITICAL_ERROR)
```

---

## 📝 最佳实践

### 1. 最小干预原则

```yaml
原则: 能不改的就不改，能少改的就不多改

实施:
  - 只标记必须修改的问题
  - 给出具体的修改建议
  - 限制修改范围（特定段落）
  - 保护其他部分不被误改
```

### 2. 优先级排序

```yaml
优先级:
  1. 安全合规（一票否决）
  2. 事实准确性
  3. 人设一致性
  4. 逻辑流畅度
  5. 可读性

实施:
  - 按优先级排序问题
  - 优先解决高优先级问题
  - 低优先级作为建议
```

### 3. 可操作建议

```yaml
要求:
  - 不要只说"有问题"
  - 要明确"哪里有问题"
  - 要给出"怎么改"
  - 要说明"为什么"

示例:
  ❌ "语气不对"
  ✅ "第3段语气过于专业，建议用'我亲身体会'增加朴实感"
```

---

**维护者**: Content Factory Team
**最后更新**: 2026-01-20
