"""Tavily 搜索工具"""
import logging
import requests
from typing import Dict, Any
from strands import tool
from src.config import TAVILY_API_KEY, TAVILY_API_URL, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


def _format_search_results(query: str, data: Dict[str, Any]) -> str:
    """格式化搜索结果为可读文本"""
    results_text = f"搜索查询: {query}\n\n"
    
    if data.get("answer"):
        results_text += f"答案摘要:\n{data['answer']}\n\n"
    
    results_text += "搜索结果:\n"
    for i, result in enumerate(data.get("results", []), 1):
        results_text += f"\n{i}. {result.get('title', '无标题')}\n"
        results_text += f"   URL: {result.get('url', '')}\n"
        results_text += f"   内容: {result.get('content', '')}\n"
    
    return results_text


@tool
def tavily_search(query: str, max_results: int = 5) -> Dict[str, Any]:
    """使用 Tavily API 搜索网络信息
    
    Args:
        query: 搜索查询关键词
        max_results: 返回的最大结果数量，默认为5
    
    Returns:
        包含搜索结果的字典
    """
    if not TAVILY_API_KEY:
        logger.error("TAVILY_API_KEY not configured")
        return {
            "status": "error",
            "content": [{"text": "错误：未设置 TAVILY_API_KEY 环境变量"}]
        }
    
    try:
        response = requests.post(
            TAVILY_API_URL,
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "max_results": max_results,
                "include_answer": True,
                "include_raw_content": False
            },
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        
        data = response.json()
        results_text = _format_search_results(query, data)
        
        return {
            "status": "success",
            "content": [
                {"text": results_text},
                {"json": data}
            ]
        }
        
    except requests.exceptions.Timeout:
        logger.error(f"Tavily search timeout for query: {query}")
        return {
            "status": "error",
            "content": [{"text": "搜索请求超时，请稍后重试"}]
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Tavily search request failed: {e}")
        return {
            "status": "error",
            "content": [{"text": f"搜索请求失败: {str(e)}"}]
        }
    except Exception as e:
        logger.exception(f"Unexpected error in tavily_search: {e}")
        return {
            "status": "error",
            "content": [{"text": f"发生错误: {str(e)}"}]
        }
