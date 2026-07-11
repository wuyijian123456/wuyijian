import pymysql
from pymysql import connect

from config.settings import MYSQL_CONFIG
from core.logger import log
from typing import Any, Dict, List, Optional, Union

class AssertUtil:
    """通用断言工具：简化断言逻辑，统一日志输出"""
    @staticmethod
    def assert_code(response, expected_code):
        """断言响应状态码"""
        actual_code = response.status_code
        try:
            assert actual_code == expected_code
            log.info(f"状态码断言成功：{actual_code} == {expected_code}")
        except AssertionError:
            log.error(f"状态码断言失败：{actual_code} != {expected_code}")
            raise

    @staticmethod
    def assert_json_key(response, *keys):
        """断言JSON响应包含指定key"""
        try:
            resp_json = response.json()
            for key in keys:
                assert key in resp_json
                log.info(f"JSON Key断言成功：存在key={key}")
        except (AssertionError, ValueError) as e:
            log.error(f"JSON Key断言失败：{str(e)}")
            raise

    @staticmethod
    def assert_json_value(response, key, expected_value):
        """断言JSON响应中指定key的value"""
        try:
            resp_json = response.json()
            actual_value = resp_json.get(key)
            assert actual_value == expected_value
            log.info(f"JSON Value断言成功：{key}={actual_value} == {expected_value}")
        except (AssertionError, ValueError) as e:
            log.error(f"JSON Value断言失败：{str(e)}")
            raise

    @staticmethod
    def assert_contains(response, expected_str):
        """断言响应内容包含指定字符串"""
        try:
            assert expected_str in response.text
            # log.info(f"响应内容：'{response.json()}'")
            log.info(f"包含断言成功：响应内容包含'{expected_str}'")
        except AssertionError:
            log.info(f"响应内容：'{response.text}'")
            log.error(f"包含断言失败：响应内容不包含'{expected_str}'")
            raise

class DatabaseAssert:
    """
    数据库断言工具类
    封装了连接建立、查询执行、常见断言方法
    """

    def __init__(self, host: str, port: int, user: str, password: str, database: str, charset: str = "utf8mb4"):
        self.config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
            "charset": charset,
            "cursorclass": pymysql.cursors.DictCursor  # 返回字典格式
        }
        self.conn  = None
        self.cursor = None

    def connect(self):
        """建立数据库连接"""
        try:
            self.conn = pymysql.connect(**self.config)
            self.cursor = self.conn.cursor()
        except Exception():
            log.error("连接失败")

    def close(self):
        """关闭连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # ---------- 查询方法 ----------
    def query_one(self, sql: str, params: Optional[Union[tuple, dict]] = None) -> Optional[Dict[str, Any]]:
        """查询单条记录，返回字典"""
        try:
            self.connect()
            self.cursor.execute(sql, params)
            return self.cursor.fetchone()
        finally:
            self.close()

    def query_all(self, sql: str, params: Optional[Union[tuple, dict]] = None) -> List[Dict[str, Any]]:
        """查询多条记录，返回字典列表"""
        try:
            self.connect()
            self.cursor.execute(sql, params)
            return self.cursor.fetchall()
        finally:
            self.close()

    def query_count(self, sql: str, params: Optional[Union[tuple, dict]] = None) -> int:
        """查询记录数（COUNT）"""
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            return list(result.values())[0] if result else 0
        finally:
            self.close()

    # ---------- 断言方法 ----------
    def assert_row_exists(self, sql, params, msg: Optional[str] = None):
        """断言表中存在满足条件的记录"""
        record = self.query_one(sql, params)
        assert record is not None
        log.info(msg or f"期望记录存在，但未找到满足条件的记录")

    def assert_row_not_exists(self, sql, params, msg: Optional[str] = None):
        """断言不存在满足条件的记录"""
        record = self.query_one(sql, params)
        assert record is None
        log.info(msg or f"期望记录不存在，但找到了满足条件的记录")

    def assert_count_equal(self,sql, params, expected: int, msg: Optional[str] = None):
        """断言满足条件的记录数等于预期值"""
        actual = self.query_count(sql, params)
        assert actual == expected
        log.info(msg or f"记录数断言失败: 期望 {expected}, 实际 {actual}")

    def assert_field_value(self,sql, params, expected: Any, msg: Optional[str] = None):
        """
        断言某条记录的某个字段值等于预期
        """
        record = self.query_one(sql, params)
        assert record == expected
        log.info(msg or f"字段 断言失败: 期望 {expected!r}, 实际 {record}")

    def assert_field_contains_value(self,sql, params, field: str, expected: Any, msg: Optional[str] = None):
        """
        断言某条记录的某个字段值等于预期
        """
        record = self.query_all(sql, params)
        list =[]
        for i in record:
            if i[field]:
                list.append(i[field])
        assert expected in list
        log.info(msg or f"包含断言成功：响应内容包含{expected}")



# 全局断言实例
assert_util = AssertUtil()
db = DatabaseAssert(**MYSQL_CONFIG)

