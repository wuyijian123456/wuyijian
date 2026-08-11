from core.assert_util import assert_util
from core.retry import retry
import allure
import pytest
import os
from common.yaml_util import yaml_util
from common.var_replace_util import var_util
from core.logger import log
from common.params_set import req_params_Collection
from core.report_enhancer import ReportEnhancer

# 加载用户模块测试数据
_user_yaml_path = os.path.join("user", "test_menus.yaml")
_user_all_data = yaml_util.read_yaml(_user_yaml_path)

@allure.suite("用户管理123")
@allure.feature("用户管理456")
class Testuser:
    @allure.story("获取用户权限")
    @allure.title("当前用户权限")
    @pytest.mark.parametrize("data",[_user_all_data.get("permissions_success",{})],ids=['permissions_success'])
    def test_current_user_permissions(self,data,user_api):
        with allure.step("1. 从data中获取测试请求数据"):
            data = req_params_Collection(data)
            log.info(data)
            ReportEnhancer.add_request_details(url=data.url, method='put',
                                               params=(data.params, data.data, data.json))
        with allure.step("2. 调用请求接口"):
            resp = user_api.get_user_permissions(data.url)
            allure.attach(name="响应状态码", body=str(resp.status_code))
        with allure.step("3. 断言响应状态码"):
            assert_util.assert_code(resp, data.expected_code)
        with allure.step("4. 数据库断言响应字段"):
            # db.assert_field_contains_value(sql= "select permission_code from  sys_role_permission where role_id= %s",params=(1,),field = "permission_code",
            #                                expected=data.expected_data)
            pass


    @allure.story("获取用户菜单")
    @allure.title("当前用户菜单")
    @pytest.mark.parametrize("data",[_user_all_data.get("menus_success",{})],ids=['menus_success'])
    def test_current_user_menus(self,data,user_api):
        with allure.step("1. 获取测试请求数据"):
            data = req_params_Collection(data)
            log.info(data)
            ReportEnhancer.add_request_details(url=data.url, method='put',
                                               params=(data.params, data.data, data.json))

        with allure.step("2. 调用请求接口"):
            resp = user_api.get_user_menus(data.url)
            allure.attach(name="响应状态码", body=str(resp.status_code))

        with allure.step("3.断言响应状态码"):
            assert_util.assert_code(resp, data.expected_code)

        with allure.step("4.断言数据库响应字段"):
            pass

        with allure.step("4.后置清理数据"):
            pass

    @allure.story("获取科室列表")
    @allure.title("科室列表")
    @pytest.mark.parametrize("data",[_user_all_data.get("departments_success",{}),_user_all_data.get("departments_noparams_success",{})],
                             ids=['departments_success','departments_noparams_success'])
    def test_department_list(self,data,user_api):
        with allure.step("1. 获取测试请求数据"):
            data = req_params_Collection(data)
            log.info(data)
            ReportEnhancer.add_request_details(url=data.url, method='put',
                                               params=(data.params, data.data, data.json))
        with allure.step("2. 调用请求接口"):
            resp = user_api.get_user_departments(data.url,data.params)
            ReportEnhancer.add_response_details(resp.status_code,resp.json())
        with allure.step("3.断言响应状态码"):
            assert_util.assert_code(resp, data.expected_code)

        with allure.step("4.断言数据库响应字段"):
            pass

        with allure.step("5.后置清理数据"):
            pass


