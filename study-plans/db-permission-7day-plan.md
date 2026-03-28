# 数据库权限管理 - 7 天强化学习计划

**学员:** Jackie Zhou  
**起始日期:** 2026-03-08  
**目标:** 从 L2 中级 (50 分) 提升到 L3 高级 (75+ 分)  
**重点突破:** 权限管理 (当前 20% → 目标 80%+)

---

## 📊 当前状态分析

| 子领域 | 正确率 | 状态 |
|--------|--------|------|
| 权限管理 | 20% | 🔴 重点突破 |
| 安全管理 | 75% | 🟢 保持 |
| 备份管理 | 100% | 🟢 保持 |

**薄弱环节:**
- ❌ SQL 权限命令 (GRANT/REVOKE)
- ❌ PostgreSQL 角色系统
- ❌ MySQL 8.0 角色功能
- ❌ 列级权限实现
- ❌ SQL 注入防护

---

## 📅 学习日历

| 日期 | 主题 | 时长 | 目标 |
|------|------|------|------|
| Day 1 (03/08) | SQL 权限基础：GRANT/REVOKE | 60 分钟 | 掌握基本语法 |
| Day 2 (03/09) | MySQL 用户与权限管理 | 60 分钟 | 理解 MySQL 权限系统 |
| Day 3 (03/10) | PostgreSQL 角色系统 | 60 分钟 | 掌握角色/用户关系 |
| Day 4 (03/11) | MySQL 8.0 角色功能 | 60 分钟 | 理解角色嵌套 |
| Day 5 (03/12) | 列级权限与视图 | 60 分钟 | 掌握列级控制方法 |
| Day 6 (03/13) | SQL 注入防护 | 60 分钟 | 掌握参数化查询 |
| Day 7 (03/14) | 综合复习与测评 | 90 分钟 | 检验学习成果 |

---

# 📖 Day 1 - SQL 权限基础：GRANT/REVOKE

**日期:** 2026-03-08  
**学习时长:** 60 分钟

---

## 🎯 学习目标

1. 理解 SQL 标准权限命令
2. 掌握 GRANT 语法和用法
3. 掌握 REVOKE 语法和用法
4. 理解权限的层次结构

---

## 📚 知识点讲解

### 1.1 SQL 权限命令概览

SQL 标准定义了以下权限管理命令：

| 命令 | 用途 | 示例 |
|------|------|------|
| **GRANT** | 授予权限 | `GRANT SELECT ON table TO user;` |
| **REVOKE** | 撤销权限 | `REVOKE SELECT ON table FROM user;` |
| **CREATE USER** | 创建用户 | `CREATE USER 'name'@'host' IDENTIFIED BY 'pwd';` |
| **DROP USER** | 删除用户 | `DROP USER 'name'@'host';` |

**⚠️ 重点:** SQL 标准中**没有** `REMOVE`、`DENY`、`PERMIT` 等命令！

---

### 1.2 GRANT 语法详解

**基本语法:**
```sql
GRANT 权限类型 ON 数据库对象 TO 用户 [WITH GRANT OPTION];
```

**权限类型:**
| 权限 | 说明 |
|------|------|
| SELECT | 读取数据 |
| INSERT | 插入数据 |
| UPDATE | 更新数据 |
| DELETE | 删除数据 |
| ALL PRIVILEGES | 所有权限 |

**数据库对象层次:**
```
*                    -- 全局级别 (所有数据库)
database.*           -- 数据库级别 (所有表)
database.table       -- 表级别
database.table(col)  -- 列级别 (部分数据库支持)
```

**示例:**
```sql
-- 授予单个表的 SELECT 权限
GRANT SELECT ON sales.orders TO 'analyst'@'localhost';

-- 授予整个数据库的所有权限
GRANT ALL PRIVILEGES ON mydb.* TO 'admin'@'localhost';

-- 授予多个权限
GRANT SELECT, INSERT, UPDATE ON mydb.users TO 'editor'@'%';

-- 允许用户转授权限
GRANT SELECT ON mydb.* TO 'manager'@'localhost' WITH GRANT OPTION;
```

---

### 1.3 REVOKE 语法详解

**基本语法:**
```sql
REVOKE 权限类型 ON 数据库对象 FROM 用户;
```

**示例:**
```sql
-- 撤销单个权限
REVOKE DELETE ON sales.orders FROM 'analyst'@'localhost';

-- 撤销所有权限
REVOKE ALL PRIVILEGES ON mydb.* FROM 'old_user'@'localhost';

-- 撤销转授权限
REVOKE GRANT OPTION ON mydb.* FROM 'manager'@'localhost';
```

**⚠️ 注意事项:**
- REVOKE 只能撤销已授予的权限
- 撤销 GRANT OPTION 不会撤销已转授的权限
- 删除用户前需要先撤销权限

