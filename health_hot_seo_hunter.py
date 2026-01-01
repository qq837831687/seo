#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
养生/饮食热点 + SEO长尾词挖掘器 v2.0
多数据源抓取 + 意图识别 + 评分排序 + 历史对比
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
import random
from urllib.parse import quote
from datetime import datetime
import csv
import os
from pathlib import Path

# ==================== 配置 ====================
SEED_KEYWORDS = [
    "养生", "饮食", "控糖", "抗炎饮食", "减脂餐",
    "祛湿", "补气血", "养胃", "熬夜"
]

OUTPUT_DIR = "output"
HISTORY_DIR = "history"
CONFIG_FILE = "config.json"

# 请求配置（避免被封）
HEADERS_LIST = [
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"}
]

TIMEOUT = 10


# ==================== 工具函数 ====================
def get_random_headers():
    """获取随机请求头"""
    headers = random.choice(HEADERS_LIST).copy()
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    headers["Accept-Language"] = "zh-CN,zh;q=0.9,en;q=0.8"
    return headers


def safe_request(url, params=None, source_name=""):
    """安全请求，失败返回None"""
    try:
        time.sleep(random.uniform(0.3, 1.0))  # 减少延迟
        headers = get_random_headers()
        resp = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)
        if resp.status_code == 200:
            return resp
        print(f"  ⚠️  {source_name}: HTTP {resp.status_code}")
        return None
    except Exception as e:
        print(f"  ⚠️  {source_name}: {type(e).__name__}")
        return None


def calculate_score(keyword):
    """计算关键词推荐指数（优化版）"""
    score = 0

    # 疑问高意图（权重提升）
    if any(w in keyword for w in ["怎么", "为什么", "真的", "副作用", "危害", "能不能", "多久", "有用吗", "有效吗", "是否", "如何"]):
        score += 6

    # 购买意图
    if any(w in keyword for w in ["排行榜", "推荐", "哪个牌子", "价格", "怎么买", "测评", "京东", "淘宝", "购买", "哪里买"]):
        score += 5

    # 长尾词（分级加分）
    length = len(keyword)
    if length >= 10:
        score += 4
    elif length >= 8:
        score += 3
    elif length >= 6:
        score += 2

    # 领域强相关
    if any(w in keyword for w in ["控糖", "抗炎", "减脂", "祛湿", "养胃", "补气血", "熬夜", "养生", "饮食"]):
        score += 3

    # 紧迫感关键词
    if any(w in keyword for w in ["快速", "立即", "马上", "紧急", "最佳", "最好", "必须"]):
        score += 2

    # 数字关键词（通常更具体）
    if re.search(r'\d+', keyword):
        score += 1

    return score


def detect_intent(keyword):
    """检测意图标签（增强版）"""
    intents = []

    if any(w in keyword for w in ["怎么", "为什么", "如何", "什么", "是否", "能不能", "有用吗", "有效吗", "方法"]):
        intents.append("疑问")
    if any(w in keyword for w in ["功效", "作用", "好处", "益处", "效果"]):
        intents.append("功效")
    if any(w in keyword for w in ["副作用", "危害", "风险", "禁忌", "注意事项"]):
        intents.append("副作用")
    if any(w in keyword for w in ["排行榜", "推荐", "哪个牌子", "价格", "怎么买", "测评", "购买", "哪里买"]):
        intents.append("购买")
    if any(w in keyword for w in ["和", "vs", "VS", "还是", "对比", "区别"]):
        intents.append("对比")
    if any(w in keyword for w in ["食谱", "菜单", "吃什么", "做法"]):
        intents.append("食谱")

    return "/".join(intents) if intents else "通用"


def generate_catchy_title(keyword, intent):
    """生成爆款标题建议（优化版）"""
    templates = {
        "疑问": [
            f"{keyword}？真相让人意外",
            f"医生不说，但{keyword}你必须知道",
            f"90%的人都不知道的{keyword}真相",
            f"{keyword}！看完这篇你就懂了",
        ],
        "功效": [
            f"{keyword}的5个神奇效果，第3个很多人不知道",
            f"坚持{keyword}，30天后身体的变化",
            f"为什么明星都在{keyword}？效果惊人",
        ],
        "副作用": [
            f"{keyword}的副作用，再不知道就晚了",
            f"别乱{keyword}！这3类人要注意",
            f"{keyword}的禁忌，很多人第一个就错了",
        ],
        "购买": [
            f"{keyword}排行榜TOP5，第1名没想到",
            f"买前必看！{keyword}避坑指南",
            f"{keyword}怎么选？内行人告诉你真相",
        ],
        "对比": [
            f"{keyword}：一文看懂区别",
            f"到底选哪个？{keyword}深度对比",
            f"别再纠结了！{keyword}选哪个最好",
        ],
        "食谱": [
            f"{keyword}大全，7天不重样",
            f"营养师的{keyword}秘诀",
            f"7天{keyword}计划，效果看得见",
        ],
        "通用": [
            f"{keyword}：新手完全指南",
            f"关于{keyword}，你需要知道的一切",
            f"{keyword}的正确打开方式",
        ]
    }

    intent_key = intent.split("/")[0] if intent else "通用"
    templates_list = templates.get(intent_key, templates["通用"])
    return random.choice(templates_list)


