#!/usr/bin/env python3
"""
验证项目结构和模块导入
确保所有模块都能正确导入和使用
"""

import sys
import os

def test_imports():
    """测试所有模块导入"""
    print("=" * 60)
    print("验证项目结构和模块导入")
    print("=" * 60)
    
    tests = []
    
    # 测试配置模块
    print("\n1. 测试配置模块...")
    try:
        from src.config import MEMORY_ID, REGION, MODEL_ID, BAIDU_API_KEY, TAVILY_API_KEY
        print("   ✅ src.config 导入成功")
        tests.append(("配置模块", True))
    except Exception as e:
        print(f"   ❌ src.config 导入失败: {e}")
        tests.append(("配置模块", False))
    
    # 测试工具模块
    print("\n2. 测试工具模块...")
    try:
        from src.tools.baidu_maps import initialize_baidu_mcp_client
        print("   ✅ src.tools.baidu_maps 导入成功")
        tests.append(("百度地图工具", True))
    except Exception as e:
        print(f"   ❌ src.tools.baidu_maps 导入失败: {e}")
        tests.append(("百度地图工具", False))
    
    try:
        from src.tools.tavily_search import tavily_search
        print("   ✅ src.tools.tavily_search 导入成功")
        tests.append(("Tavily 搜索工具", True))
    except Exception as e:
        print(f"   ❌ src.tools.tavily_search 导入失败: {e}")
        tests.append(("Tavily 搜索工具", False))
    
    # 测试工具函数模块
    print("\n3. 测试工具函数模块...")
    try:
        from src.utils.memory import (
            get_actor_and_session_id,
            create_memory_config,
            build_context_aware_prompt,
            get_conversation_context
        )
        print("   ✅ src.utils.memory 导入成功")
        tests.append(("Memory 工具函数", True))
    except Exception as e:
        print(f"   ❌ src.utils.memory 导入失败: {e}")
        tests.append(("Memory 工具函数", False))
    
    try:
        from src.utils.prompts import SYSTEM_PROMPT
        print("   ✅ src.utils.prompts 导入成功")
        tests.append(("系统提示词", True))
    except Exception as e:
        print(f"   ❌ src.utils.prompts 导入失败: {e}")
        tests.append(("系统提示词", False))
    
    # 测试 Agent 核心模块
    print("\n4. 测试 Agent 核心模块...")
    try:
        from src.agent.main import app, invoke
        print("   ✅ src.agent.main 导入成功")
        tests.append(("Agent 核心", True))
    except Exception as e:
        print(f"   ❌ src.agent.main 导入失败: {e}")
        tests.append(("Agent 核心", False))
    
    # 测试向后兼容入口
    print("\n5. 测试向后兼容入口...")
    try:
        import agentcore_baidu_map_agent
        print("   ✅ agentcore_baidu_map_agent 导入成功")
        tests.append(("向后兼容入口", True))
    except Exception as e:
        print(f"   ❌ agentcore_baidu_map_agent 导入失败: {e}")
        tests.append(("向后兼容入口", False))
    
    # 统计结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for name, result in tests:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name:20s} {status}")
    
    print("\n" + "-" * 60)
    print(f"总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有模块导入成功！项目结构验证通过。")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 个模块导入失败，请检查。")
        return 1


def check_file_structure():
    """检查文件结构"""
    print("\n" + "=" * 60)
    print("检查文件结构")
    print("=" * 60)
    
    required_files = [
        "src/__init__.py",
        "src/config.py",
        "src/agent/__init__.py",
        "src/agent/main.py",
        "src/tools/__init__.py",
        "src/tools/baidu_maps.py",
        "src/tools/tavily_search.py",
        "src/utils/__init__.py",
        "src/utils/memory.py",
        "src/utils/prompts.py",
        "clients/__init__.py",
        "clients/boto3_client.py",
        "tests/__init__.py",
        "tests/test_memory.py",
        "docs/README.md",
        "docs/ARCHITECTURE.md",
        "docs/PROJECT_STRUCTURE.md",
        "agentcore_baidu_map_agent.py",
        "README.md",
        "requirements.txt",
        ".env.example",
        ".gitignore"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (缺失)")
            missing_files.append(file_path)
    
    print("\n" + "-" * 60)
    if not missing_files:
        print("✅ 所有必需文件都存在")
        return 0
    else:
        print(f"⚠️  缺失 {len(missing_files)} 个文件:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return 1


if __name__ == "__main__":
    print("\n🔍 开始验证项目结构...\n")
    
    # 检查文件结构
    file_check_result = check_file_structure()
    
    # 测试模块导入
    import_test_result = test_imports()
    
    # 总结
    print("\n" + "=" * 60)
    print("验证完成")
    print("=" * 60)
    
    if file_check_result == 0 and import_test_result == 0:
        print("\n✅ 项目结构完整，所有模块正常！")
        sys.exit(0)
    else:
        print("\n⚠️  发现问题，请检查上述错误信息。")
        sys.exit(1)
