# Agent-Knowledge 交互映射表

> 标准作业程序(SOP)：每个Agent在特定时刻应该调用哪些数据接口

---

## 映射表总览

| Agent | 阶段 | 读取 | 写入 | 核心逻辑 |
|-------|------|------|------|----------|
| Agent 1 | 输入 | `persona.value_system`<br>`feedback_loop.failure` | - | 过滤热点 |
| Agent 2 | 研究 | `success_archives`<br>`persona.linguistic_style` | `viral_patterns` | 学习爆款 |
| Agent 3 | 设计 | `persona.linguistic_style`<br>`opinion_bank`<br>`story_database` | - | 设计大纲 |
| Agent 4 | 执行 | `persona.linguistic_style`<br>`story_database`<br>`fact_base` | - | 撰写正文 |
| Agent 5 | 质检 | `persona.full`<br>`fact_base` | - | 审查校对 |
| Agent 6 | 优化 | `persona.target_audience`<br>`success_archives` | - | 预测爆款 |
| Agent 8 | 分发 | - | `feedback_loop`<br>`performance` | 记录数据 |

---

## 详细交互规范

### Agent 1: 趋势观察员 (Trend Spotter)

**职责**: 发现选题机会

**读取数据**:
```json
{
  "persona": {
    "value_system": ["食疗为主", "不夸大功效", "不替代医疗"],
    "forbidden_topics": ["政治", "攻击同行"],
    "target_audience": {
      "primary": {
        "age_range": "45-70"
      }
    }
  },
  "knowledge": {
    "feedback_loop": {
      "failure_archive": {
        "common_issues": {
          "low_read": ["之前写过XX话题，阅读量极低"]
        }
      }
    }
  }
}
```

**过滤逻辑**:
1. 热点是否涉及医疗承诺？ → 如果是，过滤
2. 热点是否符合中老年关注？ → 如果不是，降权
3. 热点是否在失败档案中？ → 如果是，避开
4. 是否符合核心价值观？ → 如果不是，过滤

**输出**: 过滤后的选题列表

---

### Agent 2: 爆文分析师 (Deconstruction Analyst)

**职责**: 逆向工程爆款文章

**读取数据**:
```json
{
  "persona": {
    "linguistic_style": {
      "tone": "朴实、真诚"
    }
  },
  "knowledge": {
    "viral_patterns_database": {
      "headline_formulas": [...],
      "opening_hooks": [...],
      "structure_patterns": [...]
    },
    "success_archives": {
      "patterns": {
        "best_performing_headlines": [...]
      }
    }
  }
}
```

**分析逻辑**:
1. 拆解爆款文章结构（标题/开头/主体/结尾）
2. 提取关键词、金句、数据使用方式
3. 对比成功档案，找出共同模式
4. 生成"爆款DNA卡片"

**写入数据**:
```json
{
  "knowledge": {
    "viral_patterns_database": {
      "extracted_patterns": [
        {
          "pattern_id": "spring_liver_2024",
          "headline_formula": "[数字]种[功效]食材，[时间]必吃",
          "success_probability": 0.85
        }
      ]
    }
  }
}
```

---

### Agent 3: 首席架构师 (Chief Architect)

**职责**: 设计文章大纲

**读取数据**:
```json
{
  "persona": {
    "linguistic_style": {
      "logic_model": "问题-分析-解决",
      "sentence_patterns": [...]
    },
    "value_system": {
      "core_beliefs": [
        "食疗为主，药物为辅"
      ]
    }
  },
  "knowledge": {
    "opinion_case_bank": {
      "quotations": {
        "old_li_quotes": [
          "这8年护工生涯，把自己熬干了"
        ]
      },
      "personal_stories": [
        {
          "story_id": "story_001",
          "emotional_arc": "退休期待→护工艰辛→感悟养生"
        }
      ]
    }
  }
}
```

**设计逻辑**:
1. 确定文章类型（食谱/科普/辟谣/时令/体质）
2. 选择逻辑模型（基于老李思维习惯）
3. 引用金句作为小标题
4. 预埋故事引用位置
5. 生成结构化大纲

**输出**: 包含人设元素的大纲

---

### Agent 4: 王牌写手 (Ace Writer)

**职责**: 撰写正文

