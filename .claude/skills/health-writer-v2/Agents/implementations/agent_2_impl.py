#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent 2: Deconstruction Analyst - 爆款分析（真实实现）
分析话题，提取爆款基因，为内容创作提供指导

Version: 1.0
Created: 2026-01-20
"""

import json
import os
from typing import Dict, Optional
from pathlib import Path


class Agent2DeconstructionAnalyst:
    """
    Agent 2: 爆款分析
    分析养生健康类话题的爆款潜力
    """

    def __init__(self, llm_caller=None):
        """
        初始化 Agent 2

        Args:
            llm_caller: LLMCaller 实例（如果为 None，会尝试创建）
        """
        self.agent_id = "Agent_2_DeconstructionAnalyst"
        self.agent_name = "爆款分析师"

        # 加载 Prompt 模板
        self.prompt_template = self._load_prompt_template()

        # LLM Caller
        self.llm_caller = llm_caller

    def _load_prompt_template(self) -> str:
        """加载 Prompt 模板"""
        prompt_file = Path(__file__).parent.parent / "Agent_2_Prompt.md"

        if prompt_file.exists():
            with open(prompt_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # 如果文件不存在，使用默认模板
            return self._get_default_prompt_template()

    def _get_default_prompt_template(self) -> str:
        """获取默认的 Prompt 模板"""
        return """你是养生健康领域的爆款内容分析师。

请分析以下话题，提取爆款基因。

**话题**：{topic}
**目标受众**：{target_audience}
**话题来源**：{topic_source}

请以 JSON 格式输出分析结果，包含：
- viral_dna_card: 爆款基因卡
- key_patterns: 成功模式
- emotional_hooks: 情感钩子
- audience_persona: 受众画像
- keywords: 关键词
- old_li_persona: 老李人设适配
- golden_sentences: 金句
- success_factors: 成功因素
"""

    def analyze_topic(
        self,
        topic: str,
        target_audience: Optional[Dict] = None,
        topic_source: str = "USER_MANUAL",
        mode: str = "standard"
    ) -> Dict:
        """
        分析话题的爆款潜力

        Args:
            topic: 待分析的话题
            target_audience: 目标受众 {"age_group": "60-70", "gender": "all"}
            topic_source: 话题来源
            mode: 模式（standard/fast - fast 模式简化分析）

        Returns:
            分析结果（字典格式）
        """
        if self.llm_caller is None:
            # 如果没有 LLM caller，返回模拟数据
            return self._get_mock_analysis(topic, target_audience)

        # 构建提示词
        prompt = self._build_prompt(topic, target_audience, topic_source)

        # 系统提示词
        system_prompt = """你是一位专业的养生健康内容分析师，擅长：
- 识别话题的爆款潜力
- 提取成功的内容模式
- 分析目标用户的心理需求
- 提炼情感共鸣点

