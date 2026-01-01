# 🍵 养生/饮食热点 + SEO长尾词挖掘器

> 自动挖掘养生饮食领域的热点话题和高价值SEO长尾词

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ 功能特点

- **多数据源抓取**: 百度下拉、B站搜索、淘宝搜索、知乎热榜、微博热搜
- **智能评分算法**: 基于搜索意图、关键词长度、领域相关度等维度评分
- **意图标签识别**: 自动识别疑问/功效/副作用/购买/对比/食谱等6种意图
- **爆款标题生成**: 根据关键词和意图自动生成爆款标题建议
- **历史数据对比**: 保存每次运行的历史记录，便于追踪热点变化
- **定时任务支持**: 支持设置定时自动运行
- **多种输出格式**: Markdown表格、CSV、JSON

## 📊 输出内容

### 1. 热点选题 TOP10 (`output/hot_topics.md`)
- 包含标题、来源、争议点、适合写的角度
- 每个选题配有爆款标题建议

### 2. SEO关键词 (`output/seo_keywords.md` / `.csv` / `.json`)
- 关键词来源（百度/B站/淘宝等）
- 意图标签
- 推荐指数（评分）
- 爆款标题建议

### 3. 历史数据 (`history/history_*.json`)
- 保存每次运行的关键词和热点数据
- 便于追踪热点变化趋势

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <your-repo-url>
cd <project-directory>

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行脚本

```bash
python health_hot_seo_hunter.py
```

### 3. 查看结果

```bash
# 打开输出目录
open output  # Mac
# 或
explorer output  # Windows
```

## ⚙️ 定时任务设置

### 自动设置（推荐）

```bash
# 给脚本添加执行权限
chmod +x setup_cron.sh

# 运行设置脚本
./setup_cron.sh
```

根据提示选择运行频率：
- 每小时
- 每6小时
- 每12小时
- 每天早上9点
- 每天晚上9点
- 自定义

### 手动运行

```bash
./run_hunter.sh
```

### 查看定时任务

```bash
crontab -l
```

### 查看运行日志

```bash
tail -f logs/cron.log
```

## 📝 评分规则

| 维度 | 加分 | 说明 |
|------|------|------|
| 疑问高意图 | +6 | 包含"怎么/为什么/真的/副作用"等词 |
| 购买意图 | +5 | 包含"排行榜/推荐/价格/怎么买"等词 |
| 长度≥10字 | +4 | 长尾词，更具体 |
| 长度≥8字 | +3 | 较长关键词 |
| 长度≥6字 | +2 | 中等长度 |
| 领域强相关 | +3 | 包含"控糖/抗炎/减脂"等领域词 |
| 紧迫感关键词 | +2 | 包含"快速/立即/最佳"等词 |
| 包含数字 | +1 | 更具体的关键词 |

## 🎯 意图标签说明

| 标签 | 说明 | 示例关键词 |
|------|------|-----------|
| 疑问 | 用户提问类 | 怎么养生、为什么控糖 |
| 功效 | 寻找功效/好处 | 养生功效、控糖好处 |
| 副作用 | 关注副作用/风险 | 控糖副作用、养生危害 |
| 购买 | 购买意向 | 控糖产品推荐、养生茶价格 |
| 对比 | 对比选择 | 控糖vs生酮、养生茶哪个好 |
| 食谱 | 寻找食谱 | 控糖食谱、减脂餐做法 |

## 📁 项目结构

```
.
├── health_hot_seo_hunter.py   # 主程序
├── setup_cron.sh              # 定时任务设置脚本
├── run_hunter.sh              # 自动运行脚本（自动生成）
├── requirements.txt           # 依赖包列表
├── README.md                  # 项目文档
├── .gitignore                 # Git忽略文件
├── output/                    # 输出目录
│   ├── hot_topics.md          # 热点选题
│   ├── seo_keywords.md        # SEO关键词(Markdown)
│   ├── seo_keywords.csv       # SEO关键词(CSV)
│   └── seo_keywords.json      # SEO关键词(JSON)
├── history/                   # 历史数据目录
│   └── history_*.json         # 历史记录
└── logs/                      # 日志目录
    └── cron.log               # 定时任务日志
```

## 🔧 配置说明

### 修改种子词

编辑 `health_hot_seo_hunter.py` 中的 `SEED_KEYWORDS` 列表：

```python
SEED_KEYWORDS = [
    "养生", "饮食", "控糖", "抗炎饮食", "减脂餐",
    "祛湿", "补气血", "养胃", "熬夜"
]
```

### 修改输出目录

编辑 `health_hot_seo_hunter.py` 中的配置：

```python
OUTPUT_DIR = "output"
HISTORY_DIR = "history"
```

## ⚠️ 注意事项

1. **反爬限制**: 部分数据源（知乎、微博）可能有反爬限制，脚本会自动使用备用数据生成方案
2. **请求频率**: 脚本内置了随机延迟，避免请求过快被封
3. **网络环境**: 确保网络连接正常，部分数据源需要访问国内网站
4. **定时任务**: 确保系统有cron服务（Linux/Mac）或任务计划程序（Windows）

## 📊 数据来源

| 数据源 | 类型 | 说明 |
|--------|------|------|
| 百度下拉 | 搜索建议 | 百度搜索框的自动推荐 |
| B站搜索 | 搜索建议 | Bilibili搜索框的自动推荐 |
| 淘宝搜索 | 搜索建议 | 淘宝搜索框的自动推荐 |
| 知乎热榜 | 热点话题 | 知乎平台的热门话题 |
| 微博热搜 | 热点话题 | 微博平台的热搜榜单 |

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 作者

Created with ❤️ for SEO and content creators

---

**如果觉得有帮助，请给个 ⭐ Star！**
