# Excel 数据库列表模板

## 必需列

| 列名 | 说明 | 示例 |
|------|------|------|
| `platform` | 云平台 | `aws`, `azure`, `other` |
| `database_type` | 数据库类型 | `mysql`, `postgresql` |
| `name` | 数据库名称/标识 | `prod-db-001` |
| `host` | 主机地址 | `rm-xxx.mysql.rds.amazonaws.com` |
| `port` | 端口 | `3306`, `5432` |
| `username` | 主用户名 | `admin`, `root`, `azureadmin` |
| `password` | 主用户密码 | `YourPassword123!` |

## 可选列

| 列名 | 说明 | 示例 |
|------|------|------|
| `dba_username` | 要创建的 DBA 用户名（留空则使用统一配置） | `dba_admin` |
| `dba_password` | DBA 密码（留空则使用统一配置） | `DBAPass123!` |
| `notes` | 备注 | `生产数据库`, `测试环境` |

---

## Excel 示例

| platform | database_type | name | host | port | username | password | dba_username | dba_password | notes |
|----------|---------------|------|------|------|----------|----------|--------------|--------------|-------|
| aws | mysql | prod-mysql-01 | rm-prod01.mysql.rds.amazonaws.com | 3306 | admin | AdminPass123! | dba_admin | DBAPass123! | 生产 MySQL |
| aws | postgresql | prod-pg-01 | pg-prod01.postgres.rds.amazonaws.com | 5432 | postgres | PGPass456! | dba_admin | DBAPass123! | 生产 PG |
| azure | mysql | test-mysql | test-mysql.mysql.database.azure.com | 3306 | azureadmin | AzurePass789! | | | 测试 MySQL（使用统一 DBA 凭证） |
| azure | postgresql | test-pg | test-pg.postgres.database.azure.com | 5432 | azureadmin | AzurePass012! | | | 测试 PG（使用统一 DBA 凭证） |
| other | mysql | local-db | 192.168.1.100 | 3306 | root | LocalPass345! | dba_local | LocalDBA678! | 本地数据库 |

---

## 使用说明

1. **创建 Excel 文件**
   - 使用 Microsoft Excel、WPS、或 Google Sheets
   - 第一行必须是表头（列名）
   - 从第二行开始填写数据库信息

2. **保存文件**
   - 保存为 `.xlsx` 格式
   - 默认文件名：`databases.xlsx`
   - 或修改 `batch-add-dba-users.py` 中的 `EXCEL_FILE` 配置

3. **运行脚本**
   ```bash
   python3 batch-add-dba-users.py
   ```

4. **凭证模式**
   - **统一凭证**：所有数据库使用同一个 DBA 用户名和密码（推荐）
   - **独立凭证**：每个数据库在 Excel 中指定不同的 DBA 凭证

---

## 注意事项

1. **密码安全**
   - Excel 文件包含明文密码，请妥善保管
   - 建议设置 Excel 文件密码保护
   - 使用后立即删除或加密存储

2. **数据验证**
   - 脚本会自动验证必要列是否存在
   - 会检查端口号、主机格式、密码强度
   - 发现错误会停止执行

3. **特殊字符**
   - 密码中的特殊字符（如 `@`, `!`, `#`）需要正确转义
   - 建议在 Excel 中使用文本格式存储密码

4. **空行处理**
   - 脚本会自动跳过空行
   - 必要字段为空的行会被跳过并记录警告

---

## 模板下载

可以复制上面的表格到 Excel，或运行以下命令创建模板：

```bash
python3 -c "
import openpyxl
wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Databases'

# 表头
headers = ['platform', 'database_type', 'name', 'host', 'port', 'username', 'password', 'dba_username', 'dba_password', 'notes']
ws.append(headers)

# 示例数据
examples = [
    ['aws', 'mysql', 'prod-db-01', 'rm-prod.mysql.rds.amazonaws.com', 3306, 'admin', 'Password123!', 'dba_admin', 'DBAPass123!', '生产数据库'],
    ['azure', 'postgresql', 'test-db', 'test.postgres.database.azure.com', 5432, 'azureadmin', 'TestPass456!', '', '', '测试数据库'],
]

for row in examples:
    ws.append(row)

wb.save('databases-template.xlsx')
print('模板已创建：databases-template.xlsx')
"
```
