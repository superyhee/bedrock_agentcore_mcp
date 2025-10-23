"""配置管理"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# AWS 配置
MEMORY_ID = os.getenv("BEDROCK_AGENTCORE_MEMORY_ID")
REGION = os.getenv("AWS_REGION", "us-west-2")
MODEL_ID = "global.anthropic.claude-haiku-4-5-20251001-v1"

# API Keys
BAIDU_API_KEY = os.getenv("BAIDU_MAPS_API_KEY","baidu-key")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY","tavily-key")

# API 配置
TAVILY_API_URL = "https://api.tavily.com/search"
REQUEST_TIMEOUT = 30
