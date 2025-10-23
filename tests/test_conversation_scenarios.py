"""
测试对话场景 - 演示 Agent 的上下文理解能力

这个测试文件展示了如何使用不同的对话场景来测试 Agent 的能力：
- 多轮对话上下文理解
- 指代消解（"那里"、"这个"、"刚才"等）
- 个性化推荐
- 路线规划和优化
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clients.boto3_client import invoke_agent, all_scenarios
import uuid


def test_scenario(scenario_name: str, agent_runtime_arn: str, auto_continue: bool = False):
    """
    测试单个场景
    
    Args:
        scenario_name: 场景名称
        agent_runtime_arn: AgentCore Runtime ARN
        auto_continue: 是否自动继续（不等待用户输入）
    """
    if scenario_name not in all_scenarios:
        print(f"错误: 场景 '{scenario_name}' 不存在")
        print(f"可用场景: {', '.join(all_scenarios.keys())}")
        return
    
    questions = all_scenarios[scenario_name]
    session_id = f"test_session_{uuid.uuid4().hex}"
    
    print(f"\n{'='*80}")
    print(f"测试场景: {scenario_name}")
    print(f"问题数量: {len(questions)}")
    print(f"Session ID: {session_id}")
    print(f"{'='*80}\n")
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'='*80}")
        print(f"问题 {i}/{len(questions)}: {question}")
        print(f"{'='*80}")
        
        response = invoke_agent(
            prompt=question,
            agent_runtime_arn=agent_runtime_arn,
            session_id=session_id,
            streaming=True
        )
        
        if i < len(questions) and not auto_continue:
            input("\n按 Enter 继续...")
    
    print(f"\n{'='*80}")
    print(f"场景 '{scenario_name}' 测试完成!")
    print(f"{'='*80}\n")


def test_context_understanding(agent_runtime_arn: str):
    """
    测试上下文理解能力
    
    这个测试专门验证 Agent 是否能理解：
    - 地点指代（"那里"、"这个地方"）
    - 时间指代（"刚才"、"之前"）
    - 事物指代（"它"、"这个"）
    """
    session_id = f"context_test_{uuid.uuid4().hex}"
    
    print("\n" + "="*80)
    print("上下文理解能力测试")
    print("="*80)
    
    # 测试用例：地点指代
    test_cases = [
        {
            "name": "地点指代测试",
            "questions": [
                "帮我搜索北京的景点",
                "那里的天气怎么样？",  # "那里" 应该指代 "北京"
                "从上海到那个城市怎么走？"  # "那个城市" 应该指代 "北京"
            ]
        },
        {
            "name": "路线指代测试",
            "questions": [
                "从天安门到故宫怎么走？",
                "这条路线需要多长时间？",  # "这条路线" 指代上一个问题的路线
                "有更快的方式吗？"  # 继续讨论同一路线
            ]
        },
        {
            "name": "事物指代测试",
            "questions": [
                "搜索一下 AWS Lambda 的信息",
                "它支持哪些编程语言？",  # "它" 指代 "AWS Lambda"
                "价格怎么样？"  # 继续讨论 Lambda
            ]
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*80}")
        print(f"测试: {test_case['name']}")
        print(f"{'='*80}")
        
        for i, question in enumerate(test_case['questions'], 1):
            print(f"\n问题 {i}: {question}")
            print("-"*80)
            
            invoke_agent(
                prompt=question,
                agent_runtime_arn=agent_runtime_arn,
                session_id=session_id,
                streaming=True
            )
            
            if i < len(test_case['questions']):
                input("\n按 Enter 继续...")
        
        print(f"\n{test_case['name']} 完成!\n")


def test_personalization(agent_runtime_arn: str):
    """
    测试个性化推荐能力
    
    验证 Agent 是否能记住用户偏好并提供个性化建议
    """
    session_id = f"personalization_test_{uuid.uuid4().hex}"
    
    print("\n" + "="*80)
    print("个性化推荐测试")
    print("="*80)
    
    questions = [
        "我喜欢吃辣的，不喜欢甜食",
        "我住在北京朝阳区",
        "我的预算是人均100元左右",
        "根据我的喜好，推荐几家餐厅",  # 应该考虑：辣的、朝阳区、100元预算
        "如果我想吃火锅呢？",  # 应该继续考虑用户偏好
        "那家店从我家怎么去？"  # 应该记得用户住在朝阳区
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n问题 {i}/{len(questions)}: {question}")
        print("-"*80)
        
        invoke_agent(
            prompt=question,
            agent_runtime_arn=agent_runtime_arn,
            session_id=session_id,
            streaming=True
        )
        
        if i < len(questions):
            input("\n按 Enter 继续...")
    
    print("\n个性化推荐测试完成!\n")


def run_all_tests(agent_runtime_arn: str):
    """运行所有测试"""
    print("\n" + "="*80)
    print("开始运行所有对话场景测试")
    print("="*80)
    
    # 1. 测试上下文理解
    test_context_understanding(agent_runtime_arn)
    
    input("\n按 Enter 继续个性化测试...")
    
    # 2. 测试个性化推荐
    test_personalization(agent_runtime_arn)
    
    input("\n按 Enter 继续场景测试...")
    
    # 3. 测试几个关键智能座舱场景
    key_scenarios = ["🚗智能导航", "🚗实时路况", "🚗停车场景"]
    
    for scenario_name in key_scenarios:
        test_scenario(scenario_name, agent_runtime_arn, auto_continue=False)
        
        if scenario_name != key_scenarios[-1]:
            cont = input("\n继续下一个场景? (y/n): ").strip().lower()
            if cont != 'y':
                break
    
    print("\n" + "="*80)
    print("所有测试完成!")
    print("="*80)


def main():
    """主函数"""
    # TODO: 替换为你的 AgentCore Runtime ARN
    agent_runtime_arn = 'arn:aws:bedrock-agentcore:us-west-2:741040131740:runtime/agentcore_baidu_map_agent-JWw0Aw8Cn1'
    
    if len(sys.argv) > 1:
        # 测试指定场景
        scenario_name = sys.argv[1]
        test_scenario(scenario_name, agent_runtime_arn)
    else:
        # 显示菜单
        print("\n对话场景测试工具")
        print("="*80)
        print("1. 测试上下文理解能力")
        print("2. 测试个性化推荐能力")
        print("3. 测试单个场景")
        print("4. 运行所有测试")
        print("="*80)
        
        choice = input("\n请选择 (1-4): ").strip()
        
        if choice == "1":
            test_context_understanding(agent_runtime_arn)
        elif choice == "2":
            test_personalization(agent_runtime_arn)
        elif choice == "3":
            print("\n可用场景:")
            for i, name in enumerate(all_scenarios.keys(), 1):
                print(f"{i}. {name}")
            
            scenario_choice = input("\n选择场景编号: ").strip()
            if scenario_choice.isdigit():
                idx = int(scenario_choice) - 1
                scenario_names = list(all_scenarios.keys())
                if 0 <= idx < len(scenario_names):
                    test_scenario(scenario_names[idx], agent_runtime_arn)
                else:
                    print("无效的选择")
            else:
                print("无效的输入")
        elif choice == "4":
            run_all_tests(agent_runtime_arn)
        else:
            print("无效的选择")


if __name__ == "__main__":
    main()
