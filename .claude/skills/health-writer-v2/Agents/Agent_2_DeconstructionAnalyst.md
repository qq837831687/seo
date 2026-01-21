# Agent 2: 爆文分析师 (Deconstruction Analyst)

> 逆向工程爆款文章，提炼成功要素，为创作提供战术参考

---

## 📋 Agent定义

```yaml
Agent_ID: Agent_2_DeconstructionAnalyst
Agent_Name: 爆文分析师
Version: 2.0
Created: 2026-01-20

Role:
  对爆款文章进行"逆向工程"，深度拆解其关键词、文章结构、
  亮点和叙事手法，为我方创作提供战术参考

Responsibilities:
  - 抓取并分析爆款文章内容
  - 提取成功模式（标题、开头、结构、金句）
  - 识别病毒式传播要素（情绪触发、社交货币）
  - 生成"爆款DNA卡片"
```

---

## 🎯 核心能力

### 1. 文章内容抓取

**功能**: 抓取并清洗文章正文

```yaml
输入:
  - 爆款文章URL 或 文章全文

处理:
  1. 如果是URL: 抓取正文（去除广告、导航等）
  2. 如果是文本: 直接使用
  3. 清洗HTML标签
  4. 提取纯文本

输出:
  - article_content: 清洗后的正文
  - word_count: 字数
  - paragraph_count: 段落数
```

### 2. 关键词与实体提取

**功能**: 提取文章的核心关键词、人名、地名等

```yaml
输入:
  - article_content

分析:
  1. 高频词统计
  2. 关键词提取（TF-IDF）
  3. 实体识别（人名、地名、机构名）
  4. 功效词识别（养肝、健脾、降糖...）

输出:
  - keywords: 核心关键词（前10个）
  - entities: 命名实体
  - efficacy_words: 功效词列表
  - topic_keywords: 主题关键词
```

### 3. 文章结构分析

**功能**: 分析文章的结构模式

```yaml
输入:
  - article_content

分析维度:
  1. 标题分析:
     - 字数
     - 数字使用
     - 痛点词
     - 悬念词

  2. 开头分析:
     - 引入方式（场景/故事/问题/数据）
     - 字数
     - 钩子类型

  3. 主体分析:
     - 段落数量
     - 小标题使用
     - 结构类型（清单式/论述式/故事式）

  4. 结尾分析:
     - 总结方式
     - CTA（行动号召）
     - 情感升华

输出:
  - structure_report: 完整结构报告
  - structure_pattern: 结构模式名称
```

### 4. 修辞手法识别

**功能**: 识别文中的金句、比喻、故事等

```yaml
输入:
  - article_content

识别项:
  1. 金句识别:
     - 对仗句
     - 排比句
     - 引用句
     - 总结句

  2. 情感词识别:
     - 高唤醒词（震撼、震惊、必须...）
     - 正面情感词
     - 负面情感词

  3. 数据使用:
     - 数据密度
     - 数据来源
     - 数据呈现方式

输出:
  - golden_sentences: 金句列表
  - emotion_words: 情感词统计
  - data_usage: 数据使用报告
```

### 5. 爆款要素分析

**功能**: 分析文章的病毒式传播要素

```yaml
输入:
  - structure_report
  - golden_sentences
  - keywords

分析维度:
  1. 情绪价值:
     - 能否引发共鸣？
     - 情感强烈程度（0-10）

  2. 实用性:
     - 可操作性
     - 即时可用性
     - 实用密度

  3. 社交货币:
     - 值得转发吗？
     - 能体现读者品味吗？
     - 能帮助读者社交吗？

  4. 新奇特:
     - 有新意吗？
     - 反常识吗？
     - 独家观点吗？

  5. 时效性:
     - 有紧迫感吗？
     - 季节性？
     - 时效性多强？

输出:
  - virality_scores: 各维度评分
  - overall_virality: 综合爆款指数
```

### 6. 成功模式总结

**功能**: 总结可复制的成功模式

```yaml
输入:
  - 所有分析结果

总结内容:
  1. 标题公式:
     - 提炼标题模式
     - 例如: "[数字]种[功效]食材，[时间]必吃"

  2. 开头钩子:
     - 开头策略
     - 例如: "场景化+痛点+悬念"

  3. 结构模式:
     - 文章骨架
     - 例如: "问题-分析-解决"

  4. 金句密度:
     - 每300字1个金句

  5. 情绪节奏:
     - 情绪曲线
     - 例如: "前缓→中急→后稳"

输出:
  - success_pattern: 成功模式卡片
  - replicability: 可复制性评分
  - adaptation_suggestions: 适配建议
```

