import pymysql
from pymysql.cursors import DictCursor
from config.settings import DB_CONFIG
from core.logger import log


class DBUtil:
    """数据库操作工具类"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                cls._instance.conn = pymysql.connect(**DB_CONFIG, charset="utf8mb4")
                cls._instance.cursor = cls._instance.conn.cursor(DictCursor)
                log.info("数据库连接成功")
            except Exception as e:
                log.error(f"数据库连接失败：{str(e)}")
                raise
        return cls._instance
    
    def query(self, sql, params=None):
        """
        查询数据
        
        Args:
            sql (str): SQL 查询语句
            params (tuple/list, optional): 参数元组或列表
            
        Returns:
            list: 查询结果列表
        """
        log.debug(f"执行 SQL: {sql}, 参数：{params}")
        self.cursor.execute(sql, params or ())
        result = self.cursor.fetchall()
        log.debug(f"查询结果：{len(result)} 条记录")
        return result
    
    def execute(self, sql, params=None):
        """
        执行 SQL（INSERT/UPDATE/DELETE）
        
        Args:
            sql (str): SQL 语句
            params (tuple/list, optional): 参数
            
        Returns:
            int: 影响的行数
        """
        log.debug(f"执行 SQL: {sql}, 参数：{params}")
        affected_rows = self.cursor.execute(sql, params or ())
        self.conn.commit()
        log.info(f"SQL 执行成功，影响行数：{affected_rows}")
        return affected_rows
    
    def executemany(self, sql, params_list):
        """
        批量执行 SQL
        
        Args:
            sql (str): SQL 语句
            params_list (list): 参数列表
            
        Returns:
            int: 影响的行数
        """
        log.debug(f"批量执行 SQL: {sql}")
        affected_rows = self.cursor.executemany(sql, params_list)
        self.conn.commit()
        log.info(f"批量执行成功，影响行数：{affected_rows}")
        return affected_rows
    
    def query_one(self, sql, params=None):
        """
        查询单条数据
        
        Args:
            sql (str): SQL 查询语句
            params (tuple/list, optional): 参数
            
        Returns:
            dict: 单条记录
        """
        result = self.query(sql, params)
        return result[0] if result else None
    
    def count(self, table, condition="1=1", params=None):
        """
        统计表记录数
        
        Args:
            table (str): 表名
            condition (str, optional): WHERE 条件
            params (tuple/list, optional): 参数
            
        Returns:
            int: 记录数
        """
        sql = f"SELECT COUNT(*) as total FROM {table} WHERE {condition}"
        result = self.query_one(sql, params)
        return result['total'] if result else 0
    
    def close(self):
        """关闭连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            log.info("数据库连接已关闭")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 全局数据库实例
db = DBUtil()


# ==================== 数据库断言工具 ====================

class DBAssert:
    """数据库断言工具类"""
    
    @staticmethod
    def assert_exists(table, condition, params=None, message="数据不存在"):
        """
        断言数据存在
        
        Args:
            table (str): 表名
            condition (str): WHERE 条件
            params (tuple/list, optional): 参数
            message (str): 自定义错误消息
        """
        count = db.count(table, condition, params)
        assert count > 0, f"{message} | 表：{table}, 条件：{condition}"
        log.info(f"数据库断言通过：在 {table} 中找到 {count} 条记录")
    
    @staticmethod
    def assert_not_exists(table, condition, params=None, message="数据不应存在"):
        """
        断言数据不存在
        
        Args:
            table (str): 表名
            condition (str): WHERE 条件
            params (tuple/list, optional): 参数
            message (str): 自定义错误消息
        """
        count = db.count(table, condition, params)
        assert count == 0, f"{message} | 表：{table}, 条件：{condition}"
        log.info(f"数据库断言通过：在 {table} 中未找到记录")
    
    @staticmethod
    def assert_field_value(table, field, expected_value, condition, params=None, message="字段值不匹配"):
        """
        断言字段值
        
        Args:
            table (str): 表名
            field (str): 字段名
            expected_value (any): 期望值
            condition (str): WHERE 条件
            params (tuple/list, optional): 参数
            message (str): 自定义错误消息
        """
        sql = f"SELECT {field} FROM {table} WHERE {condition} LIMIT 1"
        result = db.query_one(sql, params)
        
        assert result is not None, f"未找到记录 | 表：{table}, 条件：{condition}"
        actual_value = result.get(field)
        assert str(actual_value) == str(expected_value), \
            f"{message} | 字段：{field}, 期望：{expected_value}, 实际：{actual_value}"
        
        log.info(f"数据库字段断言通过：{field} = {actual_value}")
    
    @staticmethod
    def assert_record_count(table, expected_count, condition="1=1", params=None, message="记录数不匹配"):
        """
        断言记录数
        
        Args:
            table (str): 表名
            expected_count (int): 期望记录数
            condition (str): WHERE 条件
            params (tuple/list, optional): 参数
            message (str): 自定义错误消息
        """
        actual_count = db.count(table, condition, params)
        assert actual_count == expected_count, \
            f"{message} | 表：{table}, 期望：{expected_count}, 实际：{actual_count}"
        
        log.info(f"数据库记录数断言通过：{actual_count} == {expected_count}")
    
    @staticmethod
    def assert_sql_result(sql, assertion_func, params=None, message="SQL 断言失败"):
        """
        自定义 SQL 断言
        
        Args:
            sql (str): SQL 查询语句
            assertion_func (function): 断言函数，接收查询结果作为参数
            params (tuple/list, optional): 参数
            message (str): 自定义错误消息
        """
        result = db.query(sql, params)
        try:
            assertion_func(result)
            log.info(f"自定义 SQL 断言通过")
        except AssertionError as e:
            log.error(f"{message} | SQL: {sql}, 结果：{result}")
            raise


# 全局断言实例
db_assert = DBAssert()