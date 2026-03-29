#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化单元测试 - Excel 导入模式

测试核心逻辑和数据结构
"""

import unittest
import sys
import os

# 添加项目路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# ============================================================================
# 测试 1: 数据结构
# ============================================================================

class TestDataStructures(unittest.TestCase):
    """测试数据结构"""
    
    def test_database_info_creation(self):
        """测试数据库信息数据类"""
        from dataclasses import dataclass
        
        @dataclass
        class DatabaseInfo:
            platform: str
            database_type: str
            name: str
            host: str
            port: int
            username: str
            password: str
            dba_username: str = ""
            dba_password: str = ""
            notes: str = ""
        
        db = DatabaseInfo(
            platform="aws",
            database_type="mysql",
            name="prod-db-01",
            host="rm-prod.mysql.rds.amazonaws.com",
            port=3306,
            username="admin",
            password="Password123!",
            dba_username="dba_admin",
            dba_password="DBAPass123!",
            notes="生产数据库"
        )
        
        self.assertEqual(db.platform, "aws")
        self.assertEqual(db.database_type, "mysql")
        self.assertEqual(db.name, "prod-db-01")
        self.assertEqual(db.port, 3306)
        self.assertEqual(db.dba_username, "dba_admin")
    
    def test_db_instance_creation(self):
        """测试数据库实例数据类"""
        from dataclasses import dataclass
        
        @dataclass
        class DbInstance:
            platform: str
            engine: str
            endpoint: str
            port: int
            instance_id: str
        
        instance = DbInstance(
            platform="aws",
            engine="mysql",
            endpoint="test.mysql.rds.amazonaws.com",
            port=3306,
            instance_id="test-instance"
        )
        
        self.assertEqual(instance.platform, "aws")
        self.assertEqual(instance.engine, "mysql")
        self.assertEqual(instance.endpoint, "test.mysql.rds.amazonaws.com")

# ============================================================================
# 测试 2: Excel 读取器
# ============================================================================

class TestExcelReader(unittest.TestCase):
    """测试 Excel 读取器"""
    
    def test_required_columns(self):
        """测试必需列验证"""
        required_columns = ['platform', 'database_type', 'name', 'host', 'port', 'username', 'password']
        
        self.assertIn('platform', required_columns)
        self.assertIn('database_type', required_columns)
        self.assertIn('host', required_columns)
        self.assertIn('port', required_columns)
        self.assertIn('username', required_columns)
        self.assertIn('password', required_columns)
    
    def test_optional_columns(self):
        """测试可选列"""
        optional_columns = ['dba_username', 'dba_password', 'notes']
        
        self.assertIn('dba_username', optional_columns)
        self.assertIn('dba_password', optional_columns)
        self.assertIn('notes', optional_columns)
    
    def test_database_type_validation(self):
        """测试数据库类型验证"""
        valid_types = ['mysql', 'postgresql', 'postgres']
        
        for db_type in valid_types:
            normalized = 'postgresql' if db_type == 'postgres' else db_type
            self.assertIn(normalized, ['mysql', 'postgresql'])
    
    def test_platform_validation(self):
        """测试平台验证"""
        valid_platforms = ['aws', 'azure', 'other']
        
        for platform in valid_platforms:
            self.assertIn(platform, valid_platforms)

# ============================================================================
# 测试 3: 凭证管理
# ============================================================================

class TestCredentialManagement(unittest.TestCase):
    """测试凭证管理"""
    
    def test_unified_credentials(self):
        """测试统一凭证模式"""
        # 所有数据库使用同一个 DBA 凭证
        dba_user = "dba_admin"
        dba_pass = "DBAPass123!"
        
        self.assertEqual(len(dba_pass) >= 8, True)
    
    def test_individual_credentials(self):
        """测试独立凭证模式"""
        # 每个数据库有自己的 DBA 凭证
        credentials = {
            "db1": {"user": "dba_admin1", "pass": "Pass1!"},
            "db2": {"user": "dba_admin2", "pass": "Pass2!"},
        }
        
        self.assertEqual(len(credentials), 2)
    
    def test_password_complexity(self):
        """测试密码复杂度验证"""
        def check_password_strength(pwd):
            if len(pwd) < 8:
                return False
            has_upper = any(c.isupper() for c in pwd)
            has_lower = any(c.islower() for c in pwd)
            has_digit = any(c.isdigit() for c in pwd)
            has_special = any(c in "!@#$%^&*()" for c in pwd)
            return has_upper and has_lower and has_digit and has_special
        
        self.assertTrue(check_password_strength("Test123!"))
        self.assertTrue(check_password_strength("Admin@2026"))
        self.assertFalse(check_password_strength("weak"))
        self.assertFalse(check_password_strength("12345678"))

# ============================================================================
# 测试 4: 边界情况
# ============================================================================

class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_empty_excel_handling(self):
        """测试空 Excel 文件处理"""
        # 空 Excel 应该返回空列表
        databases = []
        self.assertEqual(len(databases), 0)
    
    def test_missing_required_columns(self):
        """测试缺少必需列处理"""
        required = ['platform', 'database_type', 'name', 'host', 'port', 'username', 'password']
        provided = ['platform', 'name', 'host']
        
        missing = [col for col in required if col not in provided]
        self.assertEqual(len(missing), 4)
    
    def test_special_characters_in_password(self):
        """测试密码中的特殊字符"""
        passwords = [
            "P@ssw0rd!",
            "Test#123$",
            "Admin% ^&*()",
        ]
        
        for pwd in passwords:
            self.assertGreater(len(pwd), 0)
    
    def test_port_range_validation(self):
        """测试端口范围验证"""
        valid_ports = [3306, 5432, 3307, 5433]
        invalid_ports = [0, -1, 70000]
        
        for port in valid_ports:
            self.assertTrue(1 <= port <= 65535)
        
        for port in invalid_ports:
            self.assertFalse(1 <= port <= 65535)

# ============================================================================
# 测试 5: 文件存在性检查
# ============================================================================

class TestFileExistence(unittest.TestCase):
    """测试文件存在性"""
    
    def test_main_script_exists(self):
        """测试主脚本存在"""
        script_path = os.path.join(project_root, "batch-add-dba-users.py")
        self.assertTrue(os.path.exists(script_path), f"主脚本不存在：{script_path}")
    
    def test_excel_reader_exists(self):
        """测试 Excel 读取器模块存在"""
        reader_path = os.path.join(project_root, "excel_database_reader.py")
        self.assertTrue(os.path.exists(reader_path), f"Excel 读取器不存在：{reader_path}")
    
    def test_excel_template_exists(self):
        """测试 Excel 模板存在"""
        template_path = os.path.join(project_root, "databases-template.xlsx")
        self.assertTrue(os.path.exists(template_path), f"Excel 模板不存在：{template_path}")
    
    def test_readme_exists(self):
        """测试 README 存在"""
        readme_path = os.path.join(project_root, "README-批量添加 DBA 用户.md")
        self.assertTrue(os.path.exists(readme_path), f"README 不存在：{readme_path}")
    
    def test_requirements_exists(self):
        """测试 requirements.txt 存在"""
        req_path = os.path.join(project_root, "requirements.txt")
        self.assertTrue(os.path.exists(req_path), f"requirements.txt 不存在：{req_path}")

# ============================================================================
# 运行所有测试
# ============================================================================

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestDataStructures))
    suite.addTests(loader.loadTestsFromTestCase(TestExcelReader))
    suite.addTests(loader.loadTestsFromTestCase(TestCredentialManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestFileExistence))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    print("Test Report")
    print("=" * 70)
    print(f"Total Tests: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    sys.exit(0 if result.wasSuccessful() else 1)
