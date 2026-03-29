# 批量添加 DBA 用户 - Excel 导入模式

## 📋 功能说明

从 **Excel 文件**读取数据库连接信息，批量添加 DBA 用户：
- ✅ **Excel 导入**: 从 Excel 文件读取所有数据库信息
- ✅ **多云支持**: AWS, Azure, 本地数据库
- ✅ **智能检测**: 用户不存在则先创建，再授权
- ✅ **两种模式**: 统一 DBA 凭证 或 独立 DBA 凭证
- ✅ **完整 DBA 权限**: MySQL + PostgreSQL
- ✅ **详细报告**: 生成执行报告和日志

---

## 📊 Excel 文件格式

### 必需列

| 列名 | 说明 | 示例 |
|------|------|------|
| `platform` | 云平台 | `aws`, `azure`, `other` |
| `database_type` | 数据库类型 | `mysql`, `postgresql` |
| `name` | 数据库名称 | `prod-db-01` |
| `host` | 主机地址 | `rm-xxx.mysql.rds.amazonaws.com` |
| `port` | 端口 | `3306`, `5432` |
| `username` | 主用户名 | `admin`, `root` |
| `password` | 主用户密码 | `YourPassword123!` |

### 可选列

| 列名 | 说明 |
|------|------|
| `dba_username` | DBA 用户名（留空则使用统一配置） |
| `dba_password` | DBA 密码（留空则使用统一配置） |
| `notes` | 备注 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /Users/Wolf/.openclaw/workspace/projects/BayerDBA
pip3 install -r requirements.txt
```

### 2. 创建 Excel 文件

**方法 A: 使用模板**
```bash
python3 create-excel-template.py
```
生成 `databases-template.xlsx`，包含示例数据。

**方法 B: 手动创建**
1. 打开 Excel
2. 创建表头：`platform`, `database_type`, `name`, `host`, `port`, `username`, `password`
3. 填写数据库信息
4. 保存为 `databases.xlsx`

### 3. 编辑 Excel 文件

示例数据：

| platform | database_type | name | host | port | username | password | notes |
|----------|---------------|------|------|------|----------|----------|-------|
| aws | mysql | prod-db-01 | rm-prod.mysql.rds.amazonaws.com | 3306 | admin | AdminPass123! | 生产数据库 |
| azure | postgresql | test-db | test.postgres.database.azure.com | 5432 | azureadmin | TestPass456! | 测试数据库 |
| other | mysql | local-db | 192.168.1.100 | 3306 | root | LocalPass789! | 本地数据库 |

### 4. 运行脚本

```bash
python3 batch-add-dba-users.py
```

脚本会提示输入：
1. **DBA 用户名**（如果 Excel 中未指定）
2. **DBA 密码**（如果 Excel 中未指定）

---

## 💡 两种凭证模式

### 模式 1: 统一 DBA 凭证（推荐）

所有数据库使用同一个 DBA 用户名和密码。

**Excel 配置:**
- 不填写 `dba_username` 和 `dba_password` 列
- 运行时输入统一的 DBA 凭证

**优点:**
- 管理简单
- 容易记忆
- 适合标准化环境

### 模式 2: 独立 DBA 凭证

每个数据库有自己的 DBA 用户名和密码。

**Excel 配置:**
- 填写 `dba_username` 和 `dba_password` 列
- 脚本会使用 Excel 中的凭证

**优点:**
- 更高的安全性
- 符合审计要求
- 适合多租户环境

---

## 📊 输出文件

| 文件 | 说明 |
|------|------|
| `dba-batch-YYYYMMDD-HHMMSS.log` | 详细执行日志 |
| `dba-batch-YYYYMMDD-HHMMSS-report.json` | JSON 格式执行报告 |

### 报告示例

```json
{
  "timestamp": "2026-03-29T14:15:00",
  "excel_file": "databases.xlsx",
  "dba_user": "dba_admin",
  "summary": {
    "total_databases": 50,
    "success": 48,
    "failed": 2,
    "user_created": 30,
    "user_existed": 18
  },
  "details": [
    {
      "instance_id": "prod-db-01",
      "endpoint": "rm-prod.mysql.rds.amazonaws.com",
      "engine": "mysql",
      "status": "success",
      "user_existed": false,
      "user_created": true,
      "error": null
    }
  ]
}
```

---

## ⚠️ 安全建议

1. **Excel 文件保护**
   - 设置 Excel 文件密码
   - 使用后立即删除或加密存储
   - 不要通过不安全的渠道传输

2. **密码强度**
   - 至少 12 位
   - 包含大小写、数字、特殊字符
   - 定期更换

3. **访问控制**
   - 限制 DBA 用户只能从特定 IP 登录
   - 开启数据库审计日志

4. **最小权限**
   - 根据实际需求调整权限
   - 避免过度授权

---

## 🔧 高级用法

### 修改 Excel 文件路径

编辑 `batch-add-dba-users.py`:

```python
EXCEL_FILE = "your-databases.xlsx"  # 修改为你的文件路径
```

### 批量验证 Excel 数据

```bash
python3 -c "
from excel_database_reader import ExcelDatabaseReader
reader = ExcelDatabaseReader('databases.xlsx')
databases = reader.read_excel()
validation = reader.validate_connections()
print(f'Errors: {len(validation[\"errors\"])}')
print(f'Warnings: {len(validation[\"warnings\"])}')
"
```

### 按平台筛选数据库

```bash
python3 -c "
from excel_database_reader import ExcelDatabaseReader
reader = ExcelDatabaseReader('databases.xlsx')
databases = reader.read_excel()

