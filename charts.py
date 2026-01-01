#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO关键词数据可视化模块
生成多种图表帮助分析关键词数据
"""

import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import pandas as pd
import numpy as np
from pathlib import Path
import json
from collections import Counter

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 设置配色方案
sns.set_palette("husl")
sns.set_style("whitegrid")


class KeywordVisualizer:
    """关键词数据可视化器"""

    def __init__(self, output_dir="output/charts"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_score_distribution(self, keywords_data):
        """生成关键词评分分布直方图"""
        scores = [data['score'] for _, data in keywords_data]

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # 直方图
        axes[0].hist(scores, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
        axes[0].set_xlabel('评分', fontsize=12)
        axes[0].set_ylabel('关键词数量', fontsize=12)
        axes[0].set_title('关键词评分分布', fontsize=14, fontweight='bold')
        axes[0].grid(axis='y', alpha=0.3)

        # 箱线图
        axes[1].boxplot(scores, vert=True, patch_artist=True,
                       boxprops=dict(facecolor='lightblue', alpha=0.7),
                       medianprops=dict(color='red', linewidth=2))
        axes[1].set_ylabel('评分', fontsize=12)
        axes[1].set_title('评分统计箱线图', fontsize=14, fontweight='bold')
        axes[1].grid(axis='y', alpha=0.3)

        # 添加统计信息
        mean_score = np.mean(scores)
        median_score = np.median(scores)
        axes[1].text(1.1, mean_score, f'平均: {mean_score:.1f}', fontsize=10)
        axes[1].text(1.1, median_score, f'中位数: {median_score:.1f}', fontsize=10)

        plt.tight_layout()
        output_path = self.output_dir / "score_distribution.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return output_path

    def generate_intent_pie(self, keywords_data):
        """生成意图标签饼图"""
        intents = []
        for _, data in keywords_data:
            intent = data['intent'].split('/')[0]  # 取第一个意图
            intents.append(intent if intent else '通用')

        intent_counts = Counter(intents)

        # 按数量排序
        sorted_intents = dict(sorted(intent_counts.items(), key=lambda x: x[1], reverse=True))

        fig, ax = plt.subplots(figsize=(10, 8))

        colors = sns.color_palette("Set3", len(sorted_intents))
        wedges, texts, autotexts = ax.pie(
            sorted_intents.values(),
            labels=sorted_intents.keys(),
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            textprops={'fontsize': 11}
        )

        # 美化文本
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')

        ax.set_title('关键词意图标签分布', fontsize=16, fontweight='bold', pad=20)

        # 添加图例
        ax.legend(wedges, [f'{k}: {v}' for k, v in sorted_intents.items()],
                 title="意图分类",
                 loc="center left",
                 bbox_to_anchor=(1, 0, 0.5, 1))

        plt.tight_layout()
        output_path = self.output_dir / "intent_distribution.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return output_path

    def generate_source_bar(self, keywords_data):
        """生成关键词来源分布条形图"""
        sources = []
        for _, data in keywords_data:
            source = data['source']
            sources.append(source)

        source_counts = Counter(sources)
        sorted_sources = dict(sorted(source_counts.items(), key=lambda x: x[1], reverse=True))

        fig, ax = plt.subplots(figsize=(10, 6))

        sources_list = list(sorted_sources.keys())
        counts_list = list(sorted_sources.values())

        colors = sns.color_palette("viridis", len(sources_list))
        bars = ax.barh(sources_list, counts_list, color=colors)

        # 添加数值标签
        for bar, count in zip(bars, counts_list):
            width = bar.get_width()
            ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                   f'{count}',
                   ha='left', va='center', fontsize=10, fontweight='bold')

        ax.set_xlabel('关键词数量', fontsize=12)
        ax.set_ylabel('数据源', fontsize=12)
        ax.set_title('各数据源关键词数量分布', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)

        plt.tight_layout()
        output_path = self.output_dir / "source_distribution.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return output_path

    def generate_top_keywords_bar(self, keywords_data, top_n=20):
        """生成TOP关键词条形图"""
        top_keywords = keywords_data[:top_n]

        keywords_list = [kw for kw, _ in top_keywords]
        scores_list = [data['score'] for _, data in top_keywords]

        fig, ax = plt.subplots(figsize=(12, 8))

        colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(keywords_list)))
        bars = ax.barh(range(len(keywords_list)), scores_list, color=colors)

        # 设置Y轴标签
        ax.set_yticks(range(len(keywords_list)))
        ax.set_yticklabels(keywords_list, fontsize=9)

        # 添加数值标签
        for i, (bar, score) in enumerate(zip(bars, scores_list)):
            width = bar.get_width()
            ax.text(width + 0.3, bar.get_y() + bar.get_height()/2,
                   f'{score}',
                   ha='left', va='center', fontsize=9, fontweight='bold')

        ax.set_xlabel('评分', fontsize=12)
        ax.set_title(f'TOP {top_n} 高分关键词', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)

        # 反转Y轴，让最高的在顶部
        ax.invert_yaxis()

        plt.tight_layout()
        output_path = self.output_dir / f"top_{top_n}_keywords.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return output_path

    def generate_wordcloud(self, keywords_data):
        """生成关键词词云"""
        # 根据评分权重生成词频
        word_freq = {}
        for kw, data in keywords_data:
            # 使用评分作为权重
            weight = data['score']
            word_freq[kw] = word_freq.get(kw, 0) + weight

        # 生成词云
        wordcloud = WordCloud(
            width=1600,
            height=800,
            background_color='white',
            colormap='viridis',
            max_words=200,
            relative_scaling=0.5,
            min_font_size=10
        ).generate_from_frequencies(word_freq)

        fig, ax = plt.subplots(figsize=(16, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('SEO关键词词云（字体大小=评分权重）', fontsize=16, fontweight='bold', pad=20)

        plt.tight_layout(pad=0)
        output_path = self.output_dir / "wordcloud.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.1)
        plt.close()

        return output_path

    def generate_trend_line(self, history_dir="history"):
        """生成历史趋势图"""
        history_files = sorted(Path(history_dir).glob("history_*.json"))

        if len(history_files) < 2:
            print("  ⚠️  历史数据不足，跳过趋势图")
            return None

        timestamps = []
        keyword_counts = []
        high_score_counts = []

        for hist_file in history_files:
            try:
                with open(hist_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    timestamps.append(data.get('datetime', '')[:10])  # 只取日期
                    keyword_counts.append(data.get('keywords_count', 0))
                    high_score_counts.append(0)  # 历史数据中未记录
            except:
                pass

        if not timestamps:
            return None

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(range(len(timestamps)), keyword_counts,
               marker='o', linewidth=2, markersize=8, label='关键词总数', color='steelblue')

        ax.set_xlabel('时间', fontsize=12)
        ax.set_ylabel('关键词数量', fontsize=12)
        ax.set_title('关键词数量历史趋势', fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(timestamps)))
        ax.set_xticklabels(timestamps, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        output_path = self.output_dir / "historical_trend.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return output_path

    def generate_summary_dashboard(self, keywords_data, stats):
        """生成数据概览仪表板"""
        fig = plt.figure(figsize=(16, 10))

        # 创建网格布局
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

        # 1. 关键词总数
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.text(0.5, 0.5, f'{stats["total"]}',
                ha='center', va='center', fontsize=48, fontweight='bold', color='steelblue')
        ax1.text(0.5, 0.2, '关键词总数', ha='center', va='center', fontsize=14)
        ax1.axis('off')

        # 2. 高分关键词数
        ax2 = fig.add_subplot(gs[0, 1])
        high_score = sum(1 for _, d in keywords_data if d['score'] >= 8)
        ax2.text(0.5, 0.5, f'{high_score}',
                ha='center', va='center', fontsize=48, fontweight='bold', color='coral')
        ax2.text(0.5, 0.2, '高分关键词(≥8)', ha='center', va='center', fontsize=14)
        ax2.axis('off')

        # 3. 平均评分
        ax3 = fig.add_subplot(gs[0, 2])
        avg_score = np.mean([d['score'] for _, d in keywords_data])
        ax3.text(0.5, 0.5, f'{avg_score:.1f}',
                ha='center', va='center', fontsize=48, fontweight='bold', color='green')
        ax3.text(0.5, 0.2, '平均评分', ha='center', va='center', fontsize=14)
        ax3.axis('off')

        # 4. 评分分布
        ax4 = fig.add_subplot(gs[1, :])
        scores = [data['score'] for _, data in keywords_data]
        ax4.hist(scores, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
        ax4.set_xlabel('评分', fontsize=11)
        ax4.set_ylabel('数量', fontsize=11)
        ax4.set_title('评分分布', fontsize=12, fontweight='bold')
        ax4.grid(axis='y', alpha=0.3)

        # 5. 意图分布饼图
        ax5 = fig.add_subplot(gs[2, 0])
        intents = [data['intent'].split('/')[0] for _, data in keywords_data]
        intent_counts = Counter(intents)
        ax5.pie(intent_counts.values(), labels=intent_counts.keys(), autopct='%1.1f%%',
                colors=sns.color_palette("Set3", len(intent_counts)))
        ax5.set_title('意图分布', fontsize=12, fontweight='bold')

        # 6. 数据源分布
        ax6 = fig.add_subplot(gs[2, 1])
        sources = [data['source'] for _, data in keywords_data]
        source_counts = Counter(sources)
        sorted_sources = dict(sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:5])
        ax6.barh(list(sorted_sources.keys()), list(sorted_sources.values()),
                color=sns.color_palette("viridis", len(sorted_sources)))
        ax6.set_xlabel('数量', fontsize=11)
        ax6.set_title('数据源分布', fontsize=12, fontweight='bold')
        ax6.invert_yaxis()

        # 7. TOP10关键词
        ax7 = fig.add_subplot(gs[2, 2])
        top10 = keywords_data[:10]
        keywords_list = [f"{kw[:10]}..." for kw, _ in top10]
        scores_list = [data['score'] for _, data in top10]
        ax7.barh(keywords_list, scores_list, color=plt.cm.RdYlGn_r(np.linspace(0.3, 0.7, 10)))
        ax7.set_xlabel('评分', fontsize=11)
        ax7.set_title('TOP10关键词', fontsize=12, fontweight='bold')
        ax7.invert_yaxis()

        fig.suptitle('SEO关键词数据概览仪表板', fontsize=18, fontweight='bold', y=0.98)

        plt.tight_layout()
        output_path = self.output_dir / "summary_dashboard.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return output_path

    def generate_all_charts(self, keywords_data, stats=None):
        """生成所有图表"""
        print("\n📊 生成数据可视化图表...")
        print("-" * 70)

        if stats is None:
            stats = {"total": len(keywords_data)}

        charts = []

        # 1. 评分分布
        try:
            path = self.generate_score_distribution(keywords_data)
            charts.append(("评分分布图", path))
            print(f"✅ 评分分布图: {path}")
        except Exception as e:
            print(f"⚠️  评分分布图生成失败: {e}")

        # 2. 意图分布饼图
        try:
            path = self.generate_intent_pie(keywords_data)
            charts.append(("意图分布饼图", path))
            print(f"✅ 意图分布饼图: {path}")
        except Exception as e:
            print(f"⚠️  意图分布饼图生成失败: {e}")

        # 3. 数据源分布
        try:
            path = self.generate_source_bar(keywords_data)
            charts.append(("数据源分布图", path))
            print(f"✅ 数据源分布图: {path}")
        except Exception as e:
            print(f"⚠️  数据源分布图生成失败: {e}")

        # 4. TOP20关键词
        try:
            path = self.generate_top_keywords_bar(keywords_data, top_n=20)
            charts.append(("TOP20关键词图", path))
            print(f"✅ TOP20关键词图: {path}")
        except Exception as e:
            print(f"⚠️  TOP20关键词图生成失败: {e}")

        # 5. 词云
        try:
            path = self.generate_wordcloud(keywords_data)
            charts.append(("词云图", path))
            print(f"✅ 词云图: {path}")
        except Exception as e:
            print(f"⚠️  词云图生成失败: {e}")

        # 6. 历史趋势
        try:
            path = self.generate_trend_line()
            if path:
                charts.append(("历史趋势图", path))
                print(f"✅ 历史趋势图: {path}")
        except Exception as e:
            print(f"⚠️  历史趋势图生成失败: {e}")

        # 7. 仪表板
        try:
            path = self.generate_summary_dashboard(keywords_data, stats)
            charts.append(("概览仪表板", path))
            print(f"✅ 概览仪表板: {path}")
        except Exception as e:
            print(f"⚠️  概览仪表板生成失败: {e}")

        print("-" * 70)
        print(f"✅ 共生成 {len(charts)} 个图表，保存在: {self.output_dir}/")

        return charts


if __name__ == "__main__":
    # 测试代码
    print("可视化模块测试...")
    print("请通过主脚本调用此模块")
