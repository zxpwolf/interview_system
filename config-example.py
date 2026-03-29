#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速配置模板 - 复制此文件为 config.py 并修改配置
"""

# ==================== DBA 用户配置 ====================
# 格式：{"用户名": "密码"}
# 可以添加任意数量的用户
DBA_USERS = {
    # 管理员用户 - 完整权限
    "dba_admin": "YourAdminPassword123!",
    
    # 运维用户 - 完整权限
    "dba_ops": "YourOpsPassword456!",
    
    # 只读用户 - 可以改为只读权限（需要修改脚本）
    "dba_readonly": "YourReadonlyPassword789!",
    
    # 添加更多用户...
    # "username": "password",
}

# ==================== AWS 配置 ====================
# AWS 区域（根据你的 RDS 所在区域修改）
AWS_REGION = "us-east-1"  # 美东
# AWS_REGION = "us-west-2"  # 美西
# AWS_REGION = "ap-northeast-1"  # 东京
# AWS_REGION = "ap-southeast-1"  # 新加坡
# AWS_REGION = "cn-north-1"  # 北京（需要中国账户）

# AWS Profile 名称（如使用默认 profile 则留空或填 "default"）
AWS_PROFILE = "default"

# ==================== 其他配置 ====================
# 日志级别：DEBUG, INFO, WARNING, ERROR
LOG_LEVEL = "INFO"

# 是否启用并发执行（True/False）
# 并发可以加快速度，但可能增加数据库负载
ENABLE_CONCURRENCY = False

# 并发 worker 数量（仅在启用并发时有效）
MAX_WORKERS = 10

# ==================== 测试配置 ====================
# 测试模式：只处理前 N 个实例（0 表示处理所有）
# 建议首次运行时设置为 1-2 进行测试
TEST_MODE_COUNT = 0  # 0 = 处理所有实例
