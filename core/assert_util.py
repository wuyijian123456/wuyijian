from common.db_util import DBUtil
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
    def validate_response(response_data, model_class):
        """统一校验入口，自动处理异常并打印友好信息"""
        from pydantic import ValidationError
        try:
            log.info("响应模型结构校验中")
            return model_class(**response_data)
        except ValidationError as e:
            # 打印详细的错误路径和原因
            errors = [f"{err['loc']}: {err['msg']}" for err in e.errors()]
            log.error(f"响应结构校验失败:\n" + "\n".join(errors))
            raise AssertionError(f"响应结构校验失败:\n" + "\n".join(errors))

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
            log.error(f"响应内容：{response.text[:500]}")
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
            log.error(f"响应内容：{response.text[:500]}")
            raise

    @staticmethod
    def assert_contains(response, expected_str):
        """断言响应内容包含指定字符串"""
        try:
            assert expected_str in response.text
            # log.info(f"响应内容：'{response.text[:500]}'")
            log.info(f"包含断言成功：响应内容包含'{expected_str}'")
        except AssertionError:
            # log.error(f"响应内容：'{response.text[:500]}'")
            log.error(f"包含断言失败：响应内容不包含'{expected_str}'")
            raise

class DatabaseAssert:
    """
    数据库断言工具类
    封装了常见断言方法，复用 DBUtil 全局实例
    """
    def __init__(self,db):
        self.db = db

    # ---------- 断言方法 ----------

    def assert_row_exists(self, sql, params, msg: Optional[str] = None):
        """断言表中存在满足条件的记录"""
        record = self.db.query_one(sql, params)

        assert record is not None,msg
        return record

    def assert_row_not_exists(self, sql, params, msg: Optional[str] = None):
        """断言不存在满足条件的记录"""
        record = self.db.query_one(sql, params)
        assert record is None,msg

    def assert_count_equal(self,sql, params, expected: int, msg: Optional[str] = None):
        """断言满足条件的记录数等于预期值"""
        actual = self.db.count(sql.split('FROM ')[1].strip().split(' ')[0],
                               condition=sql.split('WHERE ')[1] if 'WHERE' in sql else '1=1',
                               params=params)
        log.info(f"查询总数为：{actual}")
        assert actual == expected,msg

    def assert_field_value(self,sql, params, filed, expected: Any, msg: Optional[str] = None):
        """
        断言某条记录的某个字段值等于预期
        """
        record = self.db.query_one(sql, params)
        log.info(f"数据库断言sql的查询值：{sql},{params}")
        assert record[filed] == expected , msg
        return record[filed]

    def assert_field_contains_value(self,sql, params, field: str, expected: Any, msg: Optional[str] = None):
        """
        断言某条记录的某个字段值等于预期
        """
        record = self.db.query(sql, params)
        if field:
            list = [item[field] for item in record]
        else:
            list = list(record.values())[0]
        log.info(f"===================================================数据库返回字段：{list}")
        assert expected in list
        log.info(msg or f"包含断言成功：响应内容包含{expected}")




# 全局断言实例
assert_util = AssertUtil()



