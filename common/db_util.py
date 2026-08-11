import pymysql
from pymysql.cursors import DictCursor
from core.logger import log


class DBUtil:
    """数据库操作工具类"""
    _instance = None
    def __new__(cls,env_config_mysql:dict):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                cls._instance.conn = pymysql.connect(**env_config_mysql, charset="utf8mb4", autocommit=True)
                cls._instance.cursor = cls._instance.conn.cursor(DictCursor)
                log.info("数据库连接成功")
            except Exception as e:
                log.error(f"数据库连接失败：{str(e)}")
                raise
        return cls._instance

    def __init__(self, env_config_mysql:dict):
        pass



    def query(self, sql, params=None):
        """
        查询数据

        Args:
            sql (str): SQL 查询语句
            params (tuple/list, optional): 参数元组或列表

        Returns:
            list: 查询结果列表
        """
            # 🔧 处理不同格式的参数
        if params is None:
            params = ()
        elif isinstance(params, str):
            params = (params,)  # 字符串 → 元组
        elif isinstance(params, list):
            params = tuple(params)  # 列表 → 元组
        elif isinstance(params, dict):
            # SQLAlchemy 风格：保持字典不变
            pass
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
        if params is None:
            params = ()
        elif isinstance(params, str):
            params = (params,)  # 字符串 → 元组
        elif isinstance(params, list):
            params = tuple(params)  # 列表 → 元组
        elif isinstance(params, dict):
            # SQLAlchemy 风格：保持字典不变
            pass
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
        if params_list is None:
            params = ()
        elif isinstance(params_list, str):
            params = (params_list,)  # 字符串 → 元组
        elif isinstance(params_list, list):
            params = tuple(params_list)  # 列表 → 元组
        elif isinstance(params_list, dict):
            # SQLAlchemy 风格：保持字典不变
            pass
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