---

### 1.4 权限层次结构

```
┌─────────────────────────────────────┐
│  GLOBAL ( *.* )                     │  ← 最高级别
│  适用于所有数据库的所有表            │
├─────────────────────────────────────┤
│  DATABASE ( db.* )                  │  ← 数据库级别
│  适用于指定数据库的所有表            │
├─────────────────────────────────────┤
│  TABLE ( db.table )                 │  ← 表级别
│  适用于指定表                        │
├─────────────────────────────────────┤
│  COLUMN ( db.table(col) )           │  ← 列级别
│  适用于指定列 (部分数据库支持)        │
└─────────────────────────────────────┘
```

**权限继承规则:**
- 上级权限自动包含下级权限
- 授予全局 SELECT = 所有数据库都可读
- 权限是累积的 (用户可以有多个权限来源)

---

## 💻 实践练习

### 练习 1: 创建用户并授权

```sql
-- 1. 创建新用户
CREATE USER 'test_user'@'localhost' IDENTIFIED BY 'SecurePass123!';

-- 2. 授予只读权限
GRANT SELECT ON mydb.* TO 'test_user'@'localhost';

-- 3. 验证权限
SHOW GRANTS FOR 'test_user'@'localhost';

-- 4. 撤销权限
REVOKE SELECT ON mydb.* FROM 'test_user'@'localhost';

-- 5. 删除用户
DROP USER 'test_user'@'localhost';
```

### 练习 2: 权限场景模拟

```sql
-- 场景：数据分析师需要读取销售数据，但不能修改
CREATE USER 'analyst'@'192.168.1.%' IDENTIFIED BY 'AnalystPass!';
GRANT SELECT ON sales.* TO 'analyst'@'192.168.1.%';

-- 场景：开发人员需要完整权限，但不能删除数据库
CREATE USER 'developer'@'localhost' IDENTIFIED BY 'DevPass!';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER ON mydb.* 
TO 'developer'@'localhost';

-- 场景：管理员需要所有权限
CREATE USER 'dba'@'localhost' IDENTIFIED BY 'DBAPass!';
GRANT ALL PRIVILEGES ON *.* TO 'dba'@'localhost' WITH GRANT OPTION;
```

---

## 📝 今日测验 (5 题)

**1.** 撤销用户权限应该使用哪个命令？
- A. REMOVE
- B. REVOKE
- C. DENY
- D. DELETE

**2.** 以下哪个 GRANT 语句语法正确？
- A. `GRANT SELECT * TO user ON database`
- B. `GRANT SELECT ON database.* TO user`
- C. `ALLOW SELECT ON database.* TO user`
- D. `PERMIT SELECT ON database.* TO user`

**3.** 授予用户对特定表的 SELECT 和 INSERT 权限，正确的是？
- A. `GRANT SELECT, INSERT ON db.table TO user`
- B. `GRANT SELECT AND INSERT ON db.table TO user`
- C. `GRANT SELECT ON db.table, INSERT ON db.table TO user`
- D. `GRANT SELECT; GRANT INSERT ON db.table TO user`

**4.** WITH GRANT OPTION 的作用是？
- A. 允许用户删除表
- B. 允许用户转授权限给其他用户
- C. 允许用户创建数据库
- D. 允许用户修改密码

**5.** 以下哪个权限级别最高？
- A. 表级别 (db.table)
- B. 数据库级别 (db.*)
- C. 全局级别 (*.*)
- D. 列级别 (db.table(col))

---

## ✅ 今日检查清单

- [ ] 阅读完所有知识点讲解
- [ ] 完成实践练习 (可在本地或测试环境)
- [ ] 完成今日测验 (目标：5/5)
- [ ] 记录疑问点 (如有)

---

## 📝 学习笔记

_在此记录你的学习心得和疑问:_

```
今日收获:


疑问点:


明日目标:


```

---

---

# 📖 Day 2 - MySQL 用户与权限管理

**日期:** 2026-03-09  
**学习时长:** 60 分钟

---

## 🎯 学习目标

1. 理解 MySQL 权限系统架构
2. 掌握 MySQL 用户管理
3. 理解权限表结构
4. 掌握权限刷新和验证

---

## 📚 知识点讲解

### 2.1 MySQL 权限系统架构

MySQL 权限信息存储在 `mysql` 数据库的系统表中：

| 表名 | 权限级别 | 说明 |
|------|----------|------|
| `user` | 全局级别 | 用户账户和全局权限 |
| `db` | 数据库级别 | 数据库级别权限 |
| `tables_priv` | 表级别 | 表级别权限 |
| `columnspriv` | 列级别 | 列级别权限 |
| `procspriv` | 存储过程 | 存储过程权限 |