def save_history(keywords, topics):
    """保存历史数据"""
    os.makedirs(HISTORY_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    history_data = {
        "timestamp": timestamp,
        "datetime": datetime.now().isoformat(),
        "keywords_count": len(keywords),
        "topics_count": len(topics),
        "top_keywords": [kw for kw, _ in list(keywords.items())[:20]],
        "topics": [t["title"] for t in topics[:10]]
    }

    history_file = f"{HISTORY_DIR}/history_{timestamp}.json"
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history_data, f, ensure_ascii=False, indent=2)

    print(f"✅ 已保存历史数据: {history_file}")


def load_recent_history(limit=5):
    """加载最近的历史记录"""
    if not os.path.exists(HISTORY_DIR):
        return []

    files = sorted(Path(HISTORY_DIR).glob("history_*.json"), reverse=True)[:limit]
    history = []

    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                history.append(data)
        except:
            pass

    return history


# ==================== 数据源抓取 ====================
def fetch_baidu_suggestions(keyword):
    """百度下拉词"""
    url = "http://suggestion.baidu.com/su"
    params = {"wd": keyword, "cb": "cb"}

    print(f"  🔍 百度: {keyword}")
    resp = safe_request(url, params, "百度下拉")

    if not resp:
        return []

    try:
        text = resp.text
        match = re.search(r'cb\((.*)\)', text)
        if match:
            json_str = match.group(1)
            try:
                json_str = json_str.encode('latin1').decode('gb2312')
            except:
                pass
            data = json.loads(json_str)
            if isinstance(data, dict) and "s" in data:
                return data.get("s", [])
    except:
        pass
    return []


def fetch_bilibili_suggestions(keyword):
    """B站搜索建议"""
    url = "https://s.search.bilibili.com/main/suggest"
    params = {"term": keyword}

    print(f"  🔍 B站: {keyword}")
    resp = safe_request(url, params, "B站建议")

    if not resp:
        return []

    try:
        data = resp.json()
        if isinstance(data, dict) and "result" in data:
            return [item.get("value", "") for item in data.get("result", []) if "value" in item]
    except:
        pass
    return []


def fetch_taobao_suggestions(keyword):
    """淘宝搜索建议"""
    url = "https://suggest.taobao.com/sug"
    params = {"q": keyword, "code": "utf-8"}

    print(f"  🔍 淘宝: {keyword}")
    resp = safe_request(url, params, "淘宝建议")

    if not resp:
        return []

    try:
        data = resp.json()
        return data.get("result", [])
    except:
        pass
    return []


def fetch_zhihu_hot():
    """知乎热榜"""
    url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"

    print(f"  🔍 知乎热榜")
    resp = safe_request(url, source_name="知乎热榜")

    if not resp:
        return []

    try:
        data = resp.json()
        items = data.get("data", [])
        results = []
        for item in items[:30]:
            target = item.get("target", {})
            title = target.get("title", "")
            if title:
                results.append(title)
        return results
    except:
        pass
    return []


def fetch_weibo_hot():
    """微博热搜"""
    url = "https://weibo.com/ajax/side/hotSearch"

    print(f"  🔍 微博热搜")
    resp = safe_request(url, source_name="微博热搜")

    if not resp:
        return []

    try:
        data = resp.json()
        items = data.get("data", {}).get("realtime", [])
        return [item.get("word", "") for item in items]
    except:
        pass
    return []


# ==================== 备用数据生成 ====================
def generate_fallback_keywords():
    """生成备用关键词"""
    prefixes = ["怎么", "为什么", "如何", "最好的", "快速", "有效", "安全", "科学"]
    suffixes = ["方法", "食谱", "食物", "水果", "蔬菜", "茶", "注意事项", "危害", "好处", "时间", "排行榜", "推荐", "禁忌", "食谱大全", "一周计划"]
    questions = ["真的有用吗", "副作用是什么", "多久见效", "能不能天天吃", "哪些人不能吃", "什么时候吃最好", "正确打开方式", "避坑指南"]

    generated = []
    for seed in SEED_KEYWORDS:
        for prefix in prefixes[:5]:
            generated.append(f"{prefix}{seed}")
        for suffix in suffixes[:8]:
            generated.append(f"{seed}{suffix}")
        for q in questions[:5]:
            generated.append(f"{seed}{q}")

    return generated


