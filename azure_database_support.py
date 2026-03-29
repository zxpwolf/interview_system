#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Azure Database 支持模块
支持 Azure Database for MySQL 和 Azure Database for PostgreSQL
"""

import logging
from typing import List, Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class AzureDbInstance:
    """Azure 数据库实例信息"""
    resource_group: str
    server_name: str
    database_type: str  # "mysql" or "postgresql"
    location: str
    version: str
    sku: str
    administrator_login: str
    fully_qualified_domain_name: str
    port: int
    ssl_enforcement: str

class AzureDatabaseManager:
    """
    Azure Database 管理器
    
    使用 Azure CLI 或 Azure SDK 管理 Azure Database for MySQL/PostgreSQL
    """
    
    def __init__(self, subscription_id: str = None):
        """
        初始化 Azure Database 管理器
        
        Args:
            subscription_id: Azure 订阅 ID（可选，如不传则使用当前登录的订阅）
        """
        self.subscription_id = subscription_id
        self.instances: List[AzureDbInstance] = []
    
    def _run_azure_cli(self, command: str) -> str:
        """运行 Azure CLI 命令"""
        import subprocess
        
        try:
            # 如果有订阅 ID，添加到命令
            if self.subscription_id:
                command = f"{command} --subscription {self.subscription_id}"
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                logger.error(f"Azure CLI 错误：{result.stderr}")
                raise Exception(f"Azure CLI 失败：{result.stderr}")
            
            return result.stdout
        
        except subprocess.TimeoutExpired:
            raise Exception("Azure CLI 命令超时")
        except FileNotFoundError:
            raise Exception("未找到 Azure CLI，请先安装：az cli")
    
    def list_all_servers(self) -> List[AzureDbInstance]:
        """
        列出所有 Azure Database 服务器
        
        Returns:
            AzureDbInstance 列表
        """
        logger.info("正在获取 Azure Database 服务器列表...")
        
        instances = []
        
        try:
            # 获取 MySQL 服务器
            mysql_output = self._run_azure_cli(
                "az mysql server list --query '[].{resourceGroup:resourceGroup,name:name,location:location,version:version,sku:sku.tier,administratorLogin:administratorLogin,fqdn:fullyQualifiedDomainName,sslEnforcement:sslEnforcement}' -o json"
            )
            
            import json
            mysql_servers = json.loads(mysql_output)
            
            for server in mysql_servers:
                instances.append(AzureDbInstance(
                    resource_group=server['resourceGroup'],
                    server_name=server['name'],
                    database_type="mysql",
                    location=server['location'],
                    version=server.get('version', '5.7'),
                    sku=server.get('sku', 'GP_Gen5'),
                    administrator_login=server['administratorLogin'],
                    fully_qualified_domain_name=server['fqdn'],
                    port=3306,
                    ssl_enforcement=server.get('sslEnforcement', 'Enabled')
                ))
            
            # 获取 PostgreSQL 服务器
            pg_output = self._run_azure_cli(
                "az postgres server list --query '[].{resourceGroup:resourceGroup,name:name,location:location,version:version,sku:sku.tier,administratorLogin:administratorLogin,fqdn:fullyQualifiedDomainName,sslEnforcement:sslEnforcement}' -o json"
            )
            
            pg_servers = json.loads(pg_output)
            
            for server in pg_servers:
                instances.append(AzureDbInstance(
                    resource_group=server['resourceGroup'],
                    server_name=server['name'],
                    database_type="postgresql",
                    location=server['location'],
                    version=server.get('version', '11'),
                    sku=server.get('sku', 'GP_Gen5'),
                    administrator_login=server['administratorLogin'],
                    fully_qualified_domain_name=server['fqdn'],
                    port=5432,
                    ssl_enforcement=server.get('sslEnforcement', 'Enabled')
                ))
            
            self.instances = instances
            logger.info(f"找到 {len(instances)} 个 Azure Database 服务器")
            
        except Exception as e:
            logger.error(f"获取 Azure Database 服务器列表失败：{str(e)}")
            raise
        
        return instances
    
    def get_server_admin_password(self, server_name: str, resource_group: str) -> str:
        """
        获取服务器管理员密码
        
        注意：Azure 不支持直接获取密码，需要从 Key Vault 或用户输入
        此方法仅作为占位符，实际使用需要用户输入
        
        Args:
            server_name: 服务器名称
            resource_group: 资源组名称
        
        Returns:
            管理员密码（需要用户输入）
        """
        import getpass
        logger.warning("Azure 不支持直接获取管理员密码，请手动输入")
        password = getpass.getpass(f"请输入 {server_name} 的管理员密码：")
        return password
    
    def configure_firewall_rule(self, server_name: str, resource_group: str, 
                                rule_name: str, start_ip: str, end_ip: str = None):
        """
        配置防火墙规则
        
        Args:
            server_name: 服务器名称
            resource_group: 资源组名称
            rule_name: 规则名称
            start_ip: 起始 IP
            end_ip: 结束 IP（可选，默认与 start_ip 相同）
        """
        if end_ip is None:
            end_ip = start_ip
        
        database_type = None
        for inst in self.instances:
            if inst.server_name == server_name:
                database_type = inst.database_type
                break
        
        if not database_type:
            raise Exception(f"未找到服务器：{server_name}")
        
        command = f"az {database_type} server firewall-rule create " \
                  f"--resource-group {resource_group} " \
                  f"--server-name {server_name} " \
                  f"--name {rule_name} " \
                  f"--start-ip-address {start_ip} " \
                  f"--end-ip-address {end_ip}"
        
        self._run_azure_cli(command)
        logger.info(f"✓ 防火墙规则 {rule_name} 已创建 ({start_ip} - {end_ip})")
    
    def allow_azure_services(self, server_name: str, resource_group: str):
        """
        允许 Azure 服务访问
        
        Args:
            server_name: 服务器名称
            resource_group: 资源组名称
        """
        database_type = None
        for inst in self.instances:
            if inst.server_name == server_name:
                database_type = inst.database_type
                break
        
        if not database_type:
            raise Exception(f"未找到服务器：{server_name}")
        
        command = f"az {database_type} server firewall-rule create " \
                  f"--resource-group {resource_group} " \
                  f"--server-name {server_name} " \
                  f"--name AllowAzureServices " \
                  f"--start-ip-address 0.0.0.0 " \
                  f"--end-ip-address 0.0.0.0"
        
        self._run_azure_cli(command)
        logger.info(f"✓ 已允许 Azure 服务访问 {server_name}")
    
    def get_connection_string(self, instance: AzureDbInstance, database: str = None) -> str:
        """
        获取连接字符串
        
        Args:
            instance: AzureDbInstance 对象
            database: 数据库名称（可选）
        
        Returns:
            连接字符串
        """
        if instance.database_type == "mysql":
            conn_str = f"mysql://{instance.administrator_login}@{instance.server_name}.mysql.database.azure.com:{instance.port}"
            if database:
                conn_str += f"/{database}"
            return conn_str
        
        elif instance.database_type == "postgresql":
            conn_str = f"postgresql://{instance.administrator_login}@{instance.server_name}.postgres.database.azure.com:{instance.port}"
            if database:
                conn_str += f"/{database}"
            return conn_str
        
        else:
            raise Exception(f"不支持的数据库类型：{instance.database_type}")
    
    def list_servers_interactive(self) -> Optional[AzureDbInstance]:
        """
        交互式选择数据库服务器
        
        Returns:
            用户选择的 AzureDbInstance，或 None（如果用户取消）
        """
        instances = self.list_all_servers()
        
        if not instances:
            print("未找到任何 Azure Database 服务器")
            return None
        
        print("\n找到的 Azure Database 服务器：")
        print("-" * 80)
        
        for i, inst in enumerate(instances, 1):
            print(f"{i}. {inst.server_name}")
            print(f"   类型：{inst.database_type}")
            print(f"   位置：{inst.location}")
            print(f"   版本：{inst.version}")
            print(f"   主机：{inst.fully_qualified_domain_name}:{inst.port}")
            print(f"   管理员：{inst.administrator_login}")
            print(f"   SSL: {inst.ssl_enforcement}")
            print()
        
        # 让用户选择
        while True:
            try:
                choice = input("请选择服务器编号（或 0 退出）：").strip()
                choice_num = int(choice)
                
                if choice_num == 0:
                    return None
                elif 1 <= choice_num <= len(instances):
                    return instances[choice_num - 1]
                else:
                    print(f"请输入 0-{len(instances)} 之间的数字")
            except ValueError:
                print("请输入有效的数字")
