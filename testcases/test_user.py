import allure
import pytest
from api.user_api import UserApi
from core import logger
from core.assert_util import assert_util
from common.yaml_util import yaml_util

# 读取测试数据


user_data = yaml_util.read_yaml("user_data.yaml")
print("----------------------",user_data)


@allure.feature("用户模块")
class TestUser:
    @allure.story("用户登录")
    @allure.title("正常登录")
    @pytest.mark.parametrize("data", [user_data["login_success"]])
    def test_login_success(self, data):
        """登录成功用例"""
        with allure.step("1. 调用登录接口"):
            resp = UserApi.login(data["username"], data["password"])

        with allure.step("2. 断言响应状态码"):
            assert_util.assert_code(resp, data["expected_code"])

        with allure.step("3. 断言响应包含成功提示"):
            assert_util.assert_contains(resp, data["expected_key"])

    @allure.story("用户登录")
    @allure.title("密码错误登录失败")
    @pytest.mark.parametrize("data", [user_data["login_fail_wrong_pwd"]])
    def test_login_fail(self, data):
        """登录失败用例"""
        resp = UserApi.login(data["username"], data["password"])
        assert_util.assert_code(resp, data["expected_code"])
        assert_util.assert_contains(resp, data["expected_msg"])

    @allure.story("获取用户信息")
    @allure.title("带有效token获取用户信息")
    def test_get_user_info(self, login_token):
        """获取用户信息用例"""
        resp = UserApi.get_user_info(login_token)
        # 断言状态码
        assert_util.assert_code(resp, 200)
        # 断言包含指定key
        assert_util.assert_json_key(resp, *user_data["user_info"]["expected_keys"])
        # 断言data包含指定key
        data = resp.json()["data"]
        for key in user_data["user_info"]["expected_data_keys"]:
            assert key in data