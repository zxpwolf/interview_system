# 批量添加 DBA 用户 - AWS RDS

## 📋 功能说明

批量给 AWS RDS MySQL/Aurora 和 PostgreSQL 实例添加 DBA 用户：
- ✅ 自动检测用户是否存在
- ✅ 不存在则创建，存在则更新权限
- ✅ 授予完整 DBA 权限
- ✅ 生成执行报告和日志

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /Users/Wolf/.openclaw/workspace/projects/BayerDBA
pip3 install -r requirements.txt
```

### 2. 配置 AWS

```bash
# 配置 AWS 凭证
aws configure

# 或指定 profile
aws configure --profile your-profile
```

### 3. 编辑脚本配置

编辑 `batch-add-dba-users.py`，修改以下配置：

```python
# DBA 用户配置
DBA_USER = "dba_admin"           # ← 修改为你的 DBA 用户名
DBA_PASS = "YourSecurePassword!"  # ← 修改为你的 DBA 密码

# AWS 配置
AWS_REGION = "us-east-1"    # ← 修改为你的区域
AWS_PROFILE = "default"     # ← 修改为你的 AWS profile
```

### 4. 运行脚本

```bash
python3 batch-add-dba-users.py
```

脚本会提示输入 RDS 主用户密码（用于登录各实例执行 SQL）。

## 📊 输出文件

| 文件 | 说明 |
|------|------|
| `dba-batch-YYYYMMDD-HHMMSS.log` | 详细执行日志 |
| `dba-batch-YYYYMMDD-HHMMSS-report.json` | JSON 格式执行报告 |

## 🔐 权限说明

### MySQL/Aurora 权限
```sql
GRANT ALL PRIVILEGES ON *.* TO 'dba_admin'@'%' WITH GRANT OPTION;
GRANT PROCESS ON *.* TO 'dba_admin'@'%';
GRANT REPLICATION CLIENT ON *.* TO 'dba_admin'@'%';
GRANT REPLICATION SLAVE ON *.* TO 'dba_admin'@'%';
```

### PostgreSQL 权限
```sql
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dba_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO dba_admin;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO dba_admin;
ALTER ROLE dba_admin SET search_path TO public;
```

## ⚠️ 安全建议

1. **密码管理**：使用强密码，建议从 Secrets Manager 动态获取
2. **白名单**：限制 DBA 用户只能从特定 IP 登录
3. **审计**：开启 RDS 审计日志
4. **测试**：先在小范围测试，确认无误后再批量执行

## 🔧 高级用法

### 只处理特定实例

编辑脚本，在 `get_all_instances()` 后添加过滤：

```python
# 只处理特定名称的实例
instances = [i for i in instances if 'prod' in i.instance_id]
```

### 从 Secrets Manager 获取主密码

```python
secrets_client = boto3.client('secretsmanager')
response = secrets_client.get_secret_value(SecretId='your-secret-id')
master_password = json.loads(response['SecretString'])['password']
```

### 并发执行（加速）

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_instance, inst) for inst in instances]
    for future in as_completed(futures):
        result = future.result()
        # 处理结果
```

## 📞 故障排查

### 连接失败
- 检查安全组是否允许访问
- 确认 RDS 实例为" publicly accessible"或在同一 VPC
- 检查主用户密码是否正确

### 权限不足
- 确认主用户有 CREATE USER 和 GRANT 权限
- RDS 某些 SUPER 权限可能受限

### 用户已存在
- 脚本会自动处理，不会报错
- 会更新现有用户的权限

## 📝 执行前检查清单

- [ ] AWS 凭证已配置
- [ ] DBA 用户名和密码已设置
- [ ] 已测试单个实例连接
- [ ] 已备份重要配置
- [ ] 已通知相关团队

---

**创建时间**: 2026-03-29
**适用平台**: AWS RDS (MySQL/Aurora/PostgreSQL)
