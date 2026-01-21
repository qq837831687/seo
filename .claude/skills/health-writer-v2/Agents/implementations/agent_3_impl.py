#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent 3: Topic Architect - 大纲设计
设计文章结构，规划内容块

Version: 1.0
Created: 2026-01-20
"""

import json
from typing import Dict, Optional, List
from datetime import datetime


class Agent3TopicArchitect:
    """Agent 3: 大纲设计师"""

    def __init__(self, llm_caller=None):
        self.agent_id = "Agent_3_TopicArchitect"
        self.agent_name = "大纲设计师"
        self.llm_caller = llm_caller

    def design_outline(
        self,
        topic: str,
        viral_analysis: Dict,
        previous_outline: Optional[Dict] = None,
        revision_suggestions: Optional[Dict] = None,
        mode: str = "standard"
    ) -> Dict:
        """
        设计文章大纲

        Args:
            topic: 话题
            viral_analysis: Agent 2 的爆款分析结果
            previous_outline: 之前的纲要（用于修改）
            revision_suggestions: 修改建议
            mode: 模式（standard/fast）

        Returns:
            文章大纲
        """
        if self.llm_caller is None:
            return self._get_mock_outline(topic, viral_analysis)

        # TODO: 实现真实 LLM 调用
        return self._get_mock_outline(topic, viral_analysis)

    def _get_mock_outline(self, topic: str, viral_analysis: Dict) -> Dict:
        """获取模拟的大纲"""
        return {
            "topic": topic,
            "article_type": "实用干货类",
            "target_length": 2000,

            "structure": {
                "type": "问题-分析-解决（SCQA）",
                "sections": [
                    {
                        "section_id": 1,
                        "title": "开场：场景化引入",
                        "purpose": "引发共鸣，建立连接",
                        "word_count": 300,
                        "key_elements": [
                            "朋友动态/真实故事",
                            "痛点提出",
                            "情感连接"
                        ],
                        "old_li_voice": "亲身经历 - '我那会儿在工厂当护工...'"
                    },
                    {
                        "section_id": 2,
                        "title": "问题分析：为什么大寒进补容易上火？",
                        "purpose": "科普知识，建立权威",
                        "word_count": 400,
                        "key_elements": [
                            "大寒特点（最冷+春前奏）",
                            "中医理论（寒主收引，肝气始动）",
                            "常见误区（大热进补）"
                        ],
                        "old_li_voice": "老师傅的话 + 中医解释"
                    },
                    {
                        "section_id": 3,
                        "title": "老李的3个饮食原则",
                        "purpose": "核心解决方案",
                        "word_count": 600,
                        "subsections": [
                            {
                                "title": "原则1：温补，不是热补",
                                "content": "鸡肉/鱼肉 vs 羊肉/狗肉",
                                "recipe": "山药莲子鸡汤"
                            },
                            {
                                "title": "原则2：补得进去，先得'通'",
                                "content": "萝卜/白菜/白扁豆",
                                "recipe": "萝卜排骨汤"
                            },
                            {
                                "title": "原则3：春天快来了，养肝为先",
                                "content": "绿色蔬菜+酸味适量",
                                "recipe": "清肝茶"
                            }
                        ],
                        "old_li_voice": "秀芳的妙招 + 老中医的话 + 老李体验"
                    },
                    {
                        "section_id": 4,
                        "title": "具体食谱（3个）",
                        "purpose": "可操作的价值",
                        "word_count": 500,
                        "recipes": [
                            {
                                "name": "白萝卜炖羊肉（不上火版）",
                                "ingredients": ["羊肉500g", "白萝卜1根", "生姜3片", "枸杞"],
                                "steps": ["焯水", "切块", "炖煮", "放枸杞"],
                                "tips": "萝卜别去皮，清热"
                            },
                            {
                                "name": "山药莲子鸡汤",
                                "ingredients": ["鸡肉500g", "山药1段", "莲子30颗", "红枣5颗"],
                                "steps": ["焯水", "切块", "炖2小时"],
                                "tips": "温和养脾，适合所有老人"
                            },
                            {
                                "name": "清肝茶（立春前）",
                                "ingredients": ["菊花5朵", "枸杞", "山楂2片", "决明子10g"],
                                "steps": ["开水冲泡", "焖10分钟"],
                                "tips": "清理肝火，为春天准备"
                            }
                        ],
                        "old_li_voice": "老李的亲身体验"
                    },
                    {
                        "section_id": 5,
                        "title": "给子女的3个提醒",
                        "purpose": "增强转发动机",
                        "word_count": 300,
                        "reminders": [
                            "早上别空腹喝大补汤",
                            "感冒了别进补",
                            "有慢性病咨询医生"
                        ],
                        "old_li_voice": "工友的故事 + 秀芳的提醒"
                    },
                    {
                        "section_id": 6,
                        "title": "结尾：情感升华",
                        "purpose": "情感共鸣，行动呼吁",
                        "word_count": 200,
                        "key_elements": [
                            "孝顺不是贵的，是合适的",
                            "给爸妈炖碗汤吧",
                            "转发给父母/朋友"
                        ],
                        "old_li_voice": "温暖的收尾"
                    }
                ]
            },

            "content_blocks": [
                {"block": "开场引入", "type": "情感共鸣", "tone": "温暖"},
                {"block": "问题分析", "type": "科普", "tone": "专业"},
                {"block": "3个原则", "type": "干货", "tone": "实用"},
                {"block": "食谱", "type": "教程", "tone": "详细"},
                {"block": "提醒", "type": "注意事项", "tone": "关切"},
                {"block": "结尾", "type": "升华", "tone": "温暖"}
            ],

            "emotional_arcs": {
                "opening": "担心/焦虑",
                "middle": "希望/安心",
                "closing": "温暖/行动"
            },

            "old_li_elements": {
                "opening_approach": "亲身经历 - '我那会儿在工厂当护工...'",
                "tone_notes": "真诚、实在、不说教",
                "memory_cards_to_use": ["工厂车间", "护工经历", "秀芳"],
                "forbidden_elements": ["营销话术", "夸张表达"]
            },

            "seo_suggestions": {
                "title_keywords": ["大寒", "进补", "不上火", "食谱"],
                "content_keywords": ["温补", "萝卜", "鸡汤", "山药"],
                "meta_description": "大寒进补怎么吃才不上火？老中医教我3招，给爸妈炖这碗汤，比买补品强百倍"
            },

            "_metadata": {
                "agent_id": self.agent_id,
                "timestamp": datetime.now().isoformat(),
                "note": "模拟数据"
            }
        }


def create_agent_3(llm_caller=None) -> Agent3TopicArchitect:
    """便捷函数：创建 Agent 3"""
    return Agent3TopicArchitect(llm_caller=llm_caller)


if __name__ == "__main__":
    # 测试
    agent = Agent3TopicArchitect()
    viral_analysis = {"topic": "大寒进补"}
    outline = agent.design_outline("大寒进补怎么吃才不上火", viral_analysis)
    print(json.dumps(outline, ensure_ascii=False, indent=2))