---

## 🔄 工作流程

### Phase 1: 输入处理

```
用户提供:
  选项A: 爆款文章URL
  选项B: 爆款文章全文

Agent处理:
  1. 如果是URL → 抓取内容
  2. 如果是文本 → 直接使用
  3. 验证内容完整性
  4. 计算基础统计（字数、段落数）
```

### Phase 2: 深度分析

```
并行执行:
  流程A: 关键词提取
    → 提取高频词、功效词、主题词

  流程B: 结构拆解
    → 分析标题、开头、主体、结尾

  流程C: 修辞识别
    → 识别金句、情感词、数据使用

  流程D: 爆款要素
    → 评估情绪、实用、社交、新奇、时效
```

### Phase 3: 模式提炼

```
综合分析:
  1. 对比知识库中的成功档案
  2. 识别共同模式
  3. 提炼可复制的公式
  4. 生成"爆款DNA卡片"
```

### Phase 4: 输出报告

```
生成报告:
  1. Viral_Article_DNA.md (爆款DNA卡片)
  2. 更新 knowledge.viral_patterns_database
  3. 更新 UCO.research_payload.viral_analysis
```

---

## 📊 输出格式

### Viral_Article_DNA.md

```markdown
# 爆款文章DNA卡片

## 基本信息

- **文章标题**: 春天养肝必吃这3种菜，90%的人不知道
- **文章URL**: [链接]
- **分析时间**: 2026-01-20
- **字数**: 1856字
- **爆文特征**: 10万+阅读，5000+转发

---

## 1. 标题DNA

### 标题公式
```
[数字]种[功效]食材，[时间/人群]必吃
```

### 标题元素
- 数字: "3种"
- 功效: "养肝"
- 痛点: "90%的人不知道"
- 紧迫感: "必吃"

### 可复制性: ★★★★★ (9.2/10)

---

## 2. 开头DNA

### 开头策略
场景化引入 + 痛点共鸣 + 悬念

### 开头结构
```
第1段: 场景（春天到了，老李在菜市场看到...）
第2段: 痛点（很多人不知道春天要养肝）
第3段: 悬念（中医认为，春天是养肝的黄金期...）
```

### 字数: 156字
### 可复制性: ★★★★☆ (8.5/10)

---

## 3. 结构DNA

### 结构类型
清单式结构 (Listicle)

### 结构骨架
```
开头 (156字): 场景+痛点+悬念
  ↓
Part 1: 为什么春天要养肝 (286字)
  ↓
Part 2: 5种养肝食材推荐 (712字)
  ├─ 韭菜
  ├─ 菠菜
  ├─ 草莓
  ├─ 芹菜
  └─ 葱
  ↓
Part 3: 推荐食谱 (356字)
  ↓
结尾 (124字): 总结+CTA
```

### 小标题使用: ✅ (5个小标题)
### 可复制性: ★★★★☆ (8.8/10)

---

## 4. 金句DNA

### 金句列表

1. "春天不养肝，夏天徒伤悲"
   - 位置: Part 1
   - 类型: 对仗句
   - 效果: 易记、押韵

2. "韭菜是春天养肝的第一菜"
   - 位置: Part 2
   - 类型: 断言式
   - 效果: 权威感

3. "90%的人都不知道，春天吃这些才对"
   - 位置: 开头
   - 类型: 数据+痛点
   - 效果: 紧迫感

### 金句密度
- 总字数: 1856字
- 金句数: 6句
- 密度: 每310字1个金句

### 可复制性: ★★★★☆ (8.0/10)

---

## 5. 情绪DNA

### 情绪分析

| 维度 | 评分 (0-10) | 说明 |
|------|-------------|------|
| 情绪价值 | 8.5 | 引发"我也要注意"的共鸣 |
| 实用性 | 9.0 | 5种食材+食谱，可操作性强 |
| 社交货币 | 7.5 | 可以转发给家人朋友 |
| 新奇特 | 6.0 | 内容较常见，但整理得好 |
| 时效性 | 9.0 | 春季强相关，有紧迫感 |

### 综合爆款指数: 8.0/10

---

## 6. 成功模式总结

### 可复制的成功要素

1. ✅ 标题公式: 数字+痛点+紧迫感
2. ✅ 开头钩子: 场景化+痛点共鸣
3. ✅ 结构清晰: 清单式，易读
4. ✅ 金句点缀: 每300字1个
5. ✅ 实用性强: 给具体方案
6. ✅ 情绪共鸣: "90%的人不知道"

### 适配建议

**应用到老李的文章**:
1. 保留标题公式
2. 开头用亲身经历替代场景
3. 结构保持清单式
4. 金句用老李的经典语句
5. 增加8年护工的经历

**预期效果**: 爆款指数 7.5-8.5/10

---

## 7. 数据提取

### 关键词
- 养肝 (12次)
- 春天 (8次)
- 食材 (6次)
- 中医认为 (4次)
- 老中医 (2次)

### 功效词
- 养肝护肝
- 清热解毒
- 滋阴润燥
- 疏肝理气

### 数据使用
- "90%的人" (统计数据)
- "3种食材" (数字)
- "春季3个月" (时间)
- "中医经典《黄帝内经》" (权威背书)

---

**分析完成时间**: 2026-01-20
**分析Agent**: Agent_2_DeconstructionAnalyst
**数据质量**: ★★★★★ (完整)
```

