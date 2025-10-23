.PHONY: help install verify test deploy status destroy clean

help:
	@echo "AgentCore 百度地图 Agent - 常用命令"
	@echo ""
	@echo "开发命令:"
	@echo "  make install    - 安装依赖"
	@echo "  make verify     - 验证项目结构"
	@echo "  make test       - 运行测试"
	@echo ""
	@echo "部署命令:"
	@echo "  make deploy     - 部署到 AgentCore"
	@echo "  make status     - 查看部署状态"
	@echo "  make destroy    - 销毁部署"
	@echo ""
	@echo "其他命令:"
	@echo "  make clean      - 清理临时文件"
	@echo "  make help       - 显示此帮助信息"

install:
	@echo "安装依赖..."
	pip install -r requirements.txt
	@echo "✅ 依赖安装完成"

verify:
	@echo "验证项目结构..."
	python3 verify_structure.py

test:
	@echo "运行测试..."
	python3 tests/test_memory.py

deploy:
	@echo "部署到 AgentCore..."
	agentcore configure -e agentcore_baidu_map_agent.py
	agentcore launch
	@echo "✅ 部署完成"

status:
	@echo "查看部署状态..."
	agentcore status

destroy:
	@echo "销毁部署..."
	agentcore destroy
	@echo "✅ 销毁完成"

clean:
	@echo "清理临时文件..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	@echo "✅ 清理完成"
