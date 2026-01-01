#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版网络抓取模块
支持多种反爬策略：代理池、真实浏览器请求头、Cookie管理、智能重试
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
import random
from typing import List, Dict, Optional
from urllib.parse import quote, urlencode
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class EnhancedFetcher:
    """增强版网络抓取器"""

    # 真实浏览器请求头池
    HEADERS_POOL = [
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        },
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        },
        {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive"
        }
    ]

    def __init__(self, use_proxy=False, proxy_list=None):
        """
        初始化抓取器

        Args:
            use_proxy: 是否使用代理
            proxy_list: 代理列表 [{'http': '...', 'https': '...'}]
        """
        self.use_proxy = use_proxy
        self.proxy_list = proxy_list or []
        self.session = requests.Session()
        self.session.cookies = requests.cookies.RequestsCookieJar()

        # 配置重试策略
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _get_random_headers(self):
        """获取随机请求头"""
        headers = random.choice(self.HEADERS_POOL).copy()
        return headers

    def _get_proxy(self):
        """获取随机代理"""
        if not self.use_proxy or not self.proxy_list:
            return None
        return random.choice(self.proxy_list)

    def fetch(self, url: str, params: dict = None, method: str = "GET",
              timeout: int = 15, source_name: str = "") -> Optional[requests.Response]:
        """
        安全的HTTP请求

        Args:
            url: 请求URL
            params: 查询参数
            method: 请求方法 GET/POST
            timeout: 超时时间
            source_name: 数据源名称（用于日志）

        Returns:
            Response对象或None
        """
        headers = self._get_random_headers()
        proxies = self._get_proxy()

        # 随机延迟，避免请求过快
        delay = random.uniform(1.0, 3.0)
        time.sleep(delay)

        try:
            if method.upper() == "GET":
                response = self.session.get(
                    url,
                    params=params,
                    headers=headers,
                    proxies=proxies,
                    timeout=timeout
                )
            else:
                response = self.session.post(
                    url,
                    data=params,
                    headers=headers,
                    proxies=proxies,
                    timeout=timeout
                )

            if response.status_code == 200:
                logger.info(f"✅ {source_name}: 成功")
                return response
            else:
                logger.warning(f"⚠️  {source_name}: HTTP {response.status_code}")
                return None

        except requests.exceptions.Timeout:
            logger.warning(f"⚠️  {source_name}: 超时")
            return None
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠️  {source_name}: {type(e).__name__}")
            return None
        except Exception as e:
            logger.warning(f"⚠️  {source_name}: 未知错误 - {str(e)[:50]}")
            return None


class BaiduFetcher(EnhancedFetcher):
    """百度搜索建议抓取器"""

    def fetch_suggestions(self, keyword: str) -> List[str]:
        """
        抓取百度搜索建议

        Args:
            keyword: 关键词

        Returns:
            建议词列表
        """
        url = "http://suggestion.baidu.com/su"
        params = {"wd": keyword, "cb": "cb"}

        logger.info(f"  🔍 百度: {keyword}")
        response = self.fetch(url, params=params, source_name="百度下拉")

        if not response:
            return []

        try:
            # 百度返回的是GB2312编码的JSONP
            text = response.text
            match = re.search(r'cb\((.*)\)', text)
            if match:
                json_str = match.group(1)
                # 尝试解码GB2312
                try:
                    json_str = json_str.encode('latin1').decode('gb2312')
                except:
                    pass

                data = json.loads(json_str)
                if isinstance(data, dict) and "s" in data:
                    suggestions = data.get("s", [])
                    logger.info(f"  ✅ 百度: 获取 {len(suggestions)} 个建议词")
                    return suggestions
        except Exception as e:
            logger.warning(f"  ⚠️  百度解析失败: {e}")

        return []


class BilibiliFetcher(EnhancedFetcher):
    """B站搜索建议抓取器"""

    def fetch_suggestions(self, keyword: str) -> List[str]:
        """抓取B站搜索建议"""
        url = "https://s.search.bilibili.com/main/suggest"
        params = {"term": keyword}

        logger.info(f"  🔍 B站: {keyword}")
        response = self.fetch(url, params=params, source_name="B站建议")

        if not response:
            return []

        try:
            data = response.json()
            if isinstance(data, dict) and "result" in data:
                suggestions = [item.get("value", "") for item in data.get("result", []) if "value" in item]
                logger.info(f"  ✅ B站: 获取 {len(suggestions)} 个建议词")
                return suggestions
        except Exception as e:
            logger.warning(f"  ⚠️  B站解析失败: {e}")

        return []


class TaobaoFetcher(EnhancedFetcher):
    """淘宝搜索建议抓取器"""

    def fetch_suggestions(self, keyword: str) -> List[str]:
        """抓取淘宝搜索建议"""
        url = "https://suggest.taobao.com/sug"
        params = {"q": keyword, "code": "utf-8"}

        logger.info(f"  🔍 淘宝: {keyword}")
        response = self.fetch(url, params=params, source_name="淘宝建议")

        if not response:
            return []

        try:
            data = response.json()
            result = data.get("result", [])
            suggestions = []
            for item in result:
                if isinstance(item, list) and len(item) > 0:
                    suggestions.append(item[0])
            logger.info(f"  ✅ 淘宝: 获取 {len(suggestions)} 个建议词")
            return suggestions
        except Exception as e:
            logger.warning(f"  ⚠️  淘宝解析失败: {e}")

        return []


