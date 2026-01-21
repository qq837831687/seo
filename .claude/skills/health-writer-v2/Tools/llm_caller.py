#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Caller - 统一的 LLM 调用接口
支持多种 LLM API：OpenAI, Claude, Ollama, 国内API等

Version: 1.0
Created: 2026-01-20
"""

import json
import os
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
import requests


@dataclass
class LLMConfig:
    """LLM 配置"""
    provider: str  # openai, claude, ollama, qianwen, etc.
    api_key: str
    base_url: Optional[str] = None
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 60


class LLMCaller:
    """
    统一的 LLM 调用类
    支持多种 LLM Provider
    """

    def __init__(self, config: Optional[LLMConfig] = None):
        """
        初始化 LLM Caller

        Args:
            config: LLM 配置，如果为 None 则从环境变量或配置文件加载
        """
        if config is None:
            config = self._load_config_from_env()

        self.config = config
        self.provider = config.provider.lower()

    def _load_config_from_env(self) -> LLMConfig:
        """从环境变量加载配置"""
        provider = os.getenv("LLM_PROVIDER", "openai")
        api_key = os.getenv("LLM_API_KEY", "")

        if not api_key:
            raise ValueError(
                "LLM_API_KEY not found in environment variables. "
                "Please set LLM_API_KEY or provide config."
            )

        return LLMConfig(
            provider=provider,
            api_key=api_key,
            base_url=os.getenv("LLM_BASE_URL"),
            model=os.getenv("LLM_MODEL", self._get_default_model(provider)),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2000")),
            timeout=int(os.getenv("LLM_TIMEOUT", "60")),
        )

    def _get_default_model(self, provider: str) -> str:
        """获取默认模型"""
        defaults = {
            "openai": "gpt-3.5-turbo",
            "claude": "claude-3-sonnet-20240229",
            "ollama": "llama2",
            "qianwen": "qwen-turbo",
        }
        return defaults.get(provider, "gpt-3.5-turbo")

    def call(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: Optional[str] = "json",  # json, text
        **kwargs
    ) -> Union[str, Dict]:
        """
        调用 LLM

        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）
            response_format: 响应格式（json 或 text）
            **kwargs: 额外参数（覆盖 config）

        Returns:
            LLM 的响应（根据 response_format 返回字符串或字典）
        """
        # 合并配置
        config = self.config
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)

        # 根据不同的 provider 调用不同的实现
        if self.provider == "openai":
            return self._call_openai(prompt, system_prompt, response_format, config)
        elif self.provider == "claude":
            return self._call_claude(prompt, system_prompt, response_format, config)
        elif self.provider == "ollama":
            return self._call_ollama(prompt, system_prompt, response_format, config)
        elif self.provider in ["qianwen", "dashscope", "alibaba"]:
            return self._call_qianwen(prompt, system_prompt, response_format, config)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _call_openai(
        self,
        prompt: str,
        system_prompt: Optional[str],
        response_format: str,
        config: LLMConfig
    ) -> Union[str, Dict]:
        """调用 OpenAI API"""
        import openai

        client = openai.OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=config.timeout,
        )

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # OpenAI 需要设置 response_format
        kwargs = {
            "model": config.model,
            "messages": messages,
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
        }

        # 如果需要 JSON 输出
        if response_format == "json":
            kwargs["response_format"] = {"type": "json_object"}

        response = client.chat.completions.create(**kwargs)

        content = response.choices[0].message.content

        if response_format == "json":
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # 如果解析失败，返回原始字符串
                return content
        else:
            return content

    def _call_claude(
        self,
        prompt: str,
        system_prompt: Optional[str],
        response_format: str,
        config: LLMConfig
    ) -> Union[str, Dict]:
        """调用 Claude API"""
        import anthropic

        client = anthropic.Anthropic(
            api_key=config.api_key,
            timeout=config.timeout,
        )

        messages = [{"role": "user", "content": prompt}]

        # 如果需要 JSON 输出，在提示词中说明
        if response_format == "json":
            if system_prompt:
                system_prompt += "\n\n请务必以 JSON 格式输出。"
            else:
                prompt += "\n\n请务必以 JSON 格式输出。"

        response = client.messages.create(
            model=config.model,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            system=system_prompt,
            messages=messages,
        )

        content = response.content[0].text

        if response_format == "json":
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return content
        else:
            return content

    def _call_ollama(
        self,
        prompt: str,
        system_prompt: Optional[str],
        response_format: str,
        config: LLMConfig
    ) -> Union[str, Dict]:
        """调用 Ollama (本地) API"""
        base_url = config.base_url or "http://localhost:11434"
        url = f"{base_url}/api/generate"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": config.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": config.temperature,
                "num_predict": config.max_tokens,
            }
        }

        response = requests.post(url, json=payload, timeout=config.timeout)
        response.raise_for_status()

        content = response.json().get("response", "")

        if response_format == "json":
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return content
        else:
            return content

    def _call_qianwen(
        self,
        prompt: str,
        system_prompt: Optional[str],
        response_format: str,
        config: LLMConfig
    ) -> Union[str, Dict]:
        """调用通义千问 API"""
        base_url = config.base_url or "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

        headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        }

        # 构建消息
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": config.model or "qwen-turbo",
            "input": {
                "messages": messages
            },
            "parameters": {
                "temperature": config.temperature,
                "max_tokens": config.max_tokens,
                "result_format": response_format.upper(),
            }
        }

        response = requests.post(base_url, json=payload, headers=headers, timeout=config.timeout)
        response.raise_for_status()

        result = response.json()

        # 通义千问的响应格式
        if result.get("output"):
            content = result["output"].get("text", "")
            if response_format == "json":
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return content
            else:
                return content
        else:
            raise ValueError(f"Unexpected response format: {result}")


# ============================================================================
# 便捷函数
# ============================================================================

def create_llm_caller(
    provider: str = "openai",
    api_key: Optional[str] = None,
    **kwargs
) -> LLMCaller:
    """
    创建 LLM Caller 的便捷函数

    Args:
        provider: LLM Provider (openai, claude, ollama, qianwen)
        api_key: API Key（如果为 None，从环境变量读取）
        **kwargs: 其他配置参数

    Returns:
        LLMCaller 实例
    """
    if api_key is None:
        api_key = os.getenv("LLM_API_KEY", "")

    if not api_key:
        raise ValueError("api_key must be provided or set LLM_API_KEY environment variable")

    config = LLMConfig(
        provider=provider,
        api_key=api_key,
        **kwargs
    )

    return LLMCaller(config)


# ============================================================================
# 主程序（用于测试）
# ============================================================================

def main():
    """测试 LLM Caller"""

    print("=" * 60)
    print("LLM Caller - 测试程序")
    print("=" * 60)

    # 检查环境变量
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        print("❌ 错误: 请设置 LLM_API_KEY 环境变量")
        print("\n示例:")
        print("export LLM_API_KEY='your-api-key'")
        print("export LLM_PROVIDER='openai'  # 或 claude, ollama, qianwen")
        return

    provider = os.getenv("LLM_PROVIDER", "openai")
    print(f"✅ 使用 Provider: {provider}")

    # 创建 caller
    try:
        caller = create_llm_caller(provider=provider)
        print(f"✅ LLM Caller 创建成功")
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        return

    # 测试调用
    print("\n📝 测试简单调用...")
    try:
        response = caller.call(
            prompt="你好，请用一句话介绍你自己。",
            response_format="text"
        )
        print(f"✅ 调用成功！")
        print(f"响应: {response}")
    except Exception as e:
        print(f"❌ 调用失败: {e}")

    # 测试 JSON 调用
    print("\n📝 测试 JSON 格式调用...")
    try:
        response = caller.call(
            prompt="请用 JSON 格式返回：{'name': '测试', 'age': 25}",
            response_format="json"
        )
        print(f"✅ 调用成功！")
        print(f"响应: {json.dumps(response, ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"❌ 调用失败: {e}")


if __name__ == "__main__":
    main()
