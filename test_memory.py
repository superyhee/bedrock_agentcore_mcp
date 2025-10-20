"""
测试 AgentCore 短期记忆功能
演示 Agent 如何利用对话历史回答问题
"""

import asyncio
import json
from agentcore_baidu_map_agent import invoke


class MockContext:
    """模拟 AgentCore 上下文"""
    def __init__(self, session_id="test_session"):
        self.session_id = session_id
        self.headers = {
            'X-Amzn-Bedrock-AgentCore-Runtime-Custom-Actor-Id': 'test_user'
        }


async def test_conversation_memory():
    """测试对话记忆功能"""
    
    print("=" * 80)
    print("测试场景：多轮对话 - Agent 应该记住之前的对话内容")
    print("=" * 80)
    
    context = MockContext(session_id="memory_test_001")
    
    # 第一轮：询问北京的信息
    print("\n[第1轮] 用户: 帮我搜索一下北京的天气情况")
    print("-" * 80)
    
    payload1 = {
        "prompt": "帮我搜索一下北京的天气情况",
        "use_history": True
    }
    
    async for event in invoke(payload1, context):
        if "event" in event:
            content = event["event"].get("contentBlockDelta", {}).get("delta", {}).get("text", "")
            if content:
                print(content, end="", flush=True)
        elif "error" in event:
            print(f"\n错误: {event['error']}")
    
    print("\n")
    
    # 等待一下，让 Memory 有时间处理
    await asyncio.sleep(2)
    
    # 第二轮：使用指代词"那里"
    print("\n[第2轮] 用户: 那里有什么著名景点？")
    print("-" * 80)
    print("(Agent 应该理解'那里'指的是北京)")
    print("-" * 80)
    
    payload2 = {
        "prompt": "那里有什么著名景点？",
        "use_history": True
    }
    
    async for event in invoke(payload2, context):
        if "event" in event:
            content = event["event"].get("contentBlockDelta", {}).get("delta", {}).get("text", "")
            if content:
                print(content, end="", flush=True)
        elif "error" in event:
            print(f"\n错误: {event['error']}")
    
    print("\n")
    
    await asyncio.sleep(2)
    
    # 第三轮：继续使用上下文
    print("\n[第3轮] 用户: 从上海到刚才说的那个城市怎么走？")
    print("-" * 80)
    print("(Agent 应该理解'刚才说的那个城市'指的是北京)")
    print("-" * 80)
    
    payload3 = {
        "prompt": "从上海到刚才说的那个城市怎么走？",
        "use_history": True
    }
    
    async for event in invoke(payload3, context):
        if "event" in event:
            content = event["event"].get("contentBlockDelta", {}).get("delta", {}).get("text", "")
            if content:
                print(content, end="", flush=True)
        elif "error" in event:
            print(f"\n错误: {event['error']}")
    
    print("\n")
    print("=" * 80)
    print("测试完成！")
    print("=" * 80)


async def test_without_memory():
    """测试不使用记忆的情况（对比）"""
    
    print("\n\n")
    print("=" * 80)
    print("对比测试：不使用对话历史")
    print("=" * 80)
    
    context = MockContext(session_id="no_memory_test")
    
    print("\n[问题] 用户: 那里有什么著名景点？")
    print("-" * 80)
    print("(没有上下文，Agent 应该无法理解'那里')")
    print("-" * 80)
    
    payload = {
        "prompt": "那里有什么著名景点？",
        "use_history": False  # 禁用历史记忆
    }
    
    async for event in invoke(payload, context):
        if "event" in event:
            content = event["event"].get("contentBlockDelta", {}).get("delta", {}).get("text", "")
            if content:
                print(content, end="", flush=True)
        elif "error" in event:
            print(f"\n错误: {event['error']}")
    
    print("\n")
    print("=" * 80)


if __name__ == "__main__":
    print("\n🧠 AgentCore 短期记忆功能测试\n")
    
    # 运行测试
    asyncio.run(test_conversation_memory())
    
    # 对比测试
    asyncio.run(test_without_memory())
    
    print("\n✅ 所有测试完成！\n")