**权限验证流程:**
```
1. 用户连接 → 验证 user 表 (主机、用户名、密码)
2. 执行操作 → 检查全局权限 (user 表)
3. 访问数据库 → 检查数据库权限 (db 表)
4. 访问表 → 检查表权限 (tablespriv 表)
5. 访问列 → 检查列权限 (columnspriv 表)
```

---

### 2.2 MySQL 用户管理

**创建用户:**
```sql
-- 基本语法
CREATE USER 'username'@'host' IDENTIFIED BY 'password';

-- 常见 host 值
'localhost'      -- 仅本地连接
'%'              -- 任意主机
'192.168.1.%'    -- 指定网段
'192.168.1.100'  -- 指定 IP
```

**修改用户:**
```sql
-- 修改密码
ALTER USER 'user'@'localhost' IDENTIFIED BY 'new_password';

-- 重命名用户
RENAME USER 'old_user'@'localhost' TO 'new_user'@'localhost';

-- 锁定/解锁用户
ALTER USER 'user'@'localhost' ACCOUNT LOCK;
ALTER USER 'user'@'localhost' ACCOUNT UNLOCK;
```

**删除用户:**
```sql
DROP USER 'username'@'host';
```

---

### 2.3 查看权限

```sql
-- 查看当前用户权限
SHOW GRANTS;

-- 查看指定用户权限
SHOW GRANTS FOR 'user'@'localhost';

-- 查看 mysql.user 表
SELECT user, host, select_priv, insert_priv, update_priv, delete_priv 
FROM mysql.user;

-- 查看数据库级别权限
SELECT * FROM mysql.db WHERE user = 'username';

-- 查看表级别权限
SELECT * FROM mysql.tables_priv WHERE user = 'username';
```

---

### 2.4 权限刷新

```sql
-- 刷新权限 (使权限表更改生效)
FLUSH PRIVILEGES;

-- 注意：使用 GRANT/REVOKE 自动刷新，直接修改表需要手动刷新
```

---

## 💻 实践练习

```sql
-- 1. 创建只读用户
CREATE USER 'readonly'@'%' IDENTIFIED BY 'Read123!';
GRANT SELECT ON mydb.* TO 'readonly'@'%';
FLUSH PRIVILEGES;

-- 2. 创建读写用户
CREATE USER 'readwrite'@'192.168.1.%' IDENTIFIED BY 'RW123!';
GRANT SELECT, INSERT, UPDATE, DELETE ON mydb.* TO 'readwrite'@'192.168.1.%';

-- 3. 查看权限
SHOW GRANTS FOR 'readonly'@'%';
SHOW GRANTS FOR 'readwrite'@'192.168.1.%';

-- 4. 撤销权限
REVOKE DELETE ON mydb.* FROM 'readwrite'@'192.168.1.%';

-- 5. 验证权限变更
SHOW GRANTS FOR 'readwrite'@'192.168.1.%';
```

---

## 📝 今日测验 (5 题)

**1.** MySQL 权限信息存储在哪个数据库？
- A. information_schema
- B. performance_schema
- C. mysql
- D. sys

**2.** 允许用户从任意主机连接，host 应该设置为？
- A. '*'
- B. '%'
- C. 'any'
- D. 'all'

**3.** 直接修改 mysql.user 表后，需要执行什么命令使更改生效？
- A. RELOAD PRIVILEGES
- B. FLUSH PRIVILEGES
- C. REFRESH PERMISSIONS
- D. UPDATE PERMISSIONS

**4.** 查看用户权限的命令是？
- A. DISPLAY GRANTS
- B. SHOW PERMISSIONS
- C. SHOW GRANTS FOR user
- D. VIEW GRANTS

**5.** 删除用户的命令是？
- A. DELETE USER
- B. REMOVE USER
- C. DROP USER
- D. ERASE USER

---

## ✅ 今日检查清单

- [ ] 阅读完所有知识点讲解
- [ ] 完成实践练习
- [ ] 完成今日测验 (目标：5/5)
- [ ] 复习 Day 1 内容

---

*继续查看 Day 3 内容...*

---

# 📖 Day 3 - PostgreSQL 角色系统

**日期:** 2026-03-10  
**学习时长:** 60 分钟

---

## 🎯 学习目标

1. 理解 PostgreSQL 角色与用户的关系
2. 掌握角色创建和管理
3. 理解角色继承机制
4. 掌握行级安全策略

---

## 📚 知识点讲解

### 3.1 角色与用户的关系

**核心概念:**
> **在 PostgreSQL 中，用户 = 带有 LOGIN 权限的角色**

```sql
-- 以下两个命令等价
CREATE USER myuser WITH PASSWORD 'mypass';
CREATE ROLE myrole WITH LOGIN PASSWORD 'mypass';

-- 唯一区别：CREATE USER 默认包含 LOGIN，CREATE ROLE 默认不包含
```

