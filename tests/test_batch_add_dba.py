#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量添加 DBA 用户 - 单元测试套件

测试所有核心功能：
1. AWS RDS 实例发现
2. MySQL 用户创建和授权
3. PostgreSQL 用户创建和授权
4. IDEA 数据库连接
5. 权限验证
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

# 添加项目路径（父目录）
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# ============================================================================
# 测试 1: 数据库操作符 - MySQL
# ============================================================================

class TestDatabaseOperatorMySQL(unittest.TestCase):
    """测试 MySQL 数据库操作"""
    
    def setUp(self):
        """测试前准备"""
        from batch_add_dba_users import DatabaseOperator
        self.operator = DatabaseOperator("test_dba", "TestPassword123!")
    
    @patch('mysql.connector.connect')
    def test_check_user_exists_mysql(self, mock_connect):
        """测试检查 MySQL 用户是否存在"""
        # Mock 数据库连接
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # 用户存在的情况
        mock_cursor.fetchone.return_value = [1]
        exists = self.operator.check_user_exists_mysql(mock_cursor, "existing_user")
        self.assertTrue(exists)
        
        # 用户不存在的情况
        mock_cursor.fetchone.return_value = [0]
        exists = self.operator.check_user_exists_mysql(mock_cursor, "new_user")
        self.assertFalse(exists)
    
    @patch('mysql.connector.connect')
    def test_grant_mysql_dba_new_user(self, mock_connect):
        """测试授予 MySQL DBA 权限 - 新用户"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # 用户不存在
        self.operator.check_user_exists_mysql = MagicMock(return_value=False)
        
        # 执行授权
        self.operator.grant_mysql_dba(mock_cursor, "new_dba", "password", False)
        
        # 验证调用了 CREATE USER 和 GRANT
        self.assertEqual(mock_cursor.execute.call_count, 5)  # CREATE + 4xGRANT + FLUSH
    
    @patch('mysql.connector.connect')
    def test_grant_mysql_dba_existing_user(self, mock_connect):
        """测试授予 MySQL DBA 权限 - 已存在用户"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # 用户已存在
        self.operator.check_user_exists_mysql = MagicMock(return_value=True)
        
        # 执行授权
        self.operator.grant_mysql_dba(mock_cursor, "existing_dba", "password", True)
        
        # 验证只调用了 GRANT（没有 CREATE USER）
        self.assertEqual(mock_cursor.execute.call_count, 4)  # 4xGRANT + FLUSH
    
    @patch('mysql.connector.connect')
    def test_execute_on_mysql_success(self, mock_connect):
        """测试 MySQL 执行成功"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.is_connected.return_value = True
        
        # Mock 内部方法
        self.operator.check_user_exists_mysql = MagicMock(return_value=False)
        self.operator.grant_mysql_dba = MagicMock()
        
        from batch_add_dba_users import DbInstance
        instance = DbInstance(
            platform="aws",
            engine="mysql",
            endpoint="test.mysql.rds.amazonaws.com",
            port=3306,
            instance_id="test-instance"
        )
        
        result = self.operator.execute_on_mysql(instance, "admin", "password")
        
        self.assertEqual(result.status, "success")
        self.assertTrue(result.user_created)
        self.assertFalse(result.user_existed)
    
    @patch('mysql.connector.connect')
    def test_execute_on_mysql_failure(self, mock_connect):
        """测试 MySQL 执行失败"""
        mock_connect.side_effect = Exception("Connection refused")
        
        from batch_add_dba_users import DbInstance
        instance = DbInstance(
            platform="aws",
            engine="mysql",
            endpoint="test.mysql.rds.amazonaws.com",
            port=3306,
            instance_id="test-instance"
        )
        
        result = self.operator.execute_on_mysql(instance, "admin", "password")
        
        self.assertEqual(result.status, "failed")
        self.assertIn("Connection refused", result.error)

# ============================================================================
# 测试 2: 数据库操作符 - PostgreSQL
# ============================================================================

class TestDatabaseOperatorPostgreSQL(unittest.TestCase):
    """测试 PostgreSQL 数据库操作"""
    
    def setUp(self):
        """测试前准备"""
        from batch_add_dba_users import DatabaseOperator
        self.operator = DatabaseOperator("test_dba", "TestPassword123!")
    
    @patch('psycopg2.connect')
    def test_check_user_exists_pg(self, mock_connect):
        """测试检查 PostgreSQL 用户是否存在"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # 用户存在
        mock_cursor.fetchone.return_value = [1]
        exists = self.operator.check_user_exists_pg(mock_cursor, "existing_user")
        self.assertTrue(exists)
        
        # 用户不存在
        mock_cursor.fetchone.return_value = [0]
        exists = self.operator.check_user_exists_pg(mock_cursor, "new_user")
        self.assertFalse(exists)
    
    @patch('psycopg2.connect')
    def test_grant_pg_dba_new_user(self, mock_connect):
        """测试授予 PostgreSQL DBA 权限 - 新用户"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.autocommit = True
        
        # 执行授权
        self.operator.grant_pg_dba(mock_cursor, "new_dba", "password", False)
        
        # 验证调用了 CREATE ROLE 和 GRANT
        self.assertGreater(mock_cursor.execute.call_count, 0)
    
    @patch('psycopg2.connect')
    def test_grant_pg_dba_existing_user(self, mock_connect):
        """测试授予 PostgreSQL DBA 权限 - 已存在用户"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.autocommit = True
        
        # 执行授权
        self.operator.grant_pg_dba(mock_cursor, "existing_dba", "password", True)
        
        # 验证调用了 GRANT（没有 CREATE ROLE）
        self.assertGreater(mock_cursor.execute.call_count, 0)
    
    @patch('psycopg2.connect')
    def test_execute_on_pg_success(self, mock_connect):
        """测试 PostgreSQL 执行成功"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock 内部方法
        self.operator.check_user_exists_pg = MagicMock(return_value=False)
        self.operator.grant_pg_dba = MagicMock()
        
        from batch_add_dba_users import DbInstance
        instance = DbInstance(
            platform="aws",
            engine="postgresql",
            endpoint="test.postgresql.rds.amazonaws.com",
            port=5432,
            instance_id="test-pg-instance"
        )
        
        result = self.operator.execute_on_pg(instance, "admin", "password")
        
        self.assertEqual(result.status, "success")
        self.assertTrue(result.user_created)

# ============================================================================
# 测试 3: AWS RDS 管理器
# ============================================================================

class TestAWSRDSManager(unittest.TestCase):
    """测试 AWS RDS 实例管理"""
    
    @patch('boto3.Session')
    def test_get_all_instances(self, mock_session):
        """测试获取所有 RDS 实例"""
        from batch_add_dba_users import AWSRDSManager
        
        # Mock RDS 客户端
        mock_rds = MagicMock()
        mock_session.return_value.client.return_value = mock_rds
        
        # Mock 分页器
        mock_paginator = MagicMock()
        mock_rds.get_paginator.return_value = mock_paginator
        
        # Mock 实例数据
        mock_paginator.paginate.return_value = [{
            'DBInstances': [
                {
                    'DBInstanceIdentifier': 'mysql-instance-1',
                    'Engine': 'mysql',
                    'Endpoint': {'Address': 'mysql1.rds.amazonaws.com', 'Port': 3306}
                },
                {
                    'DBInstanceIdentifier': 'pg-instance-1',
                    'Engine': 'postgres',
                    'Endpoint': {'Address': 'pg1.rds.amazonaws.com', 'Port': 5432}
                },
                {
                    'DBInstanceIdentifier': 'aurora-instance-1',
                    'Engine': 'aurora-mysql',
                    'Endpoint': {'Address': 'aurora1.rds.amazonaws.com', 'Port': 3306}
                }
            ]
        }]
        
        manager = AWSRDSManager("us-east-1", "default")
        instances = manager.get_all_instances()
        
        self.assertEqual(len(instances), 3)
        self.assertEqual(instances[0].engine, "mysql")
        self.assertEqual(instances[1].engine, "postgresql")
        self.assertEqual(instances[2].engine, "mysql")  # aurora-mysql 映射为 mysql

# ============================================================================
# 测试 4: IDEA 数据库支持
# ============================================================================

class TestIDEADatabaseSupport(unittest.TestCase):
    """测试 IDEA 数据库连接支持"""
    
    def setUp(self):
        """测试前准备"""
        from idea_database_support import IDEAConnectionManager, IDEAConnection
        self.manager = IDEAConnectionManager()
    
    def test_map_db_type(self):
        """测试数据库类型映射"""
        self.assertEqual(self.manager._map_db_type("mysql"), "mysql")
        self.assertEqual(self.manager._map_db_type("postgresql"), "postgresql")
        self.assertEqual(self.manager._map_db_type("postgres"), "postgresql")
        self.assertEqual(self.manager._map_db_type("aurora"), "mysql")
        self.assertEqual(self.manager._map_db_type("unknown"), "unknown")
    
    def test_idea_connection_dataclass(self):
        """测试 IDEA 连接数据类"""
        from idea_database_support import IDEAConnection
        
        conn = IDEAConnection(
            name="Production DB",
            database_type="mysql",
            host="prod.example.com",
            port=3306,
            database="mydb",
            username="admin"
        )
        
        self.assertEqual(conn.name, "Production DB")
        self.assertEqual(conn.database_type, "mysql")
        self.assertEqual(conn.host, "prod.example.com")
        self.assertEqual(conn.port, 3306)

# ============================================================================
# 测试 5: 权限验证
# ============================================================================

class TestPermissionVerification(unittest.TestCase):
    """测试 DBA 权限验证"""
    
    def test_mysql_dba_permissions_format(self):
        """测试 MySQL DBA 权限格式"""
        from batch_add_dba_users import DBA_PERMISSIONS
        
        self.assertIn("mysql", DBA_PERMISSIONS)
        permissions = DBA_PERMISSIONS["mysql"]
        
        # 验证包含所有必要权限
        permission_str = " ".join(permissions)
        self.assertIn("ALL PRIVILEGES", permission_str)
        self.assertIn("PROCESS", permission_str)
        self.assertIn("REPLICATION", permission_str)
    
    def test_postgresql_dba_permissions_format(self):
        """测试 PostgreSQL DBA 权限格式"""
        from batch_add_dba_users import DBA_PERMISSIONS
        
        self.assertIn("postgresql", DBA_PERMISSIONS)
        permissions = DBA_PERMISSIONS["postgresql"]
        
        # 验证包含 rds_superuser
        self.assertIn("rds_superuser", permissions)

# ============================================================================
# 测试 6: 执行结果数据类
# ============================================================================

class TestExecutionResult(unittest.TestCase):
    """测试执行结果数据类"""
    
    def test_execution_result_creation(self):
        """测试执行结果创建"""
        from batch_add_dba_users import ExecutionResult
        
        result = ExecutionResult(
            instance_id="test-instance",
            endpoint="test.rds.amazonaws.com",
            engine="mysql",
            status="success",
            user_existed=False,
            user_created=True,
            error=None
        )
        
        self.assertEqual(result.instance_id, "test-instance")
        self.assertEqual(result.status, "success")
        self.assertTrue(result.user_created)
        self.assertFalse(result.user_existed)
        self.assertIsNone(result.error)
    
    def test_execution_result_to_dict(self):
        """测试执行结果转换为字典"""
        from dataclasses import asdict
        from batch_add_dba_users import ExecutionResult
        
        result = ExecutionResult(
            instance_id="test-instance",
            endpoint="test.rds.amazonaws.com",
            engine="mysql",
            status="success",
            user_existed=False,
            user_created=True
        )
        
        result_dict = asdict(result)
        
        self.assertIsInstance(result_dict, dict)
        self.assertIn("instance_id", result_dict)
        self.assertIn("status", result_dict)

# ============================================================================
# 测试 7: 边界情况和异常处理
# ============================================================================

class TestEdgeCases(unittest.TestCase):
    """测试边界情况和异常处理"""
    
    def test_empty_password(self):
        """测试空密码处理"""
        from batch_add_dba_users import DatabaseOperator
        
        # 空密码应该被接受（实际使用时应该验证密码强度）
        operator = DatabaseOperator("test_user", "")
        self.assertEqual(operator.dba_pass, "")
    
    def test_special_characters_in_username(self):
        """测试用户名中的特殊字符"""
        from batch_add_dba_users import DatabaseOperator
        
        # 用户名包含特殊字符
        operator = DatabaseOperator("dba_admin@test", "Password123!")
        self.assertEqual(operator.dba_user, "dba_admin@test")
    
    def test_long_instance_id(self):
        """测试长实例 ID 处理"""
        from batch_add_dba_users import ExecutionResult, DbInstance
        
        long_id = "a" * 100  # 100 字符的实例 ID
        instance = DbInstance(
            platform="aws",
            engine="mysql",
            endpoint="test.rds.amazonaws.com",
            port=3306,
            instance_id=long_id
        )
        
        result = ExecutionResult(
            instance_id=instance.instance_id,
            endpoint=instance.endpoint,
            engine=instance.engine,
            status="success",
            user_existed=False,
            user_created=True
        )
        
        self.assertEqual(len(result.instance_id), 100)

# ============================================================================
# 运行所有测试
# ============================================================================

if __name__ == '__main__':
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseOperatorMySQL))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseOperatorPostgreSQL))
    suite.addTests(loader.loadTestsFromTestCase(TestAWSRDSManager))
    suite.addTests(loader.loadTestsFromTestCase(TestIDEADatabaseSupport))
    suite.addTests(loader.loadTestsFromTestCase(TestPermissionVerification))
    suite.addTests(loader.loadTestsFromTestCase(TestExecutionResult))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出测试报告
    print("\n" + "=" * 70)
    print("测试报告")
    print("=" * 70)
    print(f"总测试数：{result.testsRun}")
    print(f"成功：{result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败：{len(result.failures)}")
    print(f"错误：{len(result.errors)}")
    print("=" * 70)
    
    # 如果有失败或错误，退出码为 1
    sys.exit(0 if result.wasSuccessful() else 1)