class ZhihuFetcher(EnhancedFetcher):
    """知乎热榜抓取器"""

    def fetch_hot_topics(self) -> List[str]:
        """抓取知乎热榜"""
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"

        logger.info(f"  🔍 知乎热榜")
        response = self.fetch(url, source_name="知乎热榜")

        if not response:
            return []

        try:
            data = response.json()
            items = data.get("data", [])
            topics = []
            for item in items[:50]:  # 取前50个
                target = item.get("target", {})
                title = target.get("title", "")
                if title:
                    topics.append(title)
            logger.info(f"  ✅ 知乎: 获取 {len(topics)} 个热榜话题")
            return topics
        except Exception as e:
            logger.warning(f"  ⚠️  知乎热榜解析失败: {e}")

        return []


class WeiboFetcher(EnhancedFetcher):
    """微博热搜抓取器（难度较高）"""

    def fetch_hot_topics(self) -> List[str]:
        """抓取微博热搜（需要登录态，成功率较低）"""
        url = "https://weibo.com/ajax/side/hotSearch"

        logger.info(f"  🔍 微博热搜")
        response = self.fetch(url, source_name="微博热搜")

        if not response:
            return []

        try:
            data = response.json()
            items = data.get("data", {}).get("realtime", [])
            topics = [item.get("word", "") for item in items]
            logger.info(f"  ✅ 微博: 获取 {len(topics)} 个热搜话题")
            return topics
        except Exception as e:
            logger.warning(f"  ⚠️  微博热搜解析失败: {e}")

        return []


class GoogleAutoCompleteFetcher(EnhancedFetcher):
    """Google自动补全抓取器（新增）"""

    def fetch_suggestions(self, keyword: str) -> List[str]:
        """抓取Google搜索建议"""
        url = "http://suggestqueries.google.com/complete/search"
        params = {
            "client": "youtube",
            "ds": "yt",
            "q": keyword,
            "output": "json"
        }

        logger.info(f"  🔍 Google: {keyword}")
        response = self.fetch(url, params=params, source_name="Google建议")

        if not response:
            return []

        try:
            text = response.text
            # Google返回的是JavaScript代码，需要解析
            match = re.search(r'\((.*)\)', text)
            if match:
                data = json.loads(match.group(1))
                suggestions = data[1] if len(data) > 1 else []
                logger.info(f"  ✅ Google: 获取 {len(suggestions)} 个建议词")
                return suggestions
        except Exception as e:
            logger.warning(f"  ⚠️  Google解析失败: {e}")

        return []


class BingAutoCompleteFetcher(EnhancedFetcher):
    """Bing自动补全抓取器（新增）"""

    def fetch_suggestions(self, keyword: str) -> List[str]:
        """抓取Bing搜索建议"""
        url = "http://api.bing.com/qsonhs.aspx"
        params = {
            "type": "cb",
            "q": keyword
        }

        logger.info(f"  🔍 Bing: {keyword}")
        response = self.fetch(url, params=params, source_name="Bing建议")

        if not response:
            return []

        try:
            text = response.text
            match = re.search(r'AS\.AddSugg\((.*)\)', text)
            if match:
                data = json.loads(match.group(1))
                if isinstance(data, dict) and "AS" in data:
                    results = data["AS"]["Results"]
                    suggestions = []
                    for result in results:
                        for suggestion in result.get("Suggs", []):
                            suggestions.append(suggestion.get("Txt", ""))
                    logger.info(f"  ✅ Bing: 获取 {len(suggestions)} 个建议词")
                    return suggestions
        except Exception as e:
            logger.warning(f"  ⚠️  Bing解析失败: {e}")

        return []


# 工厂函数
def create_fetcher(source: str, **kwargs) -> EnhancedFetcher:
    """
    创建抓取器实例

    Args:
        source: 数据源名称 (baidu/bilibili/taobao/zhihu/weibo/google/bing)
        **kwargs: 其他参数

    Returns:
        对应的抓取器实例
    """
    fetchers = {
        "baidu": BaiduFetcher,
        "bilibili": BilibiliFetcher,
        "taobao": TaobaoFetcher,
        "zhihu": ZhihuFetcher,
        "weibo": WeiboFetcher,
        "google": GoogleAutoCompleteFetcher,
        "bing": BingAutoCompleteFetcher
    }

    fetcher_class = fetchers.get(source.lower(), EnhancedFetcher)
    return fetcher_class(**kwargs)


if __name__ == "__main__":
    # 测试代码
    print("=" * 60)
    print("🌐 增强版网络抓取器测试")
    print("=" * 60)

    test_keyword = "养生"

    # 测试百度
    print(f"\n测试关键词: {test_keyword}")
    print("-" * 60)

    baidu_fetcher = create_fetcher("baidu")
    baidu_results = baidu_fetcher.fetch_suggestions(test_keyword)
    print(f"百度结果: {baidu_results[:5] if baidu_results else '无'}")

    # 测试B站
    bili_fetcher = create_fetcher("bilibili")
    bili_results = bili_fetcher.fetch_suggestions(test_keyword)
    print(f"B站结果: {bili_results[:5] if bili_results else '无'}")

    # 测试Google
    google_fetcher = create_fetcher("google")
    google_results = google_fetcher.fetch_suggestions(test_keyword)
    print(f"Google结果: {google_results[:5] if google_results else '无'}")

    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