**角色属性:**
| 属性 | 说明 | 示例 |
|------|------|------|
| LOGIN | 允许登录 | `WITH LOGIN` |
| SUPERUSER | 超级用户 | `WITH SUPERUSER` |
| CREATEDB | 创建数据库 | `WITH CREATEDB` |
| CREATEROLE | 创建角色 | `WITH CREATEROLE` |
| INHERIT | 继承权限 | `WITH INHERIT` (默认) |

---

### 3.2 角色创建与管理

**创建角色:**
```sql
-- 创建登录角色 (用户)
CREATE ROLE developer WITH LOGIN PASSWORD 'DevPass123!';

-- 创建不能登录的角色 (用于权限分组)
CREATE ROLE read_only NOLOGIN;

-- 创建超级用户
CREATE ROLE admin WITH LOGIN SUPERUSER PASSWORD 'AdminPass!';
```

**修改角色:**
```sql
-- 修改密码
ALTER ROLE developer PASSWORD 'NewPass123!';

-- 添加 LOGIN 权限
ALTER ROLE read_only WITH LOGIN;

-- 删除角色
DROP ROLE read_only;
```

**查看角色:**
```sql
-- 查看所有角色
\du

-- 查看角色详细信息
SELECT rolname, rolsuper, rolcreaterole, rolcreatedb, rolcanlogin 
FROM pg_roles;
```

---

### 3.3 角色继承

**角色可以授予其他角色 (角色嵌套):**
```sql
-- 创建角色层次
CREATE ROLE base_read NOLOGIN;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO base_read;

CREATE ROLE analyst NOLOGIN;
GRANT base_read TO analyst;  -- analyst 继承 base_read 的权限
GRANT SELECT ON reports TO analyst;  -- 额外权限

CREATE ROLE senior_analyst WITH LOGIN;
GRANT analyst TO senior_analyst;  -- senior_analyst 继承 analyst 的权限
```

**权限继承链:**
```
senior_analyst (登录)
    ↓ inherits
analyst (无登录)
    ↓ inherits
base_read (无登录)
    ↓ has
SELECT on ALL TABLES
```

**查看角色成员:**
```sql
-- 查看角色被授予给哪些用户
SELECT pg_roles.rolname as role, 
       pg_auth_members.member as granted_to
FROM pg_roles
JOIN pg_auth_members ON pg_roles.oid = pg_auth_members.roleid;
```

---

### 3.4 权限管理

**授予权限:**
```sql
-- 表级别权限
GRANT SELECT, INSERT ON table_name TO role_name;

-- Schema 级别权限
GRANT USAGE ON SCHEMA schema_name TO role_name;

-- 数据库级别权限
GRANT CONNECT ON DATABASE db_name TO role_name;

-- 所有表权限
GRANT SELECT ON ALL TABLES IN SCHEMA public TO role_name;
```

**撤销权限:**
```sql
REVOKE DELETE ON table_name FROM role_name;
```

---

## 💻 实践练习

```sql
-- 1. 创建角色层次结构
CREATE ROLE app_read NOLOGIN;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_read;

CREATE ROLE app_write NOLOGIN;
GRANT app_read TO app_write;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_write;

CREATE ROLE app_user WITH LOGIN PASSWORD 'UserPass!';
GRANT app_write TO app_user;

-- 2. 验证权限继承
\du  -- 查看角色
\dp   -- 查看表权限

-- 3. 测试权限
-- 使用 app_user 连接，尝试 SELECT 和 INSERT
```

---

## 📝 今日测验 (5 题)

**1.** PostgreSQL 中，用户和角色的关系是？
- A. 完全不同的概念
- B. 用户是带有 LOGIN 权限的角色
- C. 角色只能用于权限分组
- D. 用户可以继承角色权限，但不能反向

**2.** 创建不能登录的角色，应该使用？
- A. CREATE USER role_name NOLOGIN
- B. CREATE ROLE role_name NOLOGIN
- C. CREATE ROLE role_name WITHOUT LOGIN
- D. CREATE GROUP role_name

**3.** 角色继承的正确语法是？
- A. INHERIT role_name TO other_role
- B. GRANT role_name TO other_role
- C. ADD role_name TO other_role
- D. ATTACH role_name TO other_role

**4.** 默认情况下，PostgreSQL 角色是否继承其他角色的权限？
- A. 是，默认 INHERIT
- B. 否，需要显式设置
- C. 只有超级用户可以继承
- D. 只有 LOGIN 角色可以继承

**5.** 查看 PostgreSQL 角色的命令是？
- A. SHOW ROLES
- B. LIST ROLES
- C. \du
- D. SELECT * FROM roles

---

## ✅ 今日检查清单

