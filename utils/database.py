import os
import yaml
import pymysql
import logging
from utils.logger import logger  # 导入日志模块

logger.debug("Initializing Database module")

class Database:
    """
    数据库操作类，用于加载配置、建立连接并执行 SQL 查询。

    属性:
        conn (pymysql.Connection): 数据库连接对象。

    方法:
        __init__: 初始化数据库连接
        execute: 执行写操作（INSERT, UPDATE, DELETE）并提交事务
        query: 执行查询操作并返回结果
    """

    def __init__(self):
        """
        初始化数据库连接。
        
        从配置文件中读取数据库连接参数，并建立连接。
        如果配置文件缺失必要字段，抛出 ValueError。
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, "..", "config", "db_config.yaml")

        logger.info(f"加载数据库配置文件: {config_path}")
        
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        required_keys = ['host', 'port', 'user', 'password', 'db']
        if not all(key in config['database'] for key in required_keys):
            logger.error("数据库配置文件缺少必要字段")
            raise ValueError("数据库配置文件缺少必要字段")

        logger.debug(f"连接数据库: {config['database']['host']}:{config['database']['port']} - {config['database']['db']}")
        
        self.conn = pymysql.connect(
            host=config['database']['host'],
            port=config['database']['port'],
            user=config['database']['user'],
            password=config['database']['password'],
            db=config['database']['db'],
            cursorclass=pymysql.cursors.DictCursor
        )

    def execute(self, sql, params=None):
        """
        执行写操作（INSERT, UPDATE, DELETE）并提交事务。

        参数:
            sql (str): 要执行的 SQL 语句。
            params (tuple, optional): SQL 参数化查询的参数，默认为 None。

        返回:
            list: 查询结果列表。

        抛出:
            RuntimeError: 如果 SQL 执行失败。
        """
        logger.debug(f"执行SQL语句: {sql} 参数: {params}")
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, params or ())
                result = cursor.fetchall()
                self.conn.commit()
                logger.info(f"SQL执行成功，影响行数: {cursor.rowcount}")
                return result
        except Exception as e:
            self.conn.rollback()
            logger.error(f"执行SQL时出错: {str(e)}")
            raise RuntimeError(f"执行SQL时出错：{str(e)}")

    def query(self, sql, params=None):
        """
        执行查询操作（SELECT）并返回结果。

        参数:
            sql (str): 要执行的 SQL 语句。
            params (tuple, optional): SQL 参数化查询的参数，默认为 None。

        返回:
            list: 查询结果列表，每行作为一个字典。

        抛出:
            RuntimeError: 如果 SQL 执行失败。
        """
        logger.debug(f"查询SQL语句: {sql} 参数: {params}")
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, params or ())
                return cursor.fetchall()
        except Exception as e:
            logger.error(f"查询SQL时出错: {str(e)}")
            raise RuntimeError(f"查询SQL时出错：{str(e)}")

    def get_table_schema(self):
        """
        获取数据库中的表结构信息。
        
        返回:
            dict: 表结构信息，格式为 {表名: [列名列表]}
        """