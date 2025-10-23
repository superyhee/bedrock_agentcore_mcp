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
- 15+ pre-built conversation scenarios

Available Scenarios (16 total):

Basic Scenario (1):
1. 基础场景 - Basic user info and personalized recommendations

🚗 Smart Cockpit Scenarios (15) - Optimized for In-Car Use:
2. 智能导航 - Smart navigation with real-time routing (P0)
3. 沿途服务 - En-route services (restaurants, gas stations) (P1)
4. 停车场景 - Parking lot search and navigation (P1)
5. 自驾游 - Road trip planning (P2)
6. 接送人 - Airport/station pickup scenarios (P2)
7. 充电加油 - Refueling and EV charging (P1)
8. 实时路况 - Real-time traffic and route optimization (P0)
9. 语音控制 - Voice command interactions (P2)
10. 多目的地 - Multi-destination route planning (P2)
11. 天气路况 - Weather-aware driving (P3)
12. 车辆维护 - Vehicle maintenance and service (P3)
13. 新手司机 - Novice driver assistance (P3)
14. 商务出行 - Business trip efficiency (P3)
15. 家庭出游 - Family-friendly routes (P3)
16. 夜间驾驶 - Safe night driving (P3)

Usage:
    # Run with scenario selection
    python clients/boto3_client.py
    
    # Run with custom question
    python clients/boto3_client.py "你的问题"
