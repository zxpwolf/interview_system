#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量添加 DBA 用户 - Excel 导入模式
从 Excel 文件读取数据库连接信息，支持 MySQL 和 PostgreSQL
"""

import mysql.connector
import psycopg2
import logging
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

# ==================== 配置区域 ====================

# Excel 文件路径
EXCEL_FILE = "databases.xlsx"  # 修改为你的 Excel 文件路径

# DBA 权限配置
DBA_PERMISSIONS = {
    "mysql": [
        "ALL PRIVILEGES ON *.*",
        "PROCESS",
        "REPLICATION CLIENT",
        "REPLICATION SLAVE",
    ],
    "postgresql": [
        "rds_superuser",
    ]
}

# 日志配置
LOG_FILE = f"dba-batch-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
REPORT_FILE = f"dba-batch-{datetime.now().strftime('%Y%m%d-%H%M%S')}-report.json"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==================== 数据结构 ====================

@dataclass
class DbInstance:
    platform: str
    engine: str
    endpoint: str
    port: int
    instance_id: str

@dataclass
class ExecutionResult:
    instance_id: str
    endpoint: str
    engine: str
    status: str
    user_existed: bool
    user_created: bool
    error: Optional[str] = None

# ==================== 数据库操作 ====================

class DatabaseOperator:
    def __init__(self, dba_user: str, dba_pass: str):
        self.dba_user = dba_user
        self.dba_pass = dba_pass
    
    def check_user_exists_mysql(self, cursor, username: str) -> bool:
        cursor.execute("SELECT COUNT(*) FROM mysql.user WHERE User = %s", (username,))
        return cursor.fetchone()[0] > 0
    
    def check_user_exists_pg(self, cursor, username: str) -> bool:
        cursor.execute("SELECT COUNT(*) FROM pg_catalog.pg_roles WHERE rolname = %s", (username,))
        return cursor.fetchone()[0] > 0
    
    def grant_mysql_dba(self, cursor, username: str, password: str, user_exists: bool):
        if not user_exists:
            cursor.execute(f"CREATE USER '{username}'@'%' IDENTIFIED BY '{password}'")
            logger.info(f"  ✓ 创建用户：{username}")
        
        logger.info(f"  → 授予 DBA 权限:")
        cursor.execute(f"GRANT ALL PRIVILEGES ON *.* TO '{username}'@'%' WITH GRANT OPTION")
        logger.info(f"    - ALL PRIVILEGES ON *.* (WITH GRANT OPTION)")
        cursor.execute(f"GRANT PROCESS ON *.* TO '{username}'@'%'")
        logger.info(f"    - PROCESS")
        cursor.execute(f"GRANT REPLICATION CLIENT ON *.* TO '{username}'@'%'")
        logger.info(f"    - REPLICATION CLIENT")
        cursor.execute(f"GRANT REPLICATION SLAVE ON *.* TO '{username}'@'%'")
        logger.info(f"    - REPLICATION SLAVE")
        cursor.execute("FLUSH PRIVILEGES")
        logger.info(f"  ✓ 权限授予完成")
    
    def grant_pg_dba(self, cursor, username: str, password: str, user_exists: bool):
        if not user_exists:
            cursor.execute(f"CREATE ROLE {username} WITH LOGIN PASSWORD '{password}'")
            logger.info(f"  ✓ 创建用户：{username}")
        
        logger.info(f"  → 授予 DBA 权限:")
        cursor.execute(f"GRANT rds_superuser TO {username}")
        logger.info(f"    - rds_superuser")
        cursor.execute(f"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {username}")
        cursor.execute(f"GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO {username}")
        cursor.execute(f"GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO {username}")
        cursor.execute(f"ALTER ROLE {username} SET search_path TO public")
        logger.info(f"    - ALL PRIVILEGES ON SCHEMA public")
        logger.info(f"  ✓ 权限授予完成")
    
    def execute_on_mysql(self, instance: DbInstance, master_user: str, master_pass: str) -> ExecutionResult:
        conn = None
        try:
            conn = mysql.connector.connect(
                host=instance.endpoint,
                port=instance.port,
                user=master_user,
                password=master_pass,
                connect_timeout=10,
                ssl_disabled=True
            )
            cursor = conn.cursor()
            
            user_existed = self.check_user_exists_mysql(cursor, self.dba_user)
            self.grant_mysql_dba(cursor, self.dba_user, self.dba_pass, user_existed)
            
            conn.commit()
            
            return ExecutionResult(
                instance_id=instance.instance_id,
                endpoint=instance.endpoint,
                engine=instance.engine,
                status="success",
                user_existed=user_existed,
                user_created=not user_existed
            )
        
        except Exception as e:
            logger.error(f"MySQL {instance.instance_id} 失败：{str(e)}")
            return ExecutionResult(
                instance_id=instance.instance_id,
                endpoint=instance.endpoint,
                engine=instance.engine,
                status="failed",
                user_existed=False,
                user_created=False,
                error=str(e)
            )
        
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
    
    def execute_on_pg(self, instance: DbInstance, master_user: str, master_pass: str) -> ExecutionResult:
        conn = None
        try:
            conn = psycopg2.connect(
                host=instance.endpoint,
                port=instance.port,
                user=master_user,
                password=master_pass,
                connect_timeout=10,
                sslmode='disable'
            )
            conn.autocommit = True
            cursor = conn.cursor()
            
            user_existed = self.check_user_exists_pg(cursor, self.dba_user)
            self.grant_pg_dba(cursor, self.dba_user, self.dba_pass, user_existed)
            
            return ExecutionResult(
                instance_id=instance.instance_id,
                endpoint=instance.endpoint,
                engine=instance.engine,
                status="success",
                user_existed=user_existed,
                user_created=not user_existed
            )
        
        except Exception as e:
            logger.error(f"PostgreSQL {instance.instance_id} 失败：{str(e)}")
            return ExecutionResult(
                instance_id=instance.instance_id,
                endpoint=instance.endpoint,
                engine=instance.engine,
                status="failed",
                user_existed=False,
                user_created=False,
                error=str(e)
            )
        
        finally:
            if conn:
                cursor.close()
                conn.close()

# ==================== 主流程 ====================

def main():
    logger.info("=" * 60)
    logger.info("批量添加 DBA 用户 - Excel 导入模式")
    logger.info("=" * 60)
    
    # 读取 Excel 文件
    logger.info(f"\n正在读取 Excel 文件：{EXCEL_FILE}")
    
    try:
        from excel_database_reader import ExcelDatabaseReader
        reader = ExcelDatabaseReader(EXCEL_FILE)
        databases = reader.read_excel()
        
        if not databases:
            logger.error("Excel 文件中没有有效的数据库记录！")
            return
        
        # 打印摘要
        reader.print_summary()
        
        # 验证连接信息
        validation = reader.validate_connections()
        if validation["errors"]:
            logger.error(f"\n发现 {len(validation['errors'])} 个错误：")
            for error in validation["errors"][:5]:
                logger.error(f"  - {error}")
            if len(validation["errors"]) > 5:
                logger.error(f"  ... 还有 {len(validation['errors']) - 5} 个错误")
            return
        
        if validation["warnings"]:
            logger.warning(f"\n发现 {len(validation['warnings'])} 个警告：")
            for warning in validation["warnings"][:5]:
                logger.warning(f"  - {warning}")
            if len(validation["warnings"]) > 5:
                logger.warning(f"  ... 还有 {len(validation['warnings']) - 5} 个警告")
            logger.info("继续执行...")
        
    except FileNotFoundError:
        logger.error(f"Excel 文件不存在：{EXCEL_FILE}")
        logger.error("请创建 Excel 文件，包含以下列：")
        logger.error("  platform, database_type, name, host, port, username, password")
        logger.error("可选列：dba_username, dba_password, notes")
        return
    except Exception as e:
        logger.error(f"读取 Excel 文件失败：{str(e)}")
        return
    
    # 获取 DBA 用户信息
    use_excel_credentials = False
    dbs_with_dba_creds = [db for db in databases if db.dba_username and db.dba_password]
    
    if len(dbs_with_dba_creds) == len(databases) and len(databases) > 0:
        choice = input("\n所有数据库已在 Excel 中指定 DBA 凭证，是否使用？(y/n): ").strip().lower()
        if choice == 'y':
            use_excel_credentials = True
            logger.info("✓ 使用 Excel 中的 DBA 凭证")
    
    if not use_excel_credentials:
        logger.info("\n请输入要创建的 DBA 用户信息：")
        dba_user = input("DBA 用户名：").strip()
        
        if not dba_user:
            logger.error("用户名不能为空！")
            return
        
        import getpass
        dba_pass = getpass.getpass("DBA 密码（输入不显示）：")
        
        if not dba_pass:
            logger.error("密码不能为空！")
            return
        
        dba_pass_confirm = getpass.getpass("确认密码：")
        
        if dba_pass != dba_pass_confirm:
            logger.error("两次输入的密码不一致！")
            return
        
        logger.info(f"\n✓ 统一 DBA 用户：{dba_user}")
        logger.info(f"✓ 统一 DBA 密码：{'*' * len(dba_pass)}")
    
    # 按数据库类型分类
    mysql_dbs = [db for db in databases if db.database_type == 'mysql']
    pg_dbs = [db for db in databases if db.database_type == 'postgresql']
    
    logger.info(f"\n待处理数据库：{len(databases)} 个")
    logger.info(f"  - MySQL: {len(mysql_dbs)} 个")
    logger.info(f"  - PostgreSQL: {len(pg_dbs)} 个")
    logger.info("")
    
    results: List[ExecutionResult] = []
    
    # 处理 MySQL 数据库
    logger.info("=" * 60)
    logger.info("开始处理 MySQL 数据库")
    logger.info("=" * 60)
    
    for db_info in mysql_dbs:
        if use_excel_credentials and db_info.dba_username and db_info.dba_password:
            current_dba_user = db_info.dba_username
            current_dba_pass = db_info.dba_password
        else:
            current_dba_user = dba_user
            current_dba_pass = dba_pass
        
        db_op = DatabaseOperator(current_dba_user, current_dba_pass)
        
        instance = DbInstance(
            platform=db_info.platform,
            engine=db_info.database_type,
            endpoint=db_info.host,
            port=db_info.port,
            instance_id=db_info.name
        )
        
        logger.info(f"\n[{len(results)+1}/{len(mysql_dbs)}] 处理 MySQL: {db_info.name} ({db_info.host}:{db_info.port})")
        if db_info.notes:
            logger.info(f"  备注：{db_info.notes}")
        
        result = db_op.execute_on_mysql(instance, db_info.username, db_info.password)
        results.append(result)
        
        if result.status == "success":
            logger.info(f"✅ 数据库处理成功")
            if result.user_created:
                logger.info(f"  → 已创建 DBA 用户：{current_dba_user}")
            else:
                logger.info(f"  → DBA 用户已存在，权限已更新")
        else:
            logger.error(f"❌ 失败：{result.error}")
    
    # 处理 PostgreSQL 数据库
    logger.info("\n" + "=" * 60)
    logger.info("开始处理 PostgreSQL 数据库")
    logger.info("=" * 60)
    
    for db_info in pg_dbs:
        if use_excel_credentials and db_info.dba_username and db_info.dba_password:
            current_dba_user = db_info.dba_username
            current_dba_pass = db_info.dba_password
        else:
            current_dba_user = dba_user
            current_dba_pass = dba_pass
        
        db_op = DatabaseOperator(current_dba_user, current_dba_pass)
        
        instance = DbInstance(
            platform=db_info.platform,
            engine=db_info.database_type,
            endpoint=db_info.host,
            port=db_info.port,
            instance_id=db_info.name
        )
        
        logger.info(f"\n[{len(results)+1}/{len(pg_dbs)}] 处理 PostgreSQL: {db_info.name} ({db_info.host}:{db_info.port})")
        if db_info.notes:
            logger.info(f"  备注：{db_info.notes}")
        
        result = db_op.execute_on_pg(instance, db_info.username, db_info.password)
        results.append(result)
        
        if result.status == "success":
            logger.info(f"✅ 数据库处理成功")
            if result.user_created:
                logger.info(f"  → 已创建 DBA 用户：{current_dba_user}")
            else:
                logger.info(f"  → DBA 用户已存在，权限已更新")
        else:
            logger.error(f"❌ 失败：{result.error}")
    
    # 生成报告
    success_count = sum(1 for r in results if r.status == "success")
    failed_count = sum(1 for r in results if r.status == "failed")
    created_count = sum(1 for r in results if r.user_created)
    existed_count = sum(1 for r in results if r.user_existed)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "excel_file": EXCEL_FILE,
        "dba_user": dba_user if not use_excel_credentials else "from_excel",
        "summary": {
            "total_databases": len(results),
            "success": success_count,
            "failed": failed_count,
            "user_created": created_count,
            "user_existed": existed_count
        },
        "details": [asdict(r) for r in results]
    }
    
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    logger.info("\n" + "=" * 60)
    logger.info("执行完成！")
    logger.info(f"总计数据库：{len(results)} 个")
    logger.info(f"成功：{success_count} 个")
    logger.info(f"失败：{failed_count} 个")
    logger.info(f"新创建：{created_count} 个数据库")
    logger.info(f"已存在：{existed_count} 个数据库")
    logger.info(f"\n详细报告：{REPORT_FILE}")
    logger.info(f"日志文件：{LOG_FILE}")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