- [ ] 阅读完所有知识点讲解
- [ ] 完成实践练习
- [ ] 完成今日测验 (目标：5/5)
- [ ] 复习 Day 1-2 内容

---

*继续查看 Day 4 内容...*

---

# 📖 Day 4 - MySQL 8.0 角色功能

**日期:** 2026-03-11  
**学习时长:** 60 分钟

---

## 🎯 学习目标

1. 理解 MySQL 8.0 引入的角色功能
2. 掌握角色创建和分配
3. 理解角色嵌套
4. 掌握角色激活机制

---

## 📚 知识点讲解

### 4.1 MySQL 8.0 角色概述

MySQL 8.0 引入了真正的角色功能，类似于 PostgreSQL：

**主要特性:**
- ✅ 角色可以授予用户或其他角色 (角色嵌套)
- ✅ 角色默认不激活，需要显式激活
- ✅ 支持默认角色 (自动激活)
- ✅ 简化权限管理

---

### 4.2 创建和管理角色

**创建角色:**
```sql
-- 创建角色
CREATE ROLE 'read_only';
CREATE ROLE 'read_write';
CREATE ROLE 'admin';

-- 给角色授予权限
GRANT SELECT ON mydb.* TO 'read_only';
GRANT SELECT, INSERT, UPDATE, DELETE ON mydb.* TO 'read_write';
GRANT ALL PRIVILEGES ON mydb.* TO 'admin';
```

**授予角色给用户:**
```sql
-- 创建用户
CREATE USER 'alice'@'localhost' IDENTIFIED BY 'AlicePass!';

-- 授予角色
GRANT 'read_only'@'%' TO 'alice'@'localhost';

-- 授予多个角色
GRANT 'read_only'@'%', 'read_write'@'%' TO 'bob'@'localhost';
```

**角色嵌套 (角色授予角色):**
```sql
-- 创建角色层次
CREATE ROLE 'base';
CREATE ROLE 'intermediate';
CREATE ROLE 'advanced';

-- 角色嵌套
GRANT 'base' TO 'intermediate';
GRANT 'intermediate' TO 'advanced';

-- advanced 继承 base 和 intermediate 的权限
```

---

### 4.3 角色激活

**重要:** 授予角色的权限默认**不激活**，需要显式激活！

**激活方式:**
```sql
-- 1. 会话中激活角色
SET ROLE 'read_only'@'%';
SET ROLE 'read_write'@'%';
SET ROLE ALL;  -- 激活所有授予的角色
SET ROLE NONE; -- 停用所有角色

-- 2. 设置默认角色 (自动激活)
SET DEFAULT ROLE 'read_only'@'%' TO 'alice'@'localhost';
SET DEFAULT ROLE ALL TO 'bob'@'localhost';

-- 3. 查看当前激活的角色
SELECT CURRENT_ROLE();
```

**角色激活流程:**
```
用户登录
    ↓
检查默认角色 (SET DEFAULT ROLE)
    ↓
自动激活默认角色
    ↓
会话中可手动激活/切换角色 (SET ROLE)
```

---

### 4.4 查看角色信息

```sql
-- 查看用户被授予的角色
SELECT * FROM mysql.role_edges WHERE TO_USER = 'alice';

-- 查看角色的权限
SHOW GRANTS FOR 'read_only'@'%';

-- 查看用户的权限 (包括角色)
SHOW GRANTS FOR 'alice'@'localhost';

-- 查看用户的默认角色
SELECT * FROM mysql.default_roles WHERE USER = 'alice';
```

---

### 4.5 删除角色

```sql
-- 删除角色
DROP ROLE 'role_name';

-- 从用户撤销角色
REVOKE 'role_name'@'%' FROM 'user'@'localhost';
```

---

## 💻 实践练习

```sql
-- 1. 创建角色体系
CREATE ROLE 'app_read';
CREATE ROLE 'app_write';
CREATE ROLE 'app_admin';

GRANT SELECT ON mydb.* TO 'app_read';
GRANT SELECT, INSERT, UPDATE, DELETE ON mydb.* TO 'app_write';
GRANT ALL PRIVILEGES ON mydb.* TO 'app_admin';

-- 2. 角色嵌套
GRANT 'app_read' TO 'app_write';
GRANT 'app_write' TO 'app_admin';

-- 3. 创建用户并分配角色
CREATE USER 'dev1'@'localhost' IDENTIFIED BY 'Dev1Pass!';
GRANT 'app_write' TO 'dev1'@'localhost';

-- 4. 设置默认角色
SET DEFAULT ROLE 'app_write'@'%' TO 'dev1'@'localhost';

-- 5. 验证
SHOW GRANTS FOR 'dev1'@'localhost';
```

---

## 📝 今日测验 (5 题)

