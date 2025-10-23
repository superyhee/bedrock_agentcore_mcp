"""百度地图 MCP 工具"""
import logging
from typing import Optional
from mcp.client.sse import sse_client
from strands.tools.mcp import MCPClient
from src.config import BAIDU_API_KEY

logger = logging.getLogger(__name__)


def initialize_baidu_mcp_client() -> Optional[MCPClient]:
    """初始化百度地图 MCP 客户端
    
    Returns:
        MCPClient 实例或 None（如果初始化失败）
    """
    if not BAIDU_API_KEY:
        logger.warning("BAIDU_MAPS_API_KEY not set, Baidu Maps features unavailable")
        return None
    
    try:
        baidu_map_sse_url = f"https://mcp.map.baidu.com/sse?ak={BAIDU_API_KEY}"
        return MCPClient(lambda: sse_client(baidu_map_sse_url))
    except Exception as e:
        logger.error(f"Failed to initialize Baidu MCP client: {e}")
        return None
