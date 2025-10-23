"""Memory 相关工具函数"""
import logging
from typing import Dict, Any, List
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig

logger = logging.getLogger(__name__)


def get_actor_and_session_id(context) -> tuple[str, str]:
    """从上下文中提取 actor_id 和 session_id
    
    Args:
        context: AgentCore 运行时上下文
    
    Returns:
        (actor_id, session_id) 元组
    """
    actor_id = 'user'
    if hasattr(context, 'headers'):
        actor_id = context.headers.get(
            'X-Amzn-Bedrock-AgentCore-Runtime-Custom-Actor-Id',
            'user'
        )
    
    session_id = getattr(context, 'session_id', 'default')
    return actor_id, session_id


def create_memory_config(memory_id: str, actor_id: str, session_id: str) -> AgentCoreMemoryConfig:
    """创建 Memory 配置
    
    Args:
        memory_id: Memory ID
        actor_id: 用户标识
        session_id: 会话标识
    
    Returns:
        AgentCoreMemoryConfig 实例
    """
    return AgentCoreMemoryConfig(
        memory_id=memory_id,
        session_id=session_id,
        actor_id=actor_id,
        retrieval_config={
            f"/users/{actor_id}/facts": RetrievalConfig(top_k=5, relevance_score=0.5),
            f"/users/{actor_id}/preferences": RetrievalConfig(top_k=3, relevance_score=0.5),
            f"/users/{actor_id}/locations": RetrievalConfig(top_k=5, relevance_score=0.5)
        }
    )


def build_context_aware_prompt(prompt: str, conversation_history: List[Dict[str, Any]]) -> str:
    """构建包含对话历史的上下文感知提示
    
    Args:
        prompt: 用户当前输入
        conversation_history: 最近的对话历史
    
    Returns:
        增强后的提示词
    """
    if not conversation_history:
        return prompt
    
    # 构建对话历史摘要
    history_text = "\n\n[对话历史]:\n"
    for i, turn in enumerate(conversation_history[-5:], 1):  # 只使用最近5轮对话
        role = turn.get('role', 'unknown')
        content = turn.get('content', '')
        history_text += f"{i}. {role}: {content[:200]}...\n" if len(content) > 200 else f"{i}. {role}: {content}\n"
    
    history_text += "\n[当前问题]:\n"
    
    return history_text + prompt


async def get_conversation_context(session_manager, max_turns: int = 10) -> List[Dict[str, Any]]:
    """获取对话历史上下文
    
    Args:
        session_manager: AgentCore Memory 会话管理器
        max_turns: 获取的最大对话轮数
    
    Returns:
        对话历史列表
    """
    try:
        # 获取最近的对话历史
        turns = session_manager.get_last_k_turns(k=max_turns)
        
        conversation_history = []
        for turn in turns:
            # 提取角色和内容
            role = turn.get('role', 'unknown')
            content = turn.get('content', '')
            
            if isinstance(content, list):
                # 如果内容是列表，提取文本
                text_content = ' '.join([
                    item.get('text', '') for item in content 
                    if isinstance(item, dict) and 'text' in item
                ])
                content = text_content
            
            conversation_history.append({
                'role': role,
                'content': content
            })
        
        logger.info(f"Retrieved {len(conversation_history)} conversation turns")
        return conversation_history
        
    except Exception as e:
        logger.warning(f"Failed to retrieve conversation history: {e}")
        return []