"""
import boto3
import json

# Initialize the bedrock-agentcore client
agent_core_client = boto3.client('bedrock-agentcore', region_name='us-west-2')

# Example questions to test - 多场景对话测试集
test_questions = [
    
    # 场景1: 用户信息收集 + 个性化推荐
    "我家的地址是:北京海淀区上地十街10号，我的办公室在:北京朝阳区人寿保险大厦，我的爱好是出门赏花，我喜欢吃海鲜",
    "我住在北京海淀区附近，我想早上8点出门，中午顺路找个地方吃饭，下午继续玩，帮我根据我的爱好规划一个一天游玩的规划",
    "帮我查看这条路线的目前的交通状况？",
    "查询amazon最新的股价是多少"
]

# ========== 智能座舱专属场景 ==========

# 场景16: 智能导航场景（车载核心）
smart_navigation_scenario = [
    "从我的住址导航到我的办公室",
    "前方路况怎么样？",
    "有没有更快的路线避开拥堵？",
    "预计什么时候到达？",
    "途中帮我找个加油站",
    "最近的加油站在哪里？",
    "导航过去"
]

# 场景17: 沿途服务场景（车载高频）
enroute_service_scenario = [
    "我准备从我家去首都机场",
    "路上想吃点东西，推荐顺路的餐厅",
    "那家店有停车位吗？",
    "停车方便吗？",
    "现在路况如何？"
]

# 场景18: 停车场景（车载刚需）
parking_scenario = [
    "我从我家去三里屯太古里购物",
    "那里有停车场吗？",
    "停车费怎么收？",
    "现在有空位吗？",
    "导航到停车场入口",
    "如果那里停满了，附近还有其他停车场吗？",
    "哪个更便宜？"
]

# 场景19: 自驾游场景（周末高频）
road_trip_scenario = [
    "这个周末想自驾去郊区玩，推荐一下北京周边的景点",
    "古北水镇怎么样？",
    "从市区开车过去要多久？",
    "路上有服务区吗？",
    "那边有什么好吃的？",
    "附近有住宿的地方吗？",
    "规划一个两天一夜的自驾路线"
]

# 场景20: 接送人场景（日常高频）
pickup_scenario = [
    "我要从我家去首都机场T3航站楼接人",
    "现在出发来得及吗？",
    "走哪条路最快？",
    "机场停车怎么收费？",
    "有免费等待时间吗？",
    "如果航班延误了，附近有什么地方可以等？",
    "返程的时候想顺路吃个饭，推荐一下"
]

# 场景21: 充电/加油场景（车辆服务）
refuel_scenario = [
    "油快没了，帮我找最近的加油站",
    "哪家油价便宜？",
    "导航到那个加油站",
    "还有多远？",
    "如果是电动车，附近有充电桩吗？",
    "充电桩现在有空位吗？",
    "充满电大概需要多久？"
]

# 场景22: 实时路况场景（车载核心）
traffic_scenario = [
    "查询一下前方路况",
    "有事故吗？",
    "拥堵严重吗？大概堵多久？",
    "推荐一条避开拥堵的路线",
    "新路线会多花多少时间？",
    "沿途有限行吗？",
    "今天我的车能进五环吗？"
]


# 场景24: 多目的地场景（复杂规划）
multi_destination_scenario = [
    "我今天要去三个地方：先去公司，然后去客户那里开会，最后去接孩子放学",
    "帮我规划一个最优路线",
    "第一站到第二站要多久？",
    "中午能在客户附近吃饭吗？推荐一下",
    "下午3点必须到学校，来得及吗？",
    "如果来不及，调整一下顺序",
    "全程需要多长时间？"
]

# 场景25: 天气路况场景（安全驾驶）
weather_driving_scenario = [
    "查一下今天的天气",
    "会下雨吗？",
    "雨天开车要注意什么？",
    "高速路况怎么样？",
    "有团雾预警吗？",
    "推荐一条更安全的路线",
    "预计什么时候天气转好？"
]

# 场景26: 车辆维护场景（售后服务）
vehicle_maintenance_scenario = [
    "我的车是特斯拉",
    "我的车该保养了，附近有4S店吗？",
    "哪家评价好？",
    "营业时间是什么？",
    "需要预约吗？",
    "导航过去",
    "保养大概需要多久？",
    "等待的时候附近有什么地方可以逛？"
]

# 场景27: 新手司机场景（辅助驾驶）
novice_driver_scenario = [
    "我是新手，想去颐和园，帮我规划一条简单好走的路线",
    "避开复杂路口和立交桥",
    "这条路线有几个红绿灯？",
    "有没有难走的地方？",
    "那里好停车吗？",
]

# 场景28: 商务出行场景（效率优先）
business_trip_scenario = [
    "我10点有个会议在国贸，现在在酒店",
    "最快多久能到？",
    "规划最快路线",
    "会迟到吗？",
    "如果打车呢？",
    "附近有地铁吗？哪个更快？",
]

# 场景29: 家庭出游场景（舒适优先）
family_trip_scenario = [
    "带着老人和孩子去动物园，帮我规划一条舒适的路线",
    "避开颠簸路段",
    "路上有休息区吗？",
    "那里有母婴室吗？",
    "停车场离入口近吗？",
    "园区里有轮椅租赁吗？",
    "玩完了推荐一个适合家庭聚餐的餐厅"
]

# 场景30: 夜间驾驶场景（安全场景）
night_driving_scenario = [
    "晚上要开车回家，从CBD到通州",
    "夜间这条路安全吗？",
    "路灯照明好吗？",
    "有没有更明亮的路线？",
    "途中有24小时便利店吗？",
    "如果困了，附近有安全的休息区吗？",
    "预计几点能到家？"
]

# 所有场景集合（只保留基础场景和智能座舱专属场景）
all_scenarios = {
    "基础场景": test_questions,
    # 智能座舱专属场景
    "🚗智能导航": smart_navigation_scenario,
    "🚗沿途服务": enroute_service_scenario,
    "🚗停车场景": parking_scenario,
    "🚗自驾游": road_trip_scenario,
    "🚗接送人": pickup_scenario,
    "🚗充电加油": refuel_scenario,
    "🚗实时路况": traffic_scenario,
    "🚗多目的地": multi_destination_scenario,
    "🚗天气路况": weather_driving_scenario,
    "🚗车辆维护": vehicle_maintenance_scenario,
    "🚗新手司机": novice_driver_scenario,
    "🚗商务出行": business_trip_scenario,
    "🚗家庭出游": family_trip_scenario,
    "🚗夜间驾驶": night_driving_scenario
}

# 智能座舱推荐场景（按优先级排序）
in_car_recommended_scenarios = [
    "🚗智能导航",    # P0 - 核心功能
    "🚗实时路况",    # P0 - 核心功能
    "🚗沿途服务",    # P1 - 高频场景
    "🚗停车场景",    # P1 - 刚需场景
    "🚗充电加油",    # P1 - 刚需场景
    "🚗接送人",      # P2 - 日常高频
    "🚗自驾游",      # P2 - 周末场景
    "🚗多目的地",    # P2 - 复杂规划
    "🚗语音控制",    # P2 - 交互方式
    "🚗天气路况",    # P3 - 安全辅助
    "🚗车辆维护",    # P3 - 售后服务
    "🚗商务出行",    # P3 - 商务场景
    "🚗家庭出游",    # P3 - 家庭场景
    "🚗新手司机",    # P3 - 辅助驾驶
    "🚗夜间驾驶",    # P3 - 夜间安全
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
        session_id = f"1111111111111111111111111111111111111"  # 41 characters
    
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
    
    # Generate a single session ID for all questions to maintain conversation context
    import uuid
    session_id = f"session_{uuid.uuid4().hex}"  # 41 characters
    
    print("AgentCore Baidu Map Agent - Boto3 Client (流式输出)")
    print("=" * 80)
    print(f"Runtime ARN: {agent_runtime_arn}")
    print(f"Session ID: {session_id}")
    print("=" * 80)
    print("\n注意: 此客户端使用流式输出，响应将实时显示")
    print("注意: 所有问题使用相同的 session ID 以保持对话上下文")
    print("=" * 80)
    
    # Display available scenarios
    print("\n🚗 智能座舱对话场景 (共16个场景):")
    print("=" * 80)
    
    # Separate basic and in-car scenarios
    basic_scenarios = {k: v for k, v in all_scenarios.items() if not k.startswith("🚗")}
    car_scenarios = {k: v for k, v in all_scenarios.items() if k.startswith("🚗")}
    
    print("\n基础场景:")
    print("-" * 80)
    for idx, scenario_name in enumerate(basic_scenarios.keys(), 1):
        scenario_questions = basic_scenarios[scenario_name]
        print(f"{idx:2d}. {scenario_name:12s} - {len(scenario_questions)} 个问题")
    
    print("\n🚗 智能座舱专属场景 (按优先级排序):")
    print("-" * 80)
    start_idx = len(basic_scenarios) + 1
    for idx, scenario_name in enumerate(car_scenarios.keys(), start_idx):
        scenario_questions = car_scenarios[scenario_name]
        priority = "P0" if scenario_name in ["🚗智能导航", "🚗实时路况"] else \
                   "P1" if scenario_name in ["🚗沿途服务", "🚗停车场景", "🚗充电加油"] else \
                   "P2" if scenario_name in ["🚗接送人", "🚗自驾游", "🚗多目的地", "🚗语音控制"] else "P3"
        print(f"{idx:2d}. {scenario_name:12s} - {len(scenario_questions)} 个问题 [{priority}]")
    
    print("=" * 80)
    print(f"{len(all_scenarios) + 1:2d}. 全部场景     - 运行所有场景 (基础 + 座舱)")
    print(f"{len(all_scenarios) + 2:2d}. 座舱模式     - 按优先级运行座舱场景 (推荐)")
    print("=" * 80)
    
    # Let user choose a scenario
    try:
        choice = input("\n请选择场景编号 (直接回车运行基础场景): ").strip()
        
        if not choice:
            # Default to basic scenario
            selected_scenario = "基础场景"
            questions = test_questions
        elif choice.isdigit():
            choice_num = int(choice)
            if choice_num == len(all_scenarios) + 1:
                # Run all scenarios
                print("\n将运行所有场景...")
                for scenario_name, questions in all_scenarios.items():
                    print(f"\n\n{'='*80}")
                    print(f"场景: {scenario_name}")
                    print(f"{'='*80}")
                    run_scenario(questions, agent_runtime_arn, session_id, scenario_name)
                    
                    if scenario_name != list(all_scenarios.keys())[-1]:
                        cont = input("\n继续下一个场景? (y/n): ").strip().lower()
                        if cont != 'y':
                            break
                print("\n\n所有场景测试完成!")
                return
            elif choice_num == len(all_scenarios) + 2:
                # Run in-car scenarios only
                print("\n🚗 智能座舱模式 - 运行推荐场景...")
                print("=" * 80)
                for scenario_name in in_car_recommended_scenarios:
                    if scenario_name in all_scenarios:
                        questions = all_scenarios[scenario_name]
                        print(f"\n\n{'='*80}")
                        print(f"🚗 场景: {scenario_name}")
                        print(f"{'='*80}")
                        run_scenario(questions, agent_runtime_arn, session_id, scenario_name)
                        
                        if scenario_name != in_car_recommended_scenarios[-1]:
                            cont = input("\n继续下一个场景? (y/n): ").strip().lower()
                            if cont != 'y':
                                break
                print("\n\n🚗 智能座舱场景测试完成!")
                return
            elif 1 <= choice_num <= len(all_scenarios):
                selected_scenario = list(all_scenarios.keys())[choice_num - 1]
                questions = all_scenarios[selected_scenario]
            else:
                print("无效的选择，使用基础场景")
                selected_scenario = "基础场景"
                questions = test_questions
        else:
            print("无效的输入，使用基础场景")
            selected_scenario = "基础场景"
            questions = test_questions
    except KeyboardInterrupt:
        print("\n\n用户取消")
        return
    
    print(f"\n\n{'='*80}")
    print(f"运行场景: {selected_scenario}")
    print(f"{'='*80}")
    
    run_scenario(questions, agent_runtime_arn, session_id, selected_scenario)
    
    print("\n\n场景测试完成!")


def run_scenario(questions, agent_runtime_arn, session_id, scenario_name):
    """
    Run a specific scenario with a list of questions
    
    Args:
        questions: List of questions to ask
        agent_runtime_arn: ARN of the deployed AgentCore runtime
        session_id: Session ID for conversation context
        scenario_name: Name of the scenario for display
    """
    for i, question in enumerate(questions, 1):
        print(f"\n\n[{scenario_name}] 问题 {i}/{len(questions)}")
        invoke_agent(
            prompt=question,
            agent_runtime_arn=agent_runtime_arn,
            session_id=session_id,
            streaming=True
        )
        
        # Optional: pause between requests
        if i < len(questions):
            try:
                input("\n按 Enter 继续下一个问题 (Ctrl+C 退出)...")
            except KeyboardInterrupt:
                print("\n\n用户中断场景")
                break


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
