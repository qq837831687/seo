#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Agent 2 (爆款分析)
支持使用真实 LLM 或模拟数据

Usage:
    # 使用模拟数据（不需要 API Key）
    python test_agent_2.py

    # 使用真实 LLM（需要设置环境变量）
    export LLM_PROVIDER="openai"
    export LLM_API_KEY="your-api-key"
    python test_agent_2.py --use-llm
"""

import sys
import os
import json
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from Agents.implementations.agent_2_impl import Agent2DeconstructionAnalyst
from Tools.llm_caller import create_llm_caller


def test_with_mock():
    """使用模拟数据测试"""
    print("=" * 70)
    print("测试模式: 模拟数据（不需要 LLM API）")
    print("=" * 70)

    # 创建 Agent（不传入 llm_caller，使用模拟数据）
    agent = Agent2DeconstructionAnalyst(llm_caller=None)

    # 测试话题
    test_topic = "大寒进补怎么吃才不上火"

    print(f"\n📊 分析话题: {test_topic}")
    print("-" * 70)

    # 分析话题
    result = agent.analyze_topic(
        topic=test_topic,
        target_audience={"age_group": "45-60", "gender": "all"},
        topic_source="CHRONOS_RECOMMENDATION"
    )

    # 输出结果
    print("\n✅ 分析完成！\n")
    print("=" * 70)
    print("📊 爆款基因卡 (Viral DNA Card)")
    print("=" * 70)
    print(json.dumps(result['viral_dna_card'], ensure_ascii=False, indent=2))

    print("\n" + "=" * 70)
    print("🎯 成功模式 (Key Patterns)")
    print("=" * 70)
    print(json.dumps(result['key_patterns'], ensure_ascii=False, indent=2))

    print("\n" + "=" * 70)
    print("💝 情感钩子 (Emotional Hooks)")
    print("=" * 70)
    for hook in result['emotional_hooks']:
        print(f"  - {hook['type']}: {hook['content']} (效果: {hook['effectiveness']}/10)")

    print("\n" + "=" * 70)
    print("👥 受众画像 (Audience Persona)")
    print("=" * 70)
    print(json.dumps(result['audience_persona'], ensure_ascii=False, indent=2))

    print("\n" + "=" * 70)
    print("🔑 关键词 (Keywords)")
    print("=" * 70)
    print(json.dumps(result['keywords'], ensure_ascii=False, indent=2))

    print("\n" + "=" * 70)
    print("👴 老李人设适配 (Old Li Persona)")
    print("=" * 70)
    print(json.dumps(result['old_li_persona'], ensure_ascii=False, indent=2))

    print("\n" + "=" * 70)
    print("💎 金句 (Golden Sentences)")
    print("=" * 70)
    for i, sentence in enumerate(result['golden_sentences'], 1):
        print(f"  {i}. {sentence}")

    print("\n" + "=" * 70)
    print("📈 成功因素 (Success Factors)")
    print("=" * 70)
    factors = result['success_factors']
    print(f"  爆款潜力: {factors['overall_viral_potential']}/{factors['max_score']}")
    print(f"\n  优势:")
    for strength in factors.get('strengths', []):
        print(f"    ✅ {strength}")
    print(f"\n  劣势:")
    for weakness in factors.get('weaknesses', []):
        print(f"    ⚠️  {weakness}")
    print(f"\n  优化建议:")
    for suggestion in factors.get('optimization_suggestions', []):
        print(f"    💡 {suggestion}")

    return result


def test_with_llm():
    """使用真实 LLM 测试"""
    print("=" * 70)
    print("测试模式: 真实 LLM")
    print("=" * 70)

    # 检查环境变量
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        print("❌ 错误: 未设置 LLM_API_KEY 环境变量")
        print("\n请先设置:")
        print("  export LLM_PROVIDER='openai'  # 或 claude, ollama, qianwen")
        print("  export LLM_API_KEY='your-api-key'")
        print("\n或者使用 --mock 模式测试")
        return None

    provider = os.getenv("LLM_PROVIDER", "openai")
    print(f"✅ Provider: {provider}")
    print(f"✅ API Key: {api_key[:10]}...{api_key[-4:]}")

    # 创建 LLM Caller
    try:
        llm_caller = create_llm_caller(provider=provider)
        print("✅ LLM Caller 创建成功")
    except Exception as e:
        print(f"❌ LLM Caller 创建失败: {e}")
        return None

    # 创建 Agent
    agent = Agent2DeconstructionAnalyst(llm_caller=llm_caller)

    # 测试话题
    test_topic = "大寒进补怎么吃才不上火"

    print(f"\n📊 分析话题: {test_topic}")
    print("-" * 70)
    print("⏳ 正在调用 LLM，请稍候...")

    # 分析话题
    try:
        result = agent.analyze_topic(
            topic=test_topic,
            target_audience={"age_group": "45-60", "gender": "all"},
            topic_source="CHRONOS_RECOMMENDATION"
        )

        print("\n✅ LLM 调用成功！\n")

        # 保存完整结果到文件
        output_file = Path(__file__).parent / "agent_2_output.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"💾 完整结果已保存到: {output_file}")

        # 显示关键指标
        print("\n" + "=" * 70)
        print("📈 关键指标")
        print("=" * 70)
        viral = result.get('viral_dna_card', {})
        success = result.get('success_factors', {})
        print(f"  爆款潜力: {success.get('overall_viral_potential', 'N/A')}/{success.get('max_score', 50)}")
        print(f"  痛点紧迫性: {viral.get('pain_urgency', 'N/A')}/10")
        print(f"  情感强度: {viral.get('emotion_intensity', 'N/A')}/10")
        print(f"  社交价值: {viral.get('social_value', 'N/A')}/10")
        print(f"  时效性: {viral.get('timeliness_score', 'N/A')}/10")

        return result

    except Exception as e:
        print(f"\n❌ LLM 调用失败: {e}")
        print("\n尝试使用模拟数据...")
        return test_with_mock()


def main():
    """主程序"""
    import argparse

    parser = argparse.ArgumentParser(description="测试 Agent 2 (爆款分析)")
    parser.add_argument("--use-llm", action="store_true", help="使用真实 LLM（需要设置 API Key）")
    parser.add_argument("--mock", action="store_true", help="使用模拟数据（默认）")

    args = parser.parse_args()

    try:
        if args.use_llm:
            result = test_with_llm()
        else:
            result = test_with_mock()

        if result:
            print("\n" + "=" * 70)
            print("✅ 测试完成！")
            print("=" * 70)

    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
    except Exception as e:
        print(f"\n\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