# 只处理 AWS 数据库
aws_dbs = reader.get_databases_by_platform('aws')
print(f'AWS 数据库：{len(aws_dbs)} 个')

# 只处理 MySQL 数据库
mysql_dbs = reader.get_databases_by_type('mysql')
print(f'MySQL 数据库：{len(mysql_dbs)} 个')
"
```

---

## 📞 故障排查

### Excel 文件不存在

```
错误：Excel 文件不存在：databases.xlsx
```

**解决:**
- 确认文件路径正确
- 使用绝对路径或切换到正确的工作目录

### 缺少必需列

```
错误：Excel 文件缺少必要列：['host', 'password']
```

**解决:**
- 检查表头拼写是否正确
- 确保所有必需列都存在

### 连接失败

```
MySQL xxx 失败：Connection refused
```

**解决:**
- 检查主机地址和端口是否正确
- 确认防火墙允许访问
- 验证主用户密码

### 密码强度警告

```
警告：第 3 行：密码长度过短（6 位）
```

**解决:**
- 使用更复杂的密码（至少 8 位）
- 包含大小写、数字、特殊字符

---

## 📝 执行前检查清单

- [ ] Excel 文件已创建并填写完整
- [ ] 所有必需列都已填写
- [ ] 主机地址和端口正确
- [ ] 主用户密码正确
- [ ] 已备份重要配置
- [ ] 已测试单个数据库连接
- [ ] Excel 文件已加密保护（推荐）

---

## 💡 示例场景

### 场景 1: 新环境初始化

1. 创建 Excel 文件，列出所有新数据库
2. 使用统一 DBA 凭证模式
3. 一次性为所有数据库创建 DBA 用户

### 场景 2: 多环境管理

1. 创建多个 Excel 文件（prod.xlsx, test.xlsx, dev.xlsx）
2. 每个环境使用不同的 DBA 凭证
3. 分别执行脚本

### 场景 3: 定期审计

1. 从现有数据库导出连接信息到 Excel
2. 运行脚本更新 DBA 用户密码
3. 生成审计报告

---

## 📚 参考文档

- [Excel 模板说明](EXCEL-TEMPLATE.md)
- [AWS RDS 权限](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/MySQL.Procedural.Importing.NonSuper.html)
- [Azure Database 权限](https://docs.microsoft.com/en-us/azure/mysql/concepts-users-and-accounts)

---

**创建时间**: 2026-03-29  
**版本**: 2.0.0 (Excel Import)  
**适用平台**: AWS + Azure + 本地数据库  
**支持数据库**: MySQL + PostgreSQL
