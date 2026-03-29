#!/bin/bash
# 运行所有单元测试

set -e

echo "============================================================"
echo "BayerDBA - 单元测试套件"
echo "============================================================"

# 切换到项目目录
cd "$(dirname "$0")"

# 安装测试依赖（如果需要）
echo ""
echo "📦 检查依赖..."
pip3 install -q -r requirements.txt

# 运行单元测试
echo ""
echo "🧪 运行单元测试..."
echo ""

python3 -m pytest tests/ \
    --verbose \
    --cov=. \
    --cov-report=term-missing \
    --cov-report=html:reports/coverage \
    --html=reports/test-report.html \
    --self-contained-html \
    -o log_cli=true \
    -o log_cli_level=INFO

# 输出测试结果
echo ""
echo "============================================================"
echo "✅ 测试完成！"
echo "============================================================"
echo ""
echo "📊 测试报告:"
echo "  - HTML 报告：reports/test-report.html"
echo "  - 覆盖率报告：reports/coverage/index.html"
echo ""
