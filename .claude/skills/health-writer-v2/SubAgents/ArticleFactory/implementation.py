#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ArticleFactory SubAgent - 文章工厂
一键协调多个 Agent，自动生成爆款养生文章

Version: 1.0
Created: 2026-01-20
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum
import time


# ============================================================================
# 枚举定义
# ============================================================================

class UCOSTate(Enum):
    """UCO 状态枚举"""
    INIT = "INIT"
    ANALYZING = "ANALYZING"
    ANALYZED = "ANALYZED"
    OUTLINING = "OUTLINING"
    OUTLINED = "OUTLINED"
    DRAFTING = "DRAFTING"
    DRAFTED = "DRAFTED"
    REVIEWING = "REVIEWING"
    REVIEWED = "REVIEWED"
    OPTIMIZING = "OPTIMIZING"
    OPTIMIZED = "OPTIMIZED"
    READY = "READY"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


class RoutingDecision(Enum):
    """路由决策枚举"""
    APPROVED = "APPROVED"
    REVISE_STRUCTURE = "REVISE_STRUCTURE"
    REVISE_CONTENT = "REVISE_CONTENT"
    ADJUST_TONE = "ADJUST_TONE"
    ESCALATE = "ESCALATE"


class UrgencyLevel(Enum):
    """紧急程度枚举"""
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    EMERGENCY = "EMERGENCY"


class QualityLevel(Enum):
    """质量等级枚举"""
    STANDARD = "STANDARD"
    HIGH = "HIGH"


class TopicSource(Enum):
    """话题来源枚举"""
    USER_MANUAL = "USER_MANUAL"
    CHRONOS_RECOMMENDATION = "CHRONOS_RECOMMENDATION"
    VIRAL_TRENDING = "VIRAL_TRENDING"
    EMERGENCY_EVENT = "EMERGENCY_EVENT"


# ============================================================================
# UCO 对象类
# ============================================================================