**读取数据**:
```json
{
  "persona": {
    "linguistic_style": {
      "sentence_length_pref": "short",
      "preferred_words": ["实在话", "老伙计"],
      "forbidden_words": ["yyds", "绝绝子"],
      "signature_phrases": ["我亲身体会", "亲身经历告诉我"]
    }
  },
  "knowledge": {
    "opinion_case_bank": {
      "personal_stories": {
        "检索关键词": "脾胃虚寒",
        "返回故事": "我自己用山药调理3个月的经历"
      }
    },
    "fact_base": {
      "nutrition": {
        "key_ingredients": {
          "yam_山药": {
            "检索": "山药功效",
            "返回": "山药性平，健脾养胃，人人可用"
          }
        }
      }
    }
  }
}
```

**撰写逻辑**:
1. 每句话检查句长（3-10字短句为主）
2. 实时过滤禁用词
3. 插入签名句
4. 引用故事案例
5. 核对事实数据
6. 添加元数据标注

**输出**: 老李口吻的正文

---

### Agent 5: 首席审查官 (Chief Reviewer)

**职责**: 质量检查与分诊

**读取数据**:
```json
{
  "persona": {
    "full": "完整人设作为基准",
    "forbidden_words": [...],
    "value_system": [...]
  },
  "knowledge": {
    "fact_base": {
      "verify": "韭菜能养肝？"
    },
    "asset_library": {
      "compliance_dictionary": {
        "absolute_words": ["最", "第一"],
        "safe_alternatives": {"最": "很"}
      }
    }
  }
}
```

**检查逻辑**:
1. **人设一致性**: 这句话像老李说的吗？
2. **事实准确性**: 数据与库中一致吗？
3. **合规性**: 有禁忌词吗？
4. **价值观**: 违背核心信念吗？
5. **路由决策**: 需要修改吗？找谁修改？

**输出**: 检查报告 + 路由决策

---

### Agent 6: 爆款预测师 (Virality Forecaster)

**职责**: 预测爆款潜力

**读取数据**:
```json
{
  "persona": {
    "identity": {
      "target_audience": "45-70岁中老年人"
    }
  },
  "knowledge": {
    "success_archive": {
      "patterns": {
        "平均情绪值": 7.5,
        "平均金句密度": "每300字1个"
      }
    },
    "failure_archive": {
      "common_issues": {
        "low_read": ["情绪价值不足"]
      }
    },
    "viral_patterns_database": {
      "emotion_triggers": [...]
    }
  }
}
```

**预测逻辑**:
1. 评分5个维度（情绪/实用/社交/新奇/时效）
2. 与成功档案拟合
3. 识别弱项
4. 给出优化建议

**输出**: 爆款指数报告

---

### Agent 8: 增长黑客 (Growth Hacker)

**职责**: 分发与数据追踪

**写入数据**:
```json
{
  "knowledge": {
    "feedback_loop": {
      "article_id": "art_001",
      "publish_date": "2026-01-20",
      "metrics": {
        "views": 10000,
        "shares": 500,
        "saves": 200,
        "comments": 50
      },
      "feedback_type": "success"
    },
    "success_archive": {
      "articles": [
        {
          "article_id": "art_001",
          "final_classification": "SUCCESS",
          "lessons_learned": "情绪价值高，金句密度适中"
        }
      ]
    }
  }
}
```

---

## 数据流转图

```
输入阶段:
  Agent 1 读取 persona.value_system
        ↓ 过滤
        输出: 选题列表

研究阶段:
  Agent 2 读取 success_archives
        ↓ 分析
        写入: viral_patterns

设计阶段:
  Agent 3 读取 persona.linguistic_style + opinion_bank
        ↓ 设计
        输出: 大纲

执行阶段:
  Agent 4 读取 persona.linguistic_style + story_database
        ↓ 撰写
        输出: 草稿

质检阶段:
  Agent 5 读取 persona.full + fact_base
        ↓ 检查
        输出: 审查报告 + 路由决策

优化阶段:
  Agent 6 读取 success_archives + persona.target_audience
        ↓ 预测
        输出: 爆款报告

分发阶段:
  Agent 8 写入 feedback_loop + performance
        ↓ 记录
        输出: 数据档案
```

---

**维护者**: Content Factory Team
**最后更新**: 2026-01-20