请始终以 JSON 格式输出你的分析结果。
"""

        try:
            # 调用 LLM
            response = self.llm_caller.call(
                prompt=prompt,
                system_prompt=system_prompt,
                response_format="json"
            )

            # 验证响应格式
            if isinstance(response, dict):
                return self._validate_and_enrich(response, topic)
            else:
                # 如果返回的是字符串，尝试解析
                try:
                    parsed = json.loads(response)
                    return self._validate_and_enrich(parsed, topic)
                except json.JSONDecodeError:
                    print(f"⚠️  警告: LLM 返回的不是有效 JSON，使用模拟数据")
                    return self._get_mock_analysis(topic, target_audience)

        except Exception as e:
            print(f"❌ Agent 2 调用失败: {e}")
            print("📊 使用模拟数据")
            return self._get_mock_analysis(topic, target_audience)

    def _build_prompt(
        self,
        topic: str,
        target_audience: Optional[Dict],
        topic_source: str
    ) -> str:
        """构建提示词"""
        # 格式化目标受众
        audience_str = "未指定"
        if target_audience:
            audience_str = f"{target_audience.get('age_group', '全年龄')}岁，{target_audience.get('gender', '不限')}"

        # 填充模板
        prompt = self.prompt_template.format(
            topic=topic,
            target_audience=audience_str,
            topic_source=topic_source
        )

        return prompt

    def _validate_and_enrich(self, response: Dict, topic: str) -> Dict:
        """验证并丰富响应数据"""
        # 确保包含必需的字段
        required_fields = [
            "viral_dna_card",
            "key_patterns",
            "emotional_hooks",
            "audience_persona",
            "keywords",
            "old_li_persona",
            "golden_sentences",
            "success_factors"
        ]

        for field in required_fields:
            if field not in response:
                response[field] = self._get_default_field_value(field)

        # 添加元数据
        response["_metadata"] = {
            "agent_id": self.agent_id,
            "topic": topic,
            "timestamp": self._get_timestamp()
        }

        return response

    def _get_default_field_value(self, field: str) -> any:
        """获取字段的默认值"""
        defaults = {
            "viral_dna_card": {},
            "key_patterns": {"headline_patterns": [], "opening_patterns": []},
            "emotional_hooks": [],
            "audience_persona": {},
            "keywords": {},
            "old_li_persona": {},
            "golden_sentences": [],
            "success_factors": {"overall_viral_potential": 30}
        }
        return defaults.get(field, {})

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()

    def _get_mock_analysis(self, topic: str, target_audience: Optional[Dict]) -> Dict:
        """
        获取模拟的分析结果（用于测试或 LLM 不可用时）

        这个模拟数据基于我们之前手动分析的经验
        """
        return {
            "viral_dna_card": {
                "topic": topic,
                "pain_points": ["冬季进补上火", "不知道吃什么合适", "担心父母健康"],
                "pain_urgency": 8.5,
                "emotions": ["担心", "希望", "温暖"],
                "emotion_intensity": 9.0,
                "social_currency": "转发给父母，表达关心",
                "social_value": 8.5,
                "novelty": "大寒进补的误区和正确方法",
                "novelty_score": 7.0,
                "timeliness": "大寒时节，立春将至",
                "timeliness_score": 9.0
            },

            "key_patterns": {
                "headline_patterns": [
                    "[数字]种[功效]食材，[时间]必吃",
                    "老中医的[方/法]，比[对比对象]还管用",
                    "[时间]了，给爸妈炖这碗汤，比买补品强"
                ],
                "opening_patterns": [
                    "场景化引入：'昨天，朋友圈看到一个朋友...'",
                    "亲身经历：'我那会儿在工厂...'",
                    "问题引入：'很多人问我...'"
                ],
                "structure_patterns": [
                    "问题-分析-解决（SCQA）",
                    "清单式：引入→方法1→方法2→方法3→总结"
                ],
                "golden_sentence_patterns": [
                    "引用老中医的话",
                    "秀芳（老伴）的妙招",
                    "老李的亲身体验"
                ]
            },

            "emotional_hooks": [
                {
                    "type": "恐惧型",
                    "content": "大寒吃错，上火流鼻血",
                    "effectiveness": 8.5
                },
                {
                    "type": "希望型",
                    "content": "老中医教我3招，保了一冬的心脏",
                    "effectiveness": 9.0
                },
                {
                    "type": "温暖型",
                    "content": "给爸妈炖这碗汤，比买补品强百倍",
                    "effectiveness": 9.5
                },
                {
                    "type": "共鸣型",
                    "content": "你是不是也给爸妈买一堆补品，却不知道吃什么？",
                    "effectiveness": 8.0
                }
            ],

            "audience_persona": {
                "age_group": "45-60",
                "gender": "all",
                "role": "子女",
                "health_concerns": ["父母心血管", "父母关节", "冬季进补"],
                "psychological_needs": ["孝顺父母", "表达关心", "实用有效"],
                "cognitive_level": "高中到大学",
                "reading_scenarios": ["早上通勤", "午休时间", "睡前"],
                "sharing_motivation": "关心父母健康，帮助朋友"
            },

            "keywords": {
                "pain_points": ["进补上火", "不知道吃什么", "补品浪费"],
                "solutions": ["温补", "萝卜", "鸡汤", "山药"],
                "emotions": ["担心", "温暖", "孝顺"],
                "timeliness": ["大寒", "立春", "冬季"]
            },

            "old_li_persona": {
                "relevant_memory_cards": ["工厂车间", "护工经历", "秀芳"],
                "opening_approach": "亲身经历 - '我那会儿在工厂当护工，见过太多老人...'",
                "tone_notes": "真诚、实在、不说教",
                "forbidden_elements": ["营销话术", "夸张宣传", "虚假案例"],
                "voice_samples": [
                    "我那会儿在工厂，老师傅总说：'三九补一冬，来年无病痛。'",
                    "秀芳（我老伴）总唠叨：'萝卜汤，喝三天，肚子舒服。'",
                    "我在医院当护工那几年，见过太多老人，有的吃错了进医院，有的吃得简单，身体硬朗。"
                ]
            },

            "golden_sentences": [
                "老中医说：'顺天时而食，胜过吃药。'",
                "这碗汤，我给我爸连吃3次，他说：'身上暖和，不上火，这个对。'",
                "大寒了，给爸妈炖碗汤吧。或者，把这篇文章转给他们。",
                "最好的孝顺，不是买最贵的，而是给最合适的。"
            ],

            "success_factors": {
                "overall_viral_potential": 42,
                "max_score": 50,
                "strengths": [
                    "时效性强（大寒时节）",
                    "痛点准确（进补上火）",
                    "情感共鸣强（子女关心父母）",
                    "有实用价值（具体食谱）",
                    "符合老李人设（真实经历）"
                ],
                "weaknesses": [
                    "同类话题较多",
                    "需要差异化（老李独特视角）"
                ],
                "optimization_suggestions": [
                    "强化老李的独特经历（工厂+护工）",
                    "增加具体数据（连吃几次、效果如何）",
                    "突出子女陪伴心理（转发动机）",
                    "提供清晰的食谱和做法"
                ]
            },

            "_metadata": {
                "agent_id": "Agent_2_DeconstructionAnalyst",
                "topic": topic,
                "timestamp": self._get_timestamp(),
                "note": "模拟数据（LLM 不可用时使用）"
            }
        }


# ============================================================================
# 便捷函数
# ============================================================================

def analyze_topic(
    topic: str,
    llm_caller=None,
    target_audience: Optional[Dict] = None,
    topic_source: str = "USER_MANUAL"
) -> Dict:
    """
    分析话题的便捷函数

    Args:
        topic: 待分析的话题
        llm_caller: LLMCaller 实例
        target_audience: 目标受众
        topic_source: 话题来源

    Returns:
        分析结果
    """
    agent = Agent2DeconstructionAnalyst(llm_caller=llm_caller)
    return agent.analyze_topic(
        topic=topic,
        target_audience=target_audience,
        topic_source=topic_source
    )


# ============================================================================
# 主程序（用于测试）
# ============================================================================

def main():
    """测试 Agent 2"""

    print("=" * 60)
    print("Agent 2: 爆款分析师 - 测试程序")
    print("=" * 60)

    # 测试话题
    test_topic = "大寒进补怎么吃才不上火"

    print(f"\n📊 分析话题: {test_topic}")
    print("-" * 60)

    # 创建 Agent（不使用 LLM，使用模拟数据）
    agent = Agent2DeconstructionAnalyst(llm_caller=None)

    # 分析话题
    result = agent.analyze_topic(
        topic=test_topic,
        target_audience={"age_group": "45-60", "gender": "all"},
        topic_source="CHRONOS_RECOMMENDATION"
    )

    # 输出结果
    print("\n✅ 分析完成！\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 关键指标
    print("\n📈 关键指标:")
    print(f"  爆款潜力: {result['success_factors']['overall_viral_potential']}/50")
    print(f"  痛点紧迫性: {result['viral_dna_card']['pain_urgency']}/10")
    print(f"  情感强度: {result['viral_dna_card']['emotion_intensity']}/10")
    print(f"  社交价值: {result['viral_dna_card']['social_value']}/10")
    print(f"  时效性: {result['viral_dna_card']['timeliness_score']}/10")


if __name__ == "__main__":
    main()
