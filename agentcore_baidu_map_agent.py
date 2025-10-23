"""
向后兼容的入口文件
重定向到新的模块化结构
"""

# 导入所有必要的组件以保持向后兼容
from src.agent.main import app, invoke

# 如果直接运行此文件，启动 AgentCore Runtime
if __name__ == "__main__":
    app.run()