**1.** MySQL 8.0 中，关于角色的说法正确的是？
- A. 角色只能授予用户，不能授予其他角色
- B. 角色可以嵌套，角色可以授予其他角色
- C. 角色不能有密码
- D. 角色创建后自动激活

**2.** 授予角色给用户后，权限何时生效？
- A. 立即生效
- B. 需要用户重新登录
- C. 需要激活角色 (SET ROLE 或默认角色)
- D. 需要 FLUSH PRIVILEGES

**3.** 设置默认角色的命令是？
- A. SET DEFAULT ROLE
- B. SET AUTO ROLE
- C. CREATE DEFAULT ROLE
- D. ASSIGN ROLE

**4.** 查看当前激活的角色，使用？
- A. SELECT CURRENT_ROLE()
- B. SELECT ACTIVE_ROLE()
- C. SHOW ACTIVE ROLES
- D. SELECT @@role

**5.** 停用所有角色的命令是？
- A. SET ROLE NONE
- B. SET ROLE OFF
- C. DEACTIVATE ROLE
- D. DROP ROLE ALL

---

## ✅ 今日检查清单

- [ ] 阅读完所有知识点讲解
- [ ] 完成实践练习
- [ ] 完成今日测验 (目标：5/5)
- [ ] 复习 Day 1-3 内容

---

*继续查看 Day 5 内容...*

---

# 📖 Day 5 - 列级权限与视图

**日期:** 2026-03-12  
**学习时长:** 60 分钟

---

## 🎯 学习目标

1. 理解列级权限的概念
2. 掌握使用视图实现列级权限
3. 了解标准 SQL 的列级权限支持
4. 掌握实际应用场景

---

## 📚 知识点讲解

### 5.1 列级权限概念

**问题:** 如何只允许用户访问表中的部分列？

**场景示例:**
```
employees 表:
- id (员工 ID)
- name (姓名)
- department (部门)
- salary (薪资) ← 敏感数据，需要限制访问
- ssn (社保号)  ← 敏感数据，需要限制访问
```

**需求:** HR 可以看到所有列，普通经理只能看到 id、name、department

---

### 5.2 标准 SQL 的列级权限

**⚠️ 重要:** 标准 SQL **不支持** `GRANT SELECT(column) ON table` 语法！

虽然某些数据库 (如 Oracle) 支持列级 GRANT，但 MySQL 和 PostgreSQL 不直接支持。

**解决方案:** 使用**视图 (View)** 实现列级权限控制

---

### 5.3 使用视图实现列级权限

**步骤:**

```sql
-- 1. 创建基础表
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    ssn VARCHAR(20)
);

-- 2. 创建视图 (只暴露非敏感列)
CREATE VIEW employees_public AS
SELECT id, name, department
FROM employees;

-- 3. 授予视图权限
GRANT SELECT ON employees_public TO 'manager'@'localhost';

-- 4. 授予原表权限 (HR 专用)
GRANT SELECT ON employees TO 'hr'@'localhost';
```

**效果:**
- `manager` 用户只能看到 id、name、department
- `hr` 用户可以看到所有列 (包括 salary、ssn)

---

### 5.4 视图权限原理

```
┌─────────────────────────────────────┐
│  employees 表 (全量数据)             │
│  id | name | department | salary    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  employees_public 视图               │
│  (只暴露 id, name, department)      │
└─────────────────────────────────────┘
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
manager 用户          hr 用户
(只能访问视图)        (可访问原表)
```

---

### 5.5 实际应用场景

**场景 1: 客户信息脱敏**
```sql
-- 创建脱敏视图
CREATE VIEW customers_safe AS
SELECT 
    id,
    name,
    city,
    CONCAT(SUBSTRING(phone, 1, 3), '****') AS phone_masked
FROM customers;

GRANT SELECT ON customers_safe TO 'support'@'localhost';
```

**场景 2: 财务数据分级**
```sql
-- 基础视图 (所有员工)
CREATE VIEW budget_summary AS
SELECT department, total_budget
FROM budgets;

-- 详细视图 (管理层)
CREATE VIEW budget_detail AS
SELECT department, total_budget, actual_spend, variance
FROM budgets;

GRANT SELECT ON budget_summary TO 'all_staff';
GRANT SELECT ON budget_detail TO 'managers';
```

---

## 💻 实践练习

```sql
-- 1. 创建测试表
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    password_hash VARCHAR(255),
    created_at TIMESTAMP
);

-- 2. 创建公开视图 (不包含密码)
CREATE VIEW users_public AS
SELECT id, username, email, created_at
FROM users;

-- 3. 创建用户并授权
CREATE USER 'app'@'localhost' IDENTIFIED BY 'AppPass!';
GRANT SELECT ON users_public TO 'app'@'localhost';

-- 4. 验证
-- 使用 app 用户连接，尝试访问 users 表和 users_public 视图
```