class UCO:
    """
    Unified Content Object - 统一内容对象
    跟踪文章从话题到发布的完整生命周期
    """

    def __init__(self, topic: str, topic_source: str):
        """初始化 UCO 对象"""
        self.uco_id = f"UCO_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.topic = topic
        self.topic_source = topic_source
        self.state = UCOSTate.INIT
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        # 内容数据
        self.data = {
            "topic": topic,
            "topic_source": topic_source,
            "viral_analysis": None,  # Agent 2 输出
            "outline": None,  # Agent 3 输出
            "draft": None,  # Agent 4 输出
            "review_report": None,  # Agent 5 输出
            "virality_assessment": None,  # Agent 6 输出
            "headlines": None,  # Agent 7 输出
        }

        # 元数据
        self.metadata = {
            "revision_count": 0,
            "agent_execution_log": [],
            "routing_decisions": [],
            "issues": [],
        }

    def update_state(self, new_state: UCOSTate):
        """更新 UCO 状态"""
        old_state = self.state
        self.state = new_state
        self.updated_at = datetime.now()

        self._log_action(
            action="state_change",
            details=f"{old_state.value} → {new_state.value}"
        )

    def _log_action(self, action: str, details: str = "", agent: str = ""):
        """记录操作日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details,
            "agent": agent,
        }
        self.metadata["agent_execution_log"].append(log_entry)

    def add_routing_decision(self, decision: RoutingDecision, reason: str, agent: str):
        """添加路由决策记录"""
        decision_entry = {
            "timestamp": datetime.now().isoformat(),
            "decision": decision.value,
            "reason": reason,
            "agent": agent,
        }
        self.metadata["routing_decisions"].append(decision_entry)

    def increment_revision(self):
        """增加修改计数"""
        self.metadata["revision_count"] += 1

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "uco_id": self.uco_id,
            "topic": self.topic,
            "topic_source": self.topic_source,
            "state": self.state.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "data": self.data,
            "metadata": self.metadata,
        }


# ============================================================================
# ArticleFactory 主类
# ============================================================================

class ArticleFactory:
    """
    文章工厂 - SubAgent
    协调 Agent 2-7，一键生成爆款文章
    """

    def __init__(self, config_path: Optional[str] = None):
        """初始化 ArticleFactory"""
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()

        # 统计数据
        self.stats = {
            "total_runs": 0,
            "successful_runs": 0,
            "failed_runs": 0,
            "average_duration": 0,
        }

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置文件"""
        default_config = {
            "timeouts": {
                "agent_2": 15,
                "agent_3": 20,
                "agent_4": 90,
                "agent_5": 45,
                "agent_6": 15,
                "agent_7": 20,
            },
            "revision_limits": {
                "standard": 3,
                "high_quality": 5,
                "emergency": 1,
            },
            "quality_thresholds": {
                "min_quality_score": 80,
                "min_virality_score": 30,
                "min_tone_compliance": 85,
            },
        }

        if config_path:
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"警告: 无法加载配置文件 {config_path}: {e}")

        return default_config

    def _setup_logging(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger("ArticleFactory")
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    # ========================================================================
    # 主入口
    # ========================================================================

    def generate_article(
        self,
        topic: str,
        topic_source: str = "USER_MANUAL",
        target_audience: Optional[Dict] = None,
        urgency: str = "NORMAL",
        quality_level: str = "STANDARD",
        custom_requirements: Optional[Dict] = None,
    ) -> Dict:
        """
        生成文章的主入口

        Args:
            topic: 话题
            topic_source: 话题来源
            target_audience: 目标受众
            urgency: 紧急程度 (NORMAL/HIGH/EMERGENCY)
            quality_level: 质量等级 (STANDARD/HIGH)
            custom_requirements: 自定义要求

        Returns:
            article_factory_result: 包含文章、质量指标、工作流报告的字典
        """

        # 1. 初始化
        self.logger.info(f"🏭 ArticleFactory 启动: {topic}")
        start_time = time.time()

        try:
            # 创建 UCO 对象
            uco = UCO(topic, topic_source)

            # 根据紧急程度选择工作流
            if urgency == UrgencyLevel.EMERGENCY.value:
                result = self._emergency_workflow(uco, target_audience, custom_requirements)
            else:
                result = self._standard_workflow(
                    uco,
                    target_audience,
                    urgency,
                    quality_level,
                    custom_requirements
                )

            # 计算总耗时
            duration = time.time() - start_time
            result["workflow_report"]["total_time"] = round(duration / 60, 1)  # 转换为分钟

            # 更新统计
            self.stats["total_runs"] += 1
            self.stats["successful_runs"] += 1
            self.stats["average_duration"] = (
                (self.stats["average_duration"] * (self.stats["total_runs"] - 1) + duration)
                / self.stats["total_runs"]
            )

            self.logger.info(f"✅ ArticleFactory 完成: {uco.uco_id}, 耗时: {result['workflow_report']['total_time']} 分钟")

            return result

        except Exception as e:
            self.logger.error(f"❌ ArticleFactory 失败: {e}")
            self.stats["total_runs"] += 1
            self.stats["failed_runs"] += 1

            return {
                "success": False,
                "error": str(e),
                "uco_id": uco.uco_id if 'uco' in locals() else None,
            }

    # ========================================================================
    # 工作流实现
    # ========================================================================

    def _standard_workflow(
        self,
        uco: UCO,
        target_audience: Optional[Dict],
        urgency: str,
        quality_level: str,
        custom_requirements: Optional[Dict],
    ) -> Dict:
        """标准工作流"""

        # 获取修改限制
        revision_limit = self.config["revision_limits"]["high_quality"] \
            if quality_level == QualityLevel.HIGH.value \
            else self.config["revision_limits"]["standard"]

        # --------------------------------------------------------------
        # 步骤 2: Agent 2 - 爆款分析
        # --------------------------------------------------------------
        self.logger.info("📊 步骤 2/7: Agent 2 - 爆款分析")
        uco.update_state(UCOSTate.ANALYZING)

        viral_analysis = self._call_agent_2(
            topic=uco.topic,
            target_audience=target_audience
        )
        uco.data["viral_analysis"] = viral_analysis
        uco.update_state(UCOSTate.ANALYZED)

        # --------------------------------------------------------------
        # 步骤 3: Agent 3 - 大纲设计
        # --------------------------------------------------------------
        self.logger.info("📋 步骤 3/7: Agent 3 - 大纲设计")
        uco.update_state(UCOSTate.OUTLINING)

        outline = self._call_agent_3(
            topic=uco.topic,
            viral_analysis=viral_analysis,
        )
        uco.data["outline"] = outline
        uco.update_state(UCOSTate.OUTLINED)

        # --------------------------------------------------------------
        # 步骤 4-5: 写作 + 审核循环（可能多轮）
        # --------------------------------------------------------------
        max_revisions = revision_limit
        current_revision = 0

        while current_revision < max_revisions:
            # 步骤 4: Agent 4 - 内容写作
            self.logger.info(f"✍️  步骤 4/7: Agent 4 - 内容写作 (第 {current_revision + 1} 轮)")
            uco.update_state(UCOSTate.DRAFTING)

            # 如果是修改轮次，传入之前的审核意见
            previous_review = uco.data.get("review_report") if current_revision > 0 else None

            draft = self._call_agent_4(
                topic=uco.topic,
                outline=outline,
                viral_analysis=viral_analysis,
                custom_requirements=custom_requirements,
                revision_suggestions=previous_review,
            )
            uco.data["draft"] = draft
            uco.update_state(UCOSTate.DRAFTED)

            # 步骤 5: Agent 5 - 质量审核
            self.logger.info(f"🔍 步骤 5/7: Agent 5 - 质量审核 (第 {current_revision + 1} 轮)")
            uco.update_state(UCOSTate.REVIEWING)

            review_report = self._call_agent_5(draft=draft)
            uco.data["review_report"] = review_report

            # 路由决策
            routing_decision = review_report.get("routing_decision", "APPROVED")
            uco.add_routing_decision(
                decision=RoutingDecision(routing_decision),
                reason=review_report.get("reason", ""),
                agent="Agent_5_ChiefReviewer"
            )

            if routing_decision == "APPROVED":
                uco.update_state(UCOSTate.REVIEWED)
                self.logger.info(f"✅ 审核通过！总轮次: {current_revision + 1}")
                break
            elif current_revision >= max_revisions - 1:
                # 达到修改上限，升级给用户
                self.logger.warning(f"⚠️  达到修改上限 ({max_revisions} 轮)，升级给用户")
                review_report["escalated"] = True
                uco.update_state(UCOSTate.REVIEWED)
                break
            else:
                # 需要修改，继续循环
                current_revision += 1
                uco.increment_revision()

                if routing_decision == "REVISE_STRUCTURE":
                    self.logger.info("🔄 需要修改大纲，返回 Agent 3")
                    outline = self._call_agent_3(
                        topic=uco.topic,
                        viral_analysis=viral_analysis,
                        previous_outline=outline,
                        revision_suggestions=review_report,
                    )
                    uco.data["outline"] = outline
                elif routing_decision in ["REVISE_CONTENT", "ADJUST_TONE"]:
                    self.logger.info("🔄 需要修改内容，继续下一轮")
                    # 直接进入下一轮写作
                else:
                    # ESCALATE 或其他决策
                    self.logger.warning(f"⚠️  路由决策: {routing_decision}，升级给用户")
                    review_report["escalated"] = True
                    uco.update_state(UCOSTate.REVIEWED)
                    break

        # --------------------------------------------------------------
        # 步骤 6: Agent 6 - 爆款预测
        # --------------------------------------------------------------
        self.logger.info("📈 步骤 6/7: Agent 6 - 爆款预测")
        uco.update_state(UCOSTate.OPTIMIZING)

        virality_assessment = self._call_agent_6(
            draft=uco.data["draft"],
            review_report=review_report,
        )
        uco.data["virality_assessment"] = virality_assessment
        uco.update_state(UCOSTate.OPTIMIZED)

        # 如果是高质量模式，检查是否需要优化
        if quality_level == QualityLevel.HIGH.value:
            virality_score = virality_assessment.get("overall_score", 0)
            if virality_score < self.config["quality_thresholds"]["min_virality_score"]:
                self.logger.info("🎯 高质量模式：爆款分数不足，进行优化")
                # 再次调用 Agent 4 优化
                optimized_draft = self._call_agent_4(
                    topic=uco.topic,
                    outline=outline,
                    viral_analysis=viral_analysis,
                    custom_requirements=custom_requirements,
                    optimization_suggestions=virality_assessment.get("optimization_suggestions"),
                )
                uco.data["draft"] = optimized_draft
                uco.increment_revision()

        # --------------------------------------------------------------
        # 步骤 7: Agent 7 - 标题生成
        # --------------------------------------------------------------
        self.logger.info("📰 步骤 7/7: Agent 7 - 标题生成")

        headlines = self._call_agent_7(
            draft=uco.data["draft"],
            target_audience=target_audience,
        )
        uco.data["headlines"] = headlines
        uco.update_state(UCOSTate.READY)

        # --------------------------------------------------------------
        # 组装结果
        # --------------------------------------------------------------
        return self._assemble_result(uco)

    def _emergency_workflow(
        self,
        uco: UCO,
        target_audience: Optional[Dict],
        custom_requirements: Optional[Dict],
    ) -> Dict:
        """应急工作流（快速模式）"""

        self.logger.info("🚨 应急模式启动")

        # 快速分析
        self.logger.info("⚡ 快速分析")
        uco.update_state(UCOSTate.ANALYZING)
        viral_analysis = self._call_agent_2(topic=uco.topic, mode="fast")
        uco.data["viral_analysis"] = viral_analysis
        uco.update_state(UCOSTate.ANALYZED)

        # 快速大纲
        self.logger.info("⚡ 快速大纲")
        uco.update_state(UCOSTate.OUTLINING)
        outline = self._call_agent_3(topic=uco.topic, viral_analysis=viral_analysis, mode="fast")
        uco.data["outline"] = outline
        uco.update_state(UCOSTate.OUTLINED)

        # 快速写作
        self.logger.info("⚡ 快速写作")
        uco.update_state(UCOSTate.DRAFTING)
        draft = self._call_agent_4(
            topic=uco.topic,
            outline=outline,
            viral_analysis=viral_analysis,
            custom_requirements=custom_requirements,
            mode="fast"
        )
        uco.data["draft"] = draft
        uco.update_state(UCOSTate.DRAFTED)

        # 快速审核（仅一轮）
        self.logger.info("⚡ 快速审核")
        uco.update_state(UCOSTate.REVIEWING)
        review_report = self._call_agent_5(draft=draft, mode="fast")
        uco.data["review_report"] = review_report
        uco.update_state(UCOSTate.REVIEWED)

        # 跳过爆款预测（应急内容通常有高爆款潜力）
        uco.update_state(UCOSTate.OPTIMIZED)

        # 快速标题
        self.logger.info("⚡ 快速标题")
        headlines = self._call_agent_7(
            draft=draft,
            target_audience=target_audience,
            mode="fast"
        )
        uco.data["headlines"] = headlines
        uco.update_state(UCOSTate.READY)

        return self._assemble_result(uco, mode="EMERGENCY")

    # ========================================================================
    # Agent 调用方法（模拟）
    # ========================================================================

    def _call_agent_2(
        self,
        topic: str,
        target_audience: Optional[Dict] = None,
        mode: str = "standard"
    ) -> Dict:
        """
        调用 Agent 2: 爆款分析

        实际实现时，这里应该调用真实的 Agent 2
        这里提供模拟返回数据
        """
        # TODO: 实际实现时调用真实的 Agent 2
        return {
            "viral_dna_card": {
                "topic": topic,
                "key_patterns": ["数字+痛点", "权威背书", "反常识"],
                "emotional_hooks": ["健康焦虑", "家庭责任", "衰老恐惧"],
            },
            "key_patterns": [
                "节气 + 食材 + 痛点",
                "老中医的经验",
                "90%的人不知道"
            ],
            "golden_sentences": [
                "立春后，地里韭菜绿了",
                "这可是春天养肝的第一菜",
            ],
            "keywords": [topic, "养生", "中医", "健康"],
        }

    def _call_agent_3(
        self,
        topic: str,
        viral_analysis: Dict,
        previous_outline: Optional[Dict] = None,
        revision_suggestions: Optional[Dict] = None,
        mode: str = "standard"
    ) -> Dict:
        """调用 Agent 3: 大纲设计"""
        # TODO: 实际实现时调用真实的 Agent 3
        return {
            "title": f"{topic} - 文章大纲",
            "structure": {
                "opening": "场景引入 + 痛点共鸣",
                "body": [
                    "问题分析（中医理论）",
                    "老李故事（亲身经历）",
                    "实用方法（3-5条）",
                    "饮食建议（具体食谱）",
                ],
                "closing": "总结 + 行动呼吁"
            },
            "content_blocks": [
                {"section": "引入", "word_count": 300},
                {"section": "分析", "word_count": 500},
                {"section": "方法", "word_count": 800},
                {"section": "食谱", "word_count": 400},
                {"section": "总结", "word_count": 200},
            ],
            "emotional_arcs": ["焦虑", "共鸣", "希望", "行动"],
        }

    def _call_agent_4(
        self,
        topic: str,
        outline: Dict,
        viral_analysis: Dict,
        custom_requirements: Optional[Dict] = None,
        revision_suggestions: Optional[Dict] = None,
        optimization_suggestions: Optional[Dict] = None,
        mode: str = "standard"
    ) -> Dict:
        """调用 Agent 4: 内容写作"""
        # TODO: 实际实现时调用真实的 Agent 4
        return {
            "title": f"{topic} - 完整文章",
            "content": f"这里是{topic}的完整文章内容...\n\n" * 20,
            "word_count": 2400,
            "sources": ["《随息居饮食谱》", "《医学衷中参西录》"],
            "old_li_voice": [
                "立春了，该'咬春'了",
                "我这老寒腿开始预报天气了"
            ],
        }

    def _call_agent_5(
        self,
        draft: Dict,
        mode: str = "standard"
    ) -> Dict:
        """调用 Agent 5: 质量审核"""
        # TODO: 实际实现时调用真实的 Agent 5
        # 模拟通过
        return {
            "routing_decision": "APPROVED",
            "reason": "质量符合标准",
            "quality_score": 88,
            "tone_compliance": 92,
            "issues": [],
            "suggestions": [],
        }

    def _call_agent_6(
        self,
        draft: Dict,
        review_report: Dict
    ) -> Dict:
        """调用 Agent 6: 爆款预测"""
        # TODO: 实际实现时调用真实的 Agent 6
        return {
            "virality_assessment": {
                "emotion": 8,
                "practicality": 9,
                "social_currency": 7,
                "novelty": 7,
                "timeliness": 9,
            },
            "overall_score": 40,
            "prediction": "HIGH_POTENTIAL",
            "optimization_suggestions": [
                "增加紧迫感",
                "强化社交货币属性"
            ],
        }

    def _call_agent_7(
        self,
        draft: Dict,
        target_audience: Optional[Dict] = None,
        mode: str = "standard"
    ) -> Dict:
        """调用 Agent 7: 标题生成"""
        # TODO: 实际实现时调用真实的 Agent 7
        return {
            "generated": [
                f"{draft['title']} - 标题1",
                f"{draft['title']} - 标题2",
                f"{draft['title']} - 标题3",
            ],
            "selected": [
                {"title": "立春养肝第一菜，90%的人都吃错了", "ctr_prediction": 12.3},
                {"title": "老中医的养肝方，比吃药还管用", "ctr_prediction": 11.8},
                {"title": "春天别再吃这些了，伤肝又伤脾", "ctr_prediction": 10.9},
            ],
            "total_generated": 12,
        }

    # ========================================================================
    # 结果组装
    # ========================================================================

    def _assemble_result(self, uco: UCO, mode: str = "STANDARD") -> Dict:
        """组装最终结果"""
        draft = uco.data.get("draft", {})
        headlines = uco.data.get("headlines", {})
        virality_assessment = uco.data.get("virality_assessment", {})
        review_report = uco.data.get("review_report", {})

        # 选择最佳标题
        best_title = headlines.get("selected", [{}])[0].get("title", draft.get("title", ""))

        return {
            "success": True,
            "uco_id": uco.uco_id,
            "status": uco.state.value,

            "article": {
                "title": best_title,
                "titles_generated": headlines.get("selected", []),
                "outline": uco.data.get("outline", {}),
                "content": draft.get("content", ""),
                "word_count": draft.get("word_count", 0),
                "tags": draft.get("keywords", []),
            },

            "quality_metrics": {
                "virality_score": virality_assessment.get("overall_score", 0),
                "virality_prediction": virality_assessment.get("prediction", "UNKNOWN"),
                "quality_score": review_report.get("quality_score", 0),
                "revision_count": uco.metadata.get("revision_count", 0),
            },

            "workflow_report": {
                "total_time": 0,  # 会在外层设置
                "mode": mode,
                "agent_execution_log": uco.metadata.get("agent_execution_log", []),
                "routing_decisions": uco.metadata.get("routing_decisions", []),
                "issues_and_resolutions": uco.metadata.get("issues", []),
            },

            "old_li_compliance": {
                "tone_score": review_report.get("tone_compliance", 0),
                "voice_samples": draft.get("old_li_voice", []),
                "memory_cards_used": [],  # TODO: 从 Agent 4 获取
            },

            "next_actions": [
                "review_and_edit",
                "regenerate_titles",
                "adjust_content",
                "approve_and_publish",
            ],

            # 完整 UCO 对象（供调试使用）
            "_uco_debug": uco.to_dict(),
        }

    # ========================================================================
    # 工具方法
    # ========================================================================

    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.stats.copy()

    def reset_stats(self):
        """重置统计"""
        self.stats = {
            "total_runs": 0,
            "successful_runs": 0,
            "failed_runs": 0,
            "average_duration": 0,
        }


# ============================================================================
# 主程序入口
# ============================================================================

def main():
    """主程序入口（用于测试）"""

    print("=" * 60)
    print("ArticleFactory SubAgent - 文章工厂")
    print("=" * 60)

    # 创建 ArticleFactory 实例
    factory = ArticleFactory()

    # 示例 1: 标准文章生成
    print("\n📝 示例 1: 标准文章生成")
    print("-" * 60)

    result = factory.generate_article(
        topic="立春养肝",
        topic_source="CHRONOS_RECOMMENDATION",
        target_audience={
            "age_group": "60-70",
            "gender": "all",
        },
        urgency="NORMAL",
        quality_level="STANDARD",
    )

    if result["success"]:
        print(f"✅ 成功生成文章！")
        print(f"   UCO ID: {result['uco_id']}")
        print(f"   标题: {result['article']['title']}")
        print(f"   字数: {result['article']['word_count']}")
        print(f"   耗时: {result['workflow_report']['total_time']} 分钟")
        print(f"   爆款分数: {result['quality_metrics']['virality_score']}/50")
        print(f"   质量分数: {result['quality_metrics']['quality_score']}/100")
        print(f"   修改轮次: {result['quality_metrics']['revision_count']}")
    else:
        print(f"❌ 生成失败: {result['error']}")

    # 示例 2: 应急模式
    print("\n🚨 示例 2: 应急模式")
    print("-" * 60)

    result2 = factory.generate_article(
        topic="高温防暑",
        topic_source="EMERGENCY_EVENT",
        urgency="EMERGENCY",
    )

    if result2["success"]:
        print(f"✅ 应急文章生成成功！")
        print(f"   UCO ID: {result2['uco_id']}")
        print(f"   模式: {result2['workflow_report']['mode']}")
        print(f"   耗时: {result2['workflow_report']['total_time']} 分钟")
    else:
        print(f"❌ 生成失败: {result2['error']}")

    # 显示统计
    print("\n📊 统计信息")
    print("-" * 60)
    stats = factory.get_stats()
    print(f"   总运行次数: {stats['total_runs']}")
    print(f"   成功次数: {stats['successful_runs']}")
    print(f"   失败次数: {stats['failed_runs']}")
    print(f"   平均耗时: {stats['average_duration']:.1f} 秒")


if __name__ == "__main__":
    main()