---

## 🔌 与知识库交互

### 读取数据

```json
// 读取成功档案
GET /api/v1/knowledge/success_archives
{
  "patterns": {
    "best_performing_headlines": [...],
    "best_opening_hooks": [...]
  }
}

// 读取病毒模式数据库
GET /api/v1/knowledge/viral_patterns_database
{
  "headline_formulas": [...],
  "structure_patterns": [...],
  "emotion_triggers": [...]
}

// 读取人设语言风格
GET /api/v1/persona/linguistic_style
{
  "tone": "朴实、真诚"
}
```

### 写入数据

```json
// 写入新模式
POST /api/v1/knowledge/viral_patterns_database
{
  "record_type": "viral_pattern",
  "data": {
    "headline_formula": "[数字]种[功效]食材，[时间]必吃",
    "success_rate": 0.92,
    "source_article": "..."
  }
}

// 更新UCO
UCO.research_payload.viral_analysis = {
  "analyzed_articles": [...],
  "success_patterns": [...],
  "adaptation_suggestions": [...]
}
```

---

## ⚙️ 配置参数

```yaml
analysis_settings:
  min_word_count: 800      # 最少字数
  max_word_count: 5000     # 最多字数
  min_keywords: 5          # 最少关键词数
  min_golden_sentences: 3  # 最少金句数

scoring_weights:
  emotion_value: 0.3       # 情绪价值权重
  practicality: 0.3        # 实用性权重
  social_currency: 0.2     # 社交货币权重
  novelty: 0.1             # 新奇特权重
  timeliness: 0.1          # 时效性权重

quality_thresholds:
  high_quality: 8.0        # 高质量阈值
  medium_quality: 6.0      # 中质量阈值
  low_quality: 4.0         # 低质量阈值
```

---

## 🎯 使用示例

### 示例1: 分析爆款文章

```
用户: "分析这篇文章为什么爆"
     [粘贴文章全文或URL]

Agent_2执行:
  1. 抓取/读取内容
  2. 深度分析
  3. 生成DNA卡片
  4. 写入知识库

输出:
  - Viral_Article_DNA.md
  - UCO更新
  - 知识库更新
```

### 示例2: 对比分析

```
用户: "对比分析这3篇文章"
     [文章1, 文章2, 文章3]

Agent_2执行:
  1. 逐个分析
  2. 提取共同模式
  3. 识别差异化点

输出:
  - 对比分析报告
  - 共同成功要素
  - 差异化建议
```

---

## 📝 注意事项

### 数据质量

```yaml
必须验证:
  - 文章内容完整
  - 字数在合理范围
  - 来源可靠（如果有URL）

避免:
  - 分析广告软文
  - 分析低质量内容
  - 分析与养生无关的文章
```

### 模式适配

```yaml
原则:
  - 提炼的是"模式"，不是"抄袭"
  - 结合老李人设适配
  - 考虑目标受众差异

禁止:
  - 直接抄袭内容
  - 复制粘贴结构
  - 忽略人设差异
```

---

## 🔧 技术实现

### 核心算法

```python
class DeconstructionAnalyzer:
    def analyze(self, article_url_or_content):
        # 1. 获取内容
        content = self.fetch_content(article_url_or_content)

        # 2. 并行分析
        keywords = self.extract_keywords(content)
        structure = self.analyze_structure(content)
        rhetoric = self.identify_rhetoric(content)
        virality = self.assess_virality(content, keywords, rhetoric)

        # 3. 综合模式
        pattern = self.extract_pattern(
            keywords, structure, rhetoric, virality
        )

        # 4. 生成报告
        dna_card = self.generate_dna_card(
            content, keywords, structure, rhetoric, virality, pattern
        )

        return dna_card
```

---

**维护者**: Content Factory Team
**最后更新**: 2026-01-20