---

## 📝 今日测验 (5 题)

**1.** 实现列级别权限控制的标准方法是？
- A. GRANT SELECT(column) ON table
- B. 创建视图只包含允许的列
- C. 使用 TDE 加密
- D. 无法实现列级别权限

**2.** 关于 SQL 列级权限，以下说法正确的是？
- A. 所有数据库都支持 GRANT SELECT(col)
- B. 标准 SQL 不支持列级 GRANT
- C. MySQL 完全支持列级权限
- D. PostgreSQL 完全支持列级权限

**3.** 使用视图实现列级权限的优点是？
- A. 性能更好
- B. 兼容性好，所有数据库都支持
- C. 不需要额外存储空间
- D. 自动更新数据

**4.** 客户信息脱敏场景，应该使用？
- A. 直接授予原表权限
- B. 创建脱敏视图
- C. 使用存储过程
- D. 应用层处理

**5.** 视图权限控制的核心思想是？
- A. 加密敏感数据
- B. 通过视图限制暴露的列
- C. 使用触发器拦截
- D. 审计所有访问

---

## ✅ 今日检查清单

- [ ] 阅读完所有知识点讲解
- [ ] 完成实践练习
- [ ] 完成今日测验 (目标：5/5)
- [ ] 复习 Day 1-4 内容

---

*继续查看 Day 6 内容...*

---

# 📖 Day 6 - SQL 注入防护

**日期:** 2026-03-13  
**学习时长:** 60 分钟

---

## 🎯 学习目标

1. 理解 SQL 注入原理
2. 掌握参数化查询
3. 了解其他防护措施
4. 能够识别和避免注入漏洞

---

## 📚 知识点讲解

### 6.1 SQL 注入原理

**什么是 SQL 注入？**
> 攻击者通过在输入中插入恶意 SQL 代码，改变原有 SQL 语义，从而执行未授权操作。

**经典示例:**
```python
# ❌ 危险代码 - 字符串拼接
username = input("用户名：")
password = input("密码：")

sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
# 输入：admin' --
# 生成：SELECT * FROM users WHERE username='admin' --' AND password=''
# 结果：绕过密码验证！
```

---

### 6.2 参数化查询 (Prepared Statements)

**最有效防护方法:**

**Python (mysql-connector):**
```python
# ✅ 安全代码 - 参数化查询
cursor.execute(
    "SELECT * FROM users WHERE username=%s AND password=%s",
    (username, password)
)
```

**Python (psycopg2 - PostgreSQL):**
```python
cursor.execute(
    "SELECT * FROM users WHERE username=%s AND password=%s",
    (username, password)
)
```

**原理:**
```
参数化查询将 SQL 代码和数据分离：
1. 先编译 SQL 模板 (确定语义)
2. 再绑定参数值 (仅作为数据处理)
3. 攻击者输入无法改变 SQL 语义
```

---

### 6.3 其他防护措施

| 措施 | 说明 | 效果 |
|------|------|------|
| 参数化查询 | 分离代码和数据 | ⭐⭐⭐⭐⭐ 最有效 |
| 输入验证 | 检查输入格式和范围 | ⭐⭐⭐⭐ 辅助防护 |
| 最小权限 | 数据库账户权限最小化 | ⭐⭐⭐⭐ 减少损失 |
| 存储过程 | 封装 SQL 逻辑 | ⭐⭐⭐ 仍有风险 |
| ORM 框架 | 自动参数化 | ⭐⭐⭐⭐ 推荐使用 |
| 过滤字符 | 转义特殊字符 | ⭐⭐ 不可靠 |

**⚠️ 注意:** 过滤特殊字符**不可靠**，因为：
- 编码绕过 (URL 编码、Unicode 等)
- 上下文相关 (数字不需要引号)
- 维护困难

---

### 6.4 常见注入类型

**1. 布尔盲注:**
```sql
-- 判断第一个字符是否为'a'
SELECT * FROM users WHERE id=1 AND SUBSTRING(password,1,1)='a'
```

**2. 时间盲注:**
```sql
-- 如果条件成立，延迟 5 秒
SELECT * FROM users WHERE id=1 AND SLEEP(5)
```

**3. UNION 注入:**
```sql
-- 合并查询结果
SELECT id, name FROM products WHERE id=1 
UNION 
SELECT username, password FROM users
```

---

### 6.5 安全编码实践

**Python 示例:**
```python
# ✅ 安全：参数化查询
def get_user(username):
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    return cursor.fetchone()

# ✅ 安全：ORM (SQLAlchemy)
user = session.query(User).filter(User.username == username).first()

# ❌ 危险：字符串拼接
def get_user_unsafe(username):
    sql = f"SELECT * FROM users WHERE username='{username}'"
    cursor.execute(sql)
    return cursor.fetchone()

# ❌ 危险：format 格式化
def get_user_unsafe2(username):
    sql = "SELECT * FROM users WHERE username='{}'".format(username)
    cursor.execute(sql)
    return cursor.fetchone()
```

