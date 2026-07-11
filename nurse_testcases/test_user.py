from core.assert_util import assert_util,db
from nurse_api.user_api import Userapi
import allure
import pytest
import os
from common.yaml_util import yaml_util
from common.var_replace_util import var_util
from core.logger import log

# 加载用户模块测试数据
_user_yaml_path = os.path.join("user", "test_menus.yaml")
_user_all_data = yaml_util.read_yaml(_user_yaml_path)
# log.info(_user_all_data)

@allure.feature("用户管理")
class Testuser:
    @allure.story("获取用户权限")
    @allure.title("当前用户权限")
    @pytest.mark.parametrize("data",[_user_all_data.get("permissions_success",{})],ids=['permissions_success'])
    def test_current_user_permissions(self,data,login_cookie):
        with allure.step("1. 从data中获取测试请求数据"):
            data = var_util.replace(data)
            url = data.get("url")
            params = data.get("params")
            cookie = data.get("cookie")
            expected_code = data.get("expected_code")
            expected_data = data.get("expected_data")
        with allure.step("2. 调用请求接口"):
            resp = Userapi().get_user_permissions(url, cookie)
            allure.attach(name="响应状态码", body=str(resp.status_code))
        with allure.step("3. 断言响应状态码"):
            assert_util.assert_code(resp, expected_code)
        with allure.step("4. 数据库断言响应字段"):
            db.assert_field_contains_value(sql= "select permission_code from  sys_role_permission where role_id= %s",params=(1,),field = "permission_code",
                                           expected=expected_data)

    @pytest.mark.parametrize("data",[_user_all_data.get("menus_success",{})],ids=['menus_success'])
    def test_current_user_menus(self,data):
        with allure.step("1. 获取测试请求数据"):
            data = var_util.replace(data)
            log.info(data)
            url = data.get("url")
            params = data.get("params")
            cookie = data.get("cookie")
            expected_code = data.get("expected_code")
            expected_data = data.get("expected_data")

        with allure.step("2. 调用请求接口"):
            resp = Userapi().get_user_menus(url,cookie)
            allure.attach(name="响应状态码", body=str(resp.status_code))

        with allure.step("3.断言响应状态码"):
            assert_util.assert_code(resp, expected_code)

        with allure.step("4.断言数据库响应字段"):
            pass

        with allure.step("4.后置清理数据"):
            pass

