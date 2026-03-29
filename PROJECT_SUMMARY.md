# BayerDBA - 多云数据库批量管理工具

## 项目概述

批量给 **AWS RDS** 和 **Azure Database** 的 MySQL/PostgreSQL 实例添加 DBA 用户。

**创建时间**: 2026-03-29  
**版本**: 1.1.0 (Azure Support)

---

## 🎯 核心功能

### 1. 多云支持
- ✅ **AWS RDS**: MySQL/Aurora + PostgreSQL
- ✅ **Azure Database**: MySQL + PostgreSQL
- ✅ **统一脚本**: 一个脚本管理所有云平台

### 2. 批量 DBA 用户管理
- ✅ 交互式输入 DBA 用户名和密码
- ✅ 智能检测用户是否存在
- ✅ 自动创建用户并授予 DBA 权限
- ✅ 生成详细执行报告和日志

### 3. 完整的 DBA 权限
- ✅ AWS RDS 兼容的最大权限
- ✅ Azure Database 兼容的最大权限
- ✅ MySQL: ALL PRIVILEGES + PROCESS + REPLICATION
- ✅ PostgreSQL: rds_superuser / azure_pg_admin

### 4. 单元测试套件
- ✅ **20 个单元测试，100% 通过**
- ✅ 测试数据结构、权限配置、边界情况
- ✅ 文件完整性检查

---

## 📁 项目结构

```
BayerDBA/
├── batch-add-dba-users.py          # 主脚本（多云批量管理）
├── azure_database_support.py        # Azure 数据库支持模块 ⭐
├── requirements.txt                 # Python 依赖
├── config-example.py                # 配置模板
├── run-tests.sh                     # 测试运行脚本
├── README-批量添加 DBA 用户.md       # 详细使用文档
├── PROJECT_SUMMARY.md              # 项目总结（本文件）
└── tests/
    ├── __init__.py
    ├── test_simple.py              # 单元测试 (20 个测试)
    └── TEST-REPORT.md              # 测试报告
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /Users/Wolf/.openclaw/workspace/projects/BayerDBA
pip3 install -r requirements.txt
```

### 2. 配置云厂商凭证

#### AWS
```bash
aws configure
```

#### Azure
```bash
az login
```

### 3. 运行批量添加

```bash
python3 batch-add-dba-users.py
```

### 4. 运行测试

```bash
python3 tests/test_simple.py
```

---

## 🔐 权限说明

### MySQL (AWS RDS / Azure Database)

```sql
CREATE USER 'dba_admin'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'dba_admin'@'%' WITH GRANT OPTION;
GRANT PROCESS ON *.* TO 'dba_admin'@'%';
GRANT REPLICATION CLIENT ON *.* TO 'dba_admin'@'%';
GRANT REPLICATION SLAVE ON *.* TO 'dba_admin'@'%';
FLUSH PRIVILEGES;
```

**注意**: 云厂商 MySQL 不支持 SUPER 权限。

### PostgreSQL

**AWS RDS:**
```sql
CREATE ROLE dba_admin WITH LOGIN PASSWORD 'password';
GRANT rds_superuser TO dba_admin;
```

**Azure Database:**
```sql
CREATE ROLE dba_admin WITH LOGIN PASSWORD 'password';
GRANT azure_pg_admin TO dba_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO dba_admin;
```

---

## 📊 测试结果

### 测试结果：20/20 通过 (100%)

| 测试类别 | 测试数 | 状态 |
|---------|-------|------|
| 数据结构测试 | 2 | ✅ |
| Azure 数据库支持 | 3 | ✅ |
| 多云平台配置 | 3 | ✅ |
| 权限配置测试 | 4 | ✅ |
| 边界情况测试 | 4 | ✅ |
| 文件存在性测试 | 4 | ✅ |

详细报告：[tests/TEST-REPORT.md](tests/TEST-REPORT.md)

---

## 💡 使用场景

### 场景 1：多云环境统一管理
公司同时使用 AWS 和 Azure，需要统一管理所有数据库的 DBA 账号。

### 场景 2：新团队入职
为新加入的 DBA 团队成员批量创建数据库账号。

### 场景 3：权限标准化
统一所有云数据库实例的 DBA 账号命名和权限。

### 场景 4：审计合规
定期检查并更新 DBA 账号密码。

---

## ⚠️ 安全建议

1. **强密码**: 至少 12 位，包含大小写、数字、特殊字符
2. **密码管理**: 使用 AWS Secrets Manager 或 Azure Key Vault
3. **访问控制**: 限制 DBA 用户只能从特定 IP 登录
4. **审计日志**: 开启云厂商的数据库审计
5. **最小权限**: 根据实际需求调整权限
6. **定期轮换**: 每 90 天更新一次密码

---

## 🔧 高级功能

### 平台选择

编辑 `batch-add-dba-users.py`:

```python
# 只处理 AWS
PLATFORM = "aws"

# 只处理 Azure
PLATFORM = "azure"

# 处理所有平台（默认）
PLATFORM = "all"
```

### 从密钥管理服务获取密码

**AWS Secrets Manager:**
```python
secrets_client = boto3.client('secretsmanager')
response = secrets_client.get_secret_value(SecretId='rds-master-password')
```

**Azure Key Vault:**
```python
from azure.keyvault.secrets import SecretClient
client = SecretClient(vault_url="https://your-vault.vault.azure.net/", credential=credential)
secret = client.get_secret("db-master-password")
```

### 并发执行

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_instance, inst) for inst in instances]
```

---

## 📞 故障排查

### AWS RDS 连接失败
- 检查安全组是否允许访问（3306/5432）
- 确认 RDS 实例为 "Publicly Accessible"
- 检查主用户密码

### Azure Database 连接失败
- 检查防火墙规则是否允许你的 IP
- 确认已登录 Azure (`az login`)
- 确认订阅 ID 正确

### 权限不足
- 确认主用户有 CREATE USER 和 GRANT 权限
- PostgreSQL 需要管理员角色

---

## 📚 参考文档

### AWS
- [AWS RDS MySQL 权限](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/MySQL.Procedural.Importing.NonSuper.html)
- [AWS RDS PostgreSQL 权限](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Concepts.General.DBRoles.html)

### Azure
- [Azure Database for MySQL 权限](https://docs.microsoft.com/en-us/azure/mysql/concepts-users-and-accounts)
- [Azure Database for PostgreSQL 权限](https://docs.microsoft.com/en-us/azure/postgresql/concepts-users)

---

## 📝 更新日志

### v1.1.0 (2026-03-29)
- ✅ 新增 Azure Database 支持
- ✅ 移除 IDEA 数据库支持
- ✅ 单元测试增加到 20 个
- ✅ 多云平台配置选项

### v1.0.0 (2026-03-29)
- ✅ 初始版本发布
- ✅ AWS RDS 批量管理
- ✅ 14 个单元测试

---

## 👨‍💻 维护者

**创建者**: BayerDBA Project  
**最后更新**: 2026-03-29  
**版本**: 1.1.0

---

## 📄 许可证

内部工具，仅供团队使用。
