import allure
import pytest
from api.user_api import UserApi
from core import logger
from core.assert_util import assert_util
from common.yaml_util import yaml_util

# 读取测试数据


user_data = yaml_util.read_yaml("user_data.yaml")
# print("----------------------",user_data)


@allure.feature("用户模块")
class TestUser:
    @allure.story("用户登录")
    @allure.title("正常登录")
    @pytest.mark.parametrize("data", [user_data["login_success"],user_data["login_fail_wrong_pwd"]],ids=["success","fail"])
    @pytest.mark.order(num=1)
    def test_login_success(self, data):
        """登录成功用例"""
        
        with allure.step("1. 准备登录凭证"):
            username = data["username"]
            log.info(f"用户名：{username}")
            allure.attach(name="用户名", body=username)
        
        with allure.step("2. 调用登录接口"):
            resp = UserApi.login(data["url"], data["username"], data["password"])
            allure.attach(name="响应状态码", body=str(resp.status_code))
        
        with allure.step("3. 断言响应状态码"):
            assert_util.assert_code(resp, data["expected_code"])
        
        with allure.step("4. 断言响应包含访问令牌"):
            assert_util.assert_contains(resp, data["expected_key"])
            allure.attach(name="预期字段", body=data["expected_key"])


    @allure.story("获取用户信息")
    @allure.title("带有效 token 获取用户信息")
    @pytest.mark.order(num=3)
    def test_get_user_info(self, login_token):
        """获取用户信息用例"""
        
        with allure.step("1. 准备请求参数"):
            url = user_data["user_info"]["url"]
            log.info(f"请求 URL: {url}")
        
        with allure.step("2. 调用获取用户信息接口"):
            resp = UserApi.get_user_info(url, login_token)
            allure.attach(name="响应状态码", body=str(resp.status_code))
        
        with allure.step("3. 断言响应状态码为 200"):
            assert_util.assert_code(resp, 200)
        
        with allure.step("4. 断言响应体包含指定字段"):
            expected_keys = user_data["user_info"]["expected_keys"]
            assert_util.assert_json_key(resp, *expected_keys)
            allure.attach(name="预期字段", body=", ".join(expected_keys))
        
        with allure.step("5. 验证 data 对象包含用户信息"):
            data = resp.json()["data"]
            expected_data_keys = user_data["user_info"]["expected_data_keys"]
            for key in expected_data_keys:
                assert key in data, f"缺少字段：{key}"
            allure.attach(name="用户信息字段", body=", ".join(expected_data_keys))
            allure.attach(name="实际数据", body=str(data), attachment_type=allure.attachment_type.JSON)
    
    @allure.story("修改密码")
    @allure.title("修改密码场景测试")
    @pytest.mark.parametrize("data", 
        [user_data["update_password_success"], user_data["update_password_fail_wrong_old_pwd"]], 
        ids=["success", "fail_wrong_old_pwd"])
    @pytest.mark.order(num=4)
    def test_update_password(self, login_token, data):
        """修改密码测试用例（数据驱动）"""
        
        with allure.step("1. 准备测试数据"):
            log.info(f"测试场景：{data.get('expected_msg', '错误场景')}")
            allure.attach(name="原密码", body=data["old_password"])
            allure.attach(name="新密码", body=data["new_password"])
        
        with allure.step("2. 调用修改密码接口"):
            resp = UserApi.update_password(
                url=data["url"],
                token=login_token,
                old_pwd=data["old_password"],
                new_pwd=data["new_password"]
            )
            allure.attach(name="响应状态码", body=str(resp.status_code))
        
        with allure.step("3. 断言响应状态码"):
            assert_util.assert_code(resp, data["expected_code"])
        
        # 根据预期结果选择断言内容
        if "expected_msg" in data:
            with allure.step("4. 断言响应包含成功提示"):
                assert_util.assert_contains(resp, data["expected_msg"])
                allure.attach(name="成功消息", body=data["expected_msg"])
        elif "expected_key" in data:
            with allure.step("4. 断言响应包含错误信息"):
                assert_util.assert_contains(resp, data["expected_key"])
                allure.attach(name="错误字段", body=data["expected_key"])