def generate_fallback_hot_topics():
    """生成备用热点选题"""
    topics = [
        "控糖饮食真的能抗衰老吗？哈佛研究揭示真相",
        "抗炎饮食食物排行榜TOP10，第一名你肯定想不到",
        "熬夜后怎么补救？医生推荐的3个黄金时间点",
        "祛湿食物排行榜：红豆薏米水排第几？",
        "减脂餐一周食谱，不掉秤是因为你没吃对",
        "养胃食物排行榜：这些食物越吃胃越难受",
        "补气血食物TOP10，阿胶红枣排第几？",
        "抗炎饮食vs生酮饮食，哪个更适合中国人？",
        "控糖饮食一周食谱，告别糖尿病风险",
        "祛湿的最好方法，不是红豆薏米水！"
    ]
    return [{"title": t, "source": "热点模拟", "angle": "争议/科普型"} for t in topics]


# ==================== 主逻辑 ====================
def main():
    start_time = time.time()
    print("=" * 70)
    print("🍵 养生/饮食热点 + SEO长尾词挖掘器 v2.0")
    print("=" * 70)

    all_keywords = {}
    hot_topics = []

    # 1. 基于种子词抓取各平台的建议词
    print("\n📊 第一阶段：基于种子词抓取搜索建议")
    print("-" * 70)

    for keyword in SEED_KEYWORDS:
        print(f"\n🌱 种子词: [{keyword}]")

        # 多源并行
        baidu_results = fetch_baidu_suggestions(keyword)
        for kw in baidu_results:
            if kw not in all_keywords:
                all_keywords[kw] = {"sources": [], "score": 0, "intent": ""}
            all_keywords[kw]["sources"].append("百度")

        bili_results = fetch_bilibili_suggestions(keyword)
        for kw in bili_results:
            if kw not in all_keywords:
                all_keywords[kw] = {"sources": [], "score": 0, "intent": ""}
            all_keywords[kw]["sources"].append("B站")

        taobao_results = fetch_taobao_suggestions(keyword)
        for kw in taobao_results:
            if isinstance(kw, str) and kw:
                if kw not in all_keywords:
                    all_keywords[kw] = {"sources": [], "score": 0, "intent": ""}
                all_keywords[kw]["sources"].append("淘宝")

        time.sleep(random.uniform(0.5, 1.0))

    # 2. 抓取热榜
    print("\n\n📊 第二阶段：抓取平台热榜")
    print("-" * 70)

    zhihu_hot = fetch_zhihu_hot()
    for title in zhihu_hot:
        if any(kw in title for kw in SEED_KEYWORDS):
            hot_topics.append({"title": title, "source": "知乎热榜", "angle": "争议/问题型"})

    weibo_hot = fetch_weibo_hot()
    if not weibo_hot:
        print("  ⚠️  微博热搜已跳过（反爬限制）")
    else:
        for title in weibo_hot:
            if any(kw in title for kw in SEED_KEYWORDS):
                hot_topics.append({"title": title, "source": "微博热搜", "angle": "热点追踪"})

    # 3. 如果外部源全部失败，使用备用数据
    if not all_keywords and not hot_topics:
        print("\n  ⚠️  所有外部数据源均不可用，启用备用数据生成方案")
        print("-" * 70)

        fallback_keywords = generate_fallback_keywords()
        for kw in fallback_keywords:
            all_keywords[kw] = {"sources": ["备用生成"], "score": 0, "intent": ""}
        hot_topics = generate_fallback_hot_topics()

    # 4. 计算分数和意图
    print("\n\n📊 第三阶段：分析关键词")
    print("-" * 70)

    for kw, data in all_keywords.items():
        data["score"] = calculate_score(kw)
        data["intent"] = detect_intent(kw)
        data["catchy_title"] = generate_catchy_title(kw, data["intent"])
        data["source"] = "+".join(set(data["sources"]))

    sorted_keywords = sorted(all_keywords.items(), key=lambda x: x[1]["score"], reverse=True)
    sorted_topics = sorted(hot_topics, key=lambda x: len(x["title"]), reverse=True)

    # 5. 生成输出文件
    print("\n\n📊 第四阶段：生成输出文件")
    print("-" * 70)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 5.1 热点选题 TOP10
    hot_topics_md = f"""# 养生/饮食热点选题 TOP10

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> 数据源: {'+'.join(set([t['source'] for t in hot_topics])) if hot_topics else '备用生成'}

---

"""
    for i, topic in enumerate(sorted_topics[:10], 1):
        hot_topics_md += f"""## {i}. {topic['title']}

- **来源**: {topic['source']}
- **争议点/角度**: {topic['angle']}
- **适合写的角度**: 深度解析 / 避坑指南 / 科普向
- **💥 爆款标题建议**: {topic['title'][:40]}...这篇告诉你真相

---

"""

    with open(f"{OUTPUT_DIR}/hot_topics.md", "w", encoding="utf-8") as f:
        f.write(hot_topics_md)
    print(f"✅ 已生成: {OUTPUT_DIR}/hot_topics.md")

    # 5.2 SEO关键词 Markdown表格
    seo_keywords_md = f"""# SEO长尾词挖掘结果

> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> 总关键词数: {len(sorted_keywords)}
> 高分关键词(≥8分): {sum(1 for _, d in sorted_keywords if d['score'] >= 8)}

---

| 关键词 | 来源 | 意图标签 | 推荐指数 | 爆款标题建议 |
|--------|------|----------|----------|--------------|
"""
    for kw, data in sorted_keywords[:100]:
        seo_keywords_md += f"| {kw} | {data['source']} | {data['intent']} | {data['score']} | {data['catchy_title']} |\n"

    with open(f"{OUTPUT_DIR}/seo_keywords.md", "w", encoding="utf-8") as f:
        f.write(seo_keywords_md)
    print(f"✅ 已生成: {OUTPUT_DIR}/seo_keywords.md")

    # 5.3 SEO关键词 CSV
    with open(f"{OUTPUT_DIR}/seo_keywords.csv", "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["关键词", "来源", "意图标签", "推荐指数", "爆款标题建议"])
        for kw, data in sorted_keywords[:100]:
            writer.writerow([kw, data["source"], data["intent"], data["score"], data["catchy_title"]])
    print(f"✅ 已生成: {OUTPUT_DIR}/seo_keywords.csv")

    # 5.4 JSON格式（新增）
    json_output = {
        "generated_at": datetime.now().isoformat(),
        "total_keywords": len(sorted_keywords),
        "high_score_keywords": [
            {"keyword": kw, **data}
            for kw, data in sorted_keywords[:50]
        ],
        "hot_topics": sorted_topics[:10]
    }

    with open(f"{OUTPUT_DIR}/seo_keywords.json", "w", encoding="utf-8") as f:
        json.dump(json_output, f, ensure_ascii=False, indent=2)
    print(f"✅ 已生成: {OUTPUT_DIR}/seo_keywords.json")

    # 6. 保存历史数据
    save_history(all_keywords, hot_topics)

    # 7. 生成可视化图表
    try:
        from charts import KeywordVisualizer

        stats = {
            "total": len(sorted_keywords),
            "high_score": sum(1 for _, d in sorted_keywords if d['score'] >= 8),
            "avg_score": sum(d['score'] for _, d in sorted_keywords) / len(sorted_keywords)
        }

        visualizer = KeywordVisualizer(output_dir=f"{OUTPUT_DIR}/charts")
        charts = visualizer.generate_all_charts(sorted_keywords, stats)

    except ImportError as e:
        print(f"\n⚠️  可视化模块导入失败: {e}")
        print("💡 如需生成图表，请运行: pip install matplotlib seaborn wordcloud")
    except Exception as e:
        print(f"\n⚠️  图表生成失败: {e}")

    # 8. 打印预览
    elapsed = time.time() - start_time
    print("\n\n" + "=" * 70)
    print("🎉 数据挖掘完成！")
    print("=" * 70)
    print(f"⏱️  耗时: {elapsed:.1f}秒")
    print(f"📊 关键词总数: {len(sorted_keywords)}")
    print(f"🔥 高分关键词(≥8分): {sum(1 for _, d in sorted_keywords if d['score'] >= 8)}")

    print("\n📈 热点选题 TOP10:")
    print("-" * 70)
    for i, topic in enumerate(sorted_topics[:10], 1):
        print(f"{i:2d}. {topic['title'][:60]}")

    print("\n\n📈 SEO关键词 TOP30:")
    print("-" * 70)
    print(f"{'排名':<4} {'关键词':<28} {'分数':<4} {'意图':<12}")
    print("-" * 70)
    for i, (kw, data) in enumerate(sorted_keywords[:30], 1):
        print(f"{i:<4} {kw[:26]:<28} {data['score']:<4} {data['intent']:<12}")

    print(f"\n\n💾 输出文件位于 {OUTPUT_DIR}/ 目录")
    print("-" * 70)


if __name__ == "__main__":
    main()
