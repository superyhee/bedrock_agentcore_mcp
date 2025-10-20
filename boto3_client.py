"""
Boto3 client for calling deployed AgentCore Baidu Map Agent with streaming support

This client demonstrates how to invoke AgentCore Runtime agents with streaming responses.
The streaming approach delivers chunks of data in real-time as the agent processes requests,
providing immediate feedback rather than waiting for the complete response.

Features:
- Streaming response support (text/event-stream)
- Standard JSON response support
- Session management for conversation context
- Real-time output display
"""
import boto3
import json

# Initialize the bedrock-agentcore client
agent_core_client = boto3.client('bedrock-agentcore', region_name='us-west-2')

# Example questions to test
test_questions = [
     "制定自驾从成都到西安的路线",
    "帮我搜索上海外滩附近的餐厅",
    "深圳市南山区科技园的位置信息",
    "广州塔的地理坐标",
    "查找杭州西湖周边的景点"
]

def invoke_agent(prompt: str, agent_runtime_arn: str, session_id: str = None, streaming: bool = True):
    """
    Invoke the AgentCore runtime with a prompt
    
    Args:
        prompt: User question/prompt
        agent_runtime_arn: ARN of the deployed AgentCore runtime
        session_id: Optional session ID (must be 33+ chars if provided)
        streaming: Whether to use streaming output (default: True)
    
    Returns:
        Agent response data (for non-streaming) or None (for streaming)
    """
    # Generate a default session ID if not provided
    if session_id is None:
        import uuid
        session_id = f"session_{uuid.uuid4().hex}"  # 41 characters
    
    # Prepare the payload
    # AgentCore expects the payload format to match the entrypoint function signature
    payload = json.dumps({
        "prompt": prompt
    }).encode()
    
    print(f"\n{'='*60}")
    print(f"Question: {prompt}")
    print(f"{'='*60}")
    
    try:
        # Invoke the agent
        response = agent_core_client.invoke_agent_runtime(
            agentRuntimeArn=agent_runtime_arn,
            runtimeSessionId=session_id,
            payload=payload,
            qualifier="DEFAULT"
        )
        
        # Check content type and handle accordingly
        content_type = response.get("contentType", "")
        
        if "text/event-stream" in content_type:
            # Handle streaming response
            print("\n流式响应:")
            print("-" * 60)
            accumulated_text = []
            
            for line in response["response"].iter_lines(chunk_size=10):
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        data_str = line[6:]  # Remove "data: " prefix
                        
                        try:
                            data = json.loads(data_str)
                            
                            # 只提取和显示 contentBlockDelta 中的文本
                            if isinstance(data, dict):
                                if 'event' in data and 'contentBlockDelta' in data['event']:
                                    delta = data['event']['contentBlockDelta'].get('delta', {})
                                    if 'text' in delta:
                                        text_chunk = delta['text']
                                        # 实时打印文本块
                                        print(text_chunk, end='', flush=True)
                                        accumulated_text.append(text_chunk)
                                elif 'error' in data:
                                    print(f"\n错误: {data['error']}", flush=True)
                        except json.JSONDecodeError:
                            # 如果不是 JSON，跳过
                            pass
            
            print("\n" + "=" * 60)
            full_response = "".join(accumulated_text)
            print(f"完整响应 ({len(accumulated_text)} 个文本块):")
            print(full_response)
            return full_response
            
        elif content_type == "application/json":
            # Handle standard JSON response
            content = []
            for chunk in response.get("response", []):
                content.append(chunk.decode('utf-8'))
            
            response_data = json.loads(''.join(content))
            print("Agent Response:", json.dumps(response_data, indent=2, ensure_ascii=False))
            return response_data
        
        else:
            # Handle other content types
            response_body = response['response'].read()
            print("Raw Response:", response_body.decode('utf-8'))
            return response_body.decode('utf-8')
        
    except Exception as e:
        print(f"Error invoking agent: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """
    Main function to test the AgentCore Baidu Map Agent with streaming output
    """
    # TODO: Replace with your actual AgentCore runtime ARN
    # You can get this ARN after deploying with: agentcore deploy
    agent_runtime_arn = 'arn:aws:bedrock-agentcore:us-west-2:741040131740:runtime/agentcore_baidu_map_agent-JWw0Aw8Cn1'
    
    print("AgentCore Baidu Map Agent - Boto3 Client (流式输出)")
    print("=" * 60)
    print(f"Runtime ARN: {agent_runtime_arn}")
    print("=" * 60)
    print("\n注意: 此客户端使用流式输出，响应将实时显示")
    print("=" * 60)
    
    # Test with example questions
    for i, question in enumerate(test_questions, 1):
        print(f"\n\nTest {i}/{len(test_questions)}")
        invoke_agent(
            prompt=question,
            agent_runtime_arn=agent_runtime_arn,
            streaming=True  # Enable streaming output
        )
        
        # Optional: pause between requests
        if i < len(test_questions):
            input("\nPress Enter to continue to next question...")
    
    print("\n\nAll tests completed!")


if __name__ == "__main__":
    # You can also test with a single custom question
    import sys
    
    if len(sys.argv) > 1:
        # Custom question from command line
        custom_question = " ".join(sys.argv[1:])
        agent_runtime_arn = 'arn:aws:bedrock-agentcore:us-west-2:741040131740:runtime/agentcore_baidu_map_agent-JWw0Aw8Cn1'
        invoke_agent(custom_question, agent_runtime_arn, streaming=True)
    else:
        # Run all test questions
        main()
