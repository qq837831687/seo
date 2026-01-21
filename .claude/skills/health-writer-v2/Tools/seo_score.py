#!/usr/bin/env python3
"""
SEO 评分工具
"""

import re
import sys
from typing import Dict, List

class SEOScorer:
    def __init__(self):
        self.score_weights = {
            'title_quality': 0.25,
            'keyword_density': 0.20,
            'readability': 0.20,
            'structure': 0.15,
            'length': 0.10,
            'meta': 0.10
        }

    def score_article(self, content: str, title: str, keywords: List[str]) -> Dict:
        """综合评分"""
        scores = {}

        # 1. 标题质量
        scores['title_quality'] = self.score_title(title)

        # 2. 关键词密度
        scores['keyword_density'] = self.score_keywords(content, keywords)

        # 3. 可读性
        scores['readability'] = self.score_readability(content)

        # 4. 结构
        scores['structure'] = self.score_structure(content)

        # 5. 长度
        scores['length'] = self.score_length(content)

        # 6. 元数据
        scores['meta'] = self.score_meta(content, keywords)

        # 计算总分
        total_score = sum(
            scores[key] * self.score_weights[key]
            for key in scores
        )

        return {
            'total_score': round(total_score, 1),
            'breakdown': scores,
            'recommendations': self.get_recommendations(scores)
        }

    def score_title(self, title: str) -> float:
        """评分标题质量 (0-100)"""
        score = 60  # 基础分

        # 有数字
        if re.search(r'\d+', title):
            score += 10

        # 有痛点词
        pain_points = ['不知道', '别再', '警惕', '注意', '误区']
        if any(word in title for word in pain_points):
            score += 10

        # 有权威词
        authority = ['营养师', '中医', '老中医', '专家', '医生', '研究']
        if any(word in title for word in authority):
            score += 10

        # 长度适中 (15-25字)
        if 15 <= len(title) <= 25:
            score += 10
        elif len(title) > 25:
            score -= 5

        return min(score, 100)

    def score_keywords(self, content: str, keywords: List[str]) -> float:
        """评分关键词布局 (0-100)"""
        if not keywords:
            return 70  # 无关键词，给中等分

        score = 0

        # 检查主关键词出现次数
        main_keyword = keywords[0]
        keyword_count = content.count(main_keyword)
        content_length = len(content)

        # 密度 2-3%
        density = (keyword_count * len(main_keyword)) / content_length * 100
        if 2 <= density <= 3:
            score += 40
        elif 1.5 <= density < 2 or 3 < density <= 4:
            score += 30
        elif density < 1.5:
            score += 20
        else:  # density > 4 (堆砌)
            score += 10

        # 检查长尾词
        for keyword in keywords[1:]:
            if keyword in content:
                score += 15

        # 首段有关键词
        first_paragraph = content.split('\n\n')[0]
        if main_keyword in first_paragraph:
            score += 15

        # 结尾有关键词
        last_paragraph = content.split('\n\n')[-1]
        if main_keyword in last_paragraph:
            score += 15

        return min(score, 100)

    def score_readability(self, content: str) -> float:
        """评分可读性 (0-100)"""
        score = 70  # 基础分

        # 段落长度 (不超过3行)
        paragraphs = content.split('\n\n')
        short_paragraphs = sum(1 for p in paragraphs if len(p.split('\n')) <= 3)
        if short_paragraphs / len(paragraphs) > 0.8:
            score += 15

        # 句子长度 (平均不超过20字)
        sentences = re.split(r'[。！？]', content)
        avg_length = sum(len(s) for s in sentences) / len(sentences)
        if avg_length <= 20:
            score += 15

        return min(score, 100)

    def score_structure(self, content: str) -> float:
        """评分结构 (0-100)"""
        score = 60  # 基础分

        # 有小标题
        headings = re.findall(r'^##\s+', content, re.MULTILINE)
        if len(headings) >= 3:
            score += 20

        # 有重点标注
        emphasis = re.findall(r'\*\*[^*]+\*\*', content)
        if len(emphasis) >= 5:
            score += 20

        return min(score, 100)

    def score_length(self, content: str) -> float:
        """评分长度 (0-100)"""
        word_count = len(content)

        if 1500 <= word_count <= 2000:
            return 100
        elif 1200 <= word_count < 1500 or 2000 < word_count <= 2500:
            return 80
        elif 1000 <= word_count < 1200 or 2500 < word_count <= 3000:
            return 60
        else:
            return 40

    def score_meta(self, content: str, keywords: List[str]) -> float:
        """评分元数据 (0-100)"""
        score = 0

        # 有免责声明
        if '免责声明' in content or '仅供参考' in content:
            score += 40

        # 有参考资料
        if '参考资料' in content or '来源' in content:
            score += 30

        # 有引导关注
        if '关注' in content or '在看' in content:
            score += 30

        return min(score, 100)

    def get_recommendations(self, scores: Dict) -> List[str]:
        """生成优化建议"""
        recommendations = []

        if scores['title_quality'] < 70:
            recommendations.append("标题优化：添加数字、痛点词或权威背书")

        if scores['keyword_density'] < 70:
            recommendations.append("关键词优化：确保主关键词出现在标题、首段和结尾")

        if scores['readability'] < 70:
            recommendations.append("可读性优化：缩短段落，控制在3行以内")

        if scores['structure'] < 70:
            recommendations.append("结构优化：增加小标题，重点内容加粗")

        if scores['length'] < 70:
            recommendations.append("长度优化：目标1500-2000字")

        if scores['meta'] < 70:
            recommendations.append("元数据优化：添加免责声明、参考资料、引导关注")

        return recommendations if recommendations else ["SEO 表现优秀！"]

def main():
    if len(sys.argv) < 3:
        print("Usage: python seo_score.py <article_file> <title> <keywords...>")
        sys.exit(1)

    file_path = sys.argv[1]
    title = sys.argv[2]
    keywords = sys.argv[3:] if len(sys.argv) > 3 else []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    scorer = SEOScorer()
    result = scorer.score_article(content, title, keywords)

    print(f"\n## 📊 SEO 评分报告\n")
    print(f"**总分**: {result['total_score']}/100\n")
    print("### 分项评分\n")
    for key, score in result['breakdown'].items():
        bar = '█' * int(score / 10)
        print(f"- {key}: {score}/100 {bar}\n")

    print("### 优化建议\n")
    for i, rec in enumerate(result['recommendations'], 1):
        print(f"{i}. {rec}\n")

if __name__ == "__main__":
    main()