---

## 💻 实践练习

```python
# 练习 1: 安全登录
def login_safe(username, password):
    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password_hash=%s",
        (username, hashlib.sha256(password.encode()).hexdigest())
    )
    return cursor.fetchone()

# 练习 2: 安全搜索
def search_products(keyword, category):
    cursor.execute(
        "SELECT * FROM products WHERE name LIKE %s AND category=%s",
        (f'%{keyword}%', category)
    )
    return cursor.fetchall()

# 练习 3: 安全分页
def get_users_page(page, page_size):
    offset = (page - 1) * page_size
    # 注意：LIMIT/OFFSET 参数需要特殊处理
    cursor.execute(
        "SELECT * FROM users LIMIT %s OFFSET %s",
        (page_size, offset)
    )
    return cursor.fetchall()
```

---

## 📝 今日测验 (5 题)

**1.** 防止 SQL 注入最有效的方法是？
- A. 过滤特殊字符
- B. 使用参数化查询 (Prepared Statements)
- C. 限制查询结果数量
- D. 使用存储过程

**2.** 以下 Python 代码是否安全？
```python
cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
```
- A. 安全，user_id 是数字
- B. 不安全，应该用参数化
- C. 安全，使用了 execute
- D. 不安全，应该用存储过程

**3.** 参数化查询的原理是？
- A. 过滤特殊字符
- B. 加密用户输入
- C. 分离 SQL 代码和数据
- D. 限制输入长度

**4.** 以下哪种输入可能构成 SQL 注入？
- A. `admin`
- B. `admin' --`
- C. `123456`
- D. `user@example.com`

**5.** ORM 框架 (如 SQLAlchemy) 为什么相对安全？
- A. 自动过滤所有输入
- B. 自动使用参数化查询
- C. 禁止执行原生 SQL
- D. 有防火墙保护

---

## ✅ 今日检查清单

- [ ] 阅读完所有知识点讲解
- [ ] 完成实践练习
- [ ] 完成今日测验 (目标：5/5)
- [ ] 复习 Day 1-5 内容

---

*继续查看 Day 7 内容...*

---

# 📖 Day 7 - 综合复习与测评

**日期:** 2026-03-14  
**学习时长:** 90 分钟

---

## 🎯 今日目标

1. 复习 Day 1-6 所有知识点
2. 完成综合测评 (20 题)
3. 分析薄弱环节
4. 制定后续学习计划

---

## 📚 知识点回顾

### Day 1: SQL 权限基础
- ✅ GRANT 语法：`GRANT 权限 ON 对象 TO 用户`
- ✅ REVOKE 语法：`REVOKE 权限 ON 对象 FROM 用户`
- ✅ 权限层次：全局 → 数据库 → 表 → 列

### Day 2: MySQL 用户与权限
- ✅ 权限表：user, db, tablespriv, columnspriv
- ✅ 用户管理：CREATE USER, DROP USER
- ✅ 查看权限：SHOW GRANTS

### Day 3: PostgreSQL 角色系统
- ✅ 用户 = 带 LOGIN 权限的角色
- ✅ 角色继承：GRANT role TO role
- ✅ 角色属性：LOGIN, SUPERUSER, CREATEDB

### Day 4: MySQL 8.0 角色
- ✅ 角色可以嵌套
- ✅ 角色需要激活 (SET ROLE)
- ✅ 默认角色 (SET DEFAULT ROLE)

### Day 5: 列级权限与视图
- ✅ 标准 SQL 不支持列级 GRANT
- ✅ 使用视图实现列级权限
- ✅ 数据脱敏场景

### Day 6: SQL 注入防护
- ✅ 参数化查询最有效
- ✅ 避免字符串拼接
- ✅ ORM 自动参数化

---

## 📝 综合测评 (20 题)

**准备就绪后，回复"开始测评"，我将为你生成 20 道综合测试题！**

---

## 📊 预期目标

| 指标 | 当前 | 目标 |
|------|------|------|
| 权限管理 | 20% | 80%+ |
| 安全管理 | 75% | 90%+ |
| 整体等级 | L2 (50 分) | L3 (75+ 分) |

---

## 🎯 后续计划

**如果达到目标 (75+ 分):**
- ✅ 进入备份管理进阶学习
- ✅ 学习性能优化
- ✅ 实战项目练习

**如果未达目标:**
- 📖 针对性复习薄弱环节
- 📖 额外练习题目
- 📖 延长学习周期

---

**祝你学习顺利！有任何问题随时提问！** 📚✨

