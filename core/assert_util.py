from core.logger import log

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
            log.info(f"响应内容：'{response.json()}'")
            log.info(f"包含断言成功：响应内容包含'{expected_str}'")
        except AssertionError:
            log.info(f"响应内容：'{response.text}'")
            log.error(f"包含断言失败：响应内容不包含'{expected_str}'")
            raise

# 全局断言实例
assert_util = AssertUtil()