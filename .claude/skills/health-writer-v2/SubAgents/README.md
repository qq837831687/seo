# SubAgents 目录

本目录包含 Health Writer V2 系统的虚拟机式 SubAgent 实现。

## 什么是 SubAgent？

SubAgent 是基于 Claude Code Task 工具的虚拟机式 Agent，具有以下特点：
- **独立运行**：每个 SubAgent 在独立的虚拟机环境中执行
- **状态隔离**：SubAgent 之间不共享状态，通过 UCO 对象传递数据
- **可编排**：SubAgent 可以协调其他 Agent 或 SubAgent
- **可重入**：同一个 SubAgent 可以同时处理多个任务

## 目录结构

```
SubAgents/
├── ArticleFactory/          # 文章工厂 SubAgent
│   ├── agent.md            # SubAgent 规范文档
│   ├── implementation.py   # Python 实现代码
│   ├── test_cases.json     # 测试用例
│   └── README.md           # 快速开始指南
└── README.md               # 本文件
```

## ArticleFactory - 文章工厂

### 简介
ArticleFactory 是系统的核心 SubAgent，负责协调 Agent 2-7，一键生成爆款养生文章。

### 功能
- ✅ 一键生成：从话题到成稿，全程自动化
- ✅ 智能路由：自动处理修改循环，优化文章质量
- ✅ 多种模式：标准/应急/高质量
- ✅ UCO 跟踪：完整的状态管理和日志记录

### 快速使用

```python
from implementation import ArticleFactory

factory = ArticleFactory()

result = factory.generate_article(
    topic="立春养肝",
    topic_source="CHRONOS_RECOMMENDATION",
    target_audience={"age_group": "60-70", "gender": "all"}
)

if result["success"]:
    print(f"标题: {result['article']['title']}")
    print(f"耗时: {result['workflow_report']['total_time']} 分钟")
```

### 详细文档
- [ArticleFactory 规范文档](./ArticleFactory/agent.md)
- [ArticleFactory 快速开始](./ArticleFactory/README.md)
- [ArticleFactory 测试用例](./ArticleFactory/test_cases.json)

---

## 未来 SubAgent 计划

### Phase 2: ChronosScheduler (时令调度器)
- 功能：实时监控节气、天气、节日，自动触发内容生成
- 协作：调用 ArticleFactory 生成文章

### Phase 3: KnowledgeKeeper (知识库维护员)
- 功能：自动扫描、提取、合并新知识到知识库
- 特性：智能冲突解决、版本管理

### Phase 4: ViralHunter (热点猎手)
- 功能：实时抓取社交媒体热点，分析爆款模式
- 协作：为 ArticleFactory 提供热点话题

---

## SubAgent 开发规范

### 1. 目录结构
每个 SubAgent 应包含：
```
SubAgentName/
├── agent.md              # 规范文档（必需）
├── implementation.py     # 实现代码（必需）
├── test_cases.json       # 测试用例（推荐）
└── README.md            # 使用指南（推荐）
```

### 2. 规范文档模板
参考 `ArticleFactory/agent.md`，应包含：
- SubAgent 信息（ID、名称、版本）
- 核心职责与工作模式
- 输入/输出协议
- 工作流程设计
- 数据流与状态管理
- 错误处理机制
- 使用示例

### 3. 实现代码规范
参考 `ArticleFactory/implementation.py`，应包含：
- 类定义（继承基础类）
- 主入口方法（如 `generate_article`）
- Agent 调用方法（`_call_agent_X`）
- 结果组装方法
- 日志记录
- 错误处理

### 4. 测试用例规范
参考 `ArticleFactory/test_cases.json`，应包含：
- 功能测试（核心功能）
- 路由逻辑测试（决策分支）
- 边界条件测试（极端情况）
- 质量测试（输出质量）
- 性能测试（响应时间）

---

## SubAgent 协作模式

### 1. 层级协作
```
Orchestrator (编排器)
    ↓
ChronosScheduler (时令调度器)
    ↓
ArticleFactory (文章工厂)
    ↓
Agent 2, 3, 4, 5, 6, 7 (专业 Agent)
```

### 2. 数据传递
- 所有 SubAgent 和 Agent 通过 UCO 对象传递数据
- UCO 对象包含：状态、内容数据、元数据、日志
- 每个 Agent/SubAgent 读取和更新 UCO

### 3. 错误处理
- SubAgent 应捕获并处理内部错误
- 无法处理的错误应升级给 Orchestrator
- 所有错误应记录日志

---

## 集成到系统

### 1. 在 Orchestrator 中调用

```python
from SubAgents.ArticleFactory.implementation import ArticleFactory

# 创建 SubAgent 实例
factory = ArticleFactory()

# 调用 SubAgent
result = factory.generate_article(
    topic=topic_from_user,
    topic_source="USER_MANUAL"
)

# 处理结果
if result["success"]:
    # 保存到数据库
    # 发送通知
    # ...
```

### 2. 作为 Skill 暴露

在 `SKILL.md` 中添加：
```yaml
SubAgents:
  ArticleFactory:
    description: "一键生成爆款文章"
    usage: "调用 generate_article() 方法"
    documentation: "SubAgents/ArticleFactory/README.md"
```

---

## 维护与更新

### 版本管理
- 每个更新应更新版本号
- 在 `agent.md` 中记录版本历史
- 重大变更应更新 `CHANGELOG.md`

### 测试
- 每次修改后运行测试
- 确保所有测试用例通过
- 新功能应添加新测试用例

### 文档
- 保持文档与代码同步
- 更新使用示例
- 记录已知问题和限制

---

## 联系方式

- **问题反馈**: 在 GitHub Issues 中提交
- **功能建议**: 在 Discussions 中讨论
- **贡献代码**: 提交 Pull Request

---

**创建时间**: 2026-01-20
**最后更新**: 2026-01-20
**维护者**: Health Writer V2 Team
