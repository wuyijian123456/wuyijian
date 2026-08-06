import json
from common.response_extractor import ResponseExtractor
from common.data_factory import data_factory
from common.db_util import db
from core.assert_util import assert_util,dbAssert
from nurse_api.intern_api import InternManageApi,InternRotatiobApi
import allure
import pytest
import os
from common.yaml_util import yaml_util
from common.var_replace_util import var_util, VarUtil
from core.logger import log
from common.params_set import req_params_Collection
from core.report_enhancer import ReportEnhancer


# 加载实习生模块测试数据

intern_yaml_path = os.path.join('intern', "test_intern.yaml")
intern_rotation_yaml_path = os.path.join('intern', "test_intern_rotation.yaml")
intern_all_data = yaml_util.read_yaml(intern_yaml_path)
intern_rotation_all_data = yaml_util.read_yaml(intern_rotation_yaml_path)
log.info(f"{intern_all_data},{intern_rotation_all_data}")

#
# @allure.suite("实习生管理")
# @allure.feature("实习生管理")
# @pytest.mark.skip(reason="整个模块功能未上线")
# class Test_intern_manage:
#
#     @allure.story("实习生人员列表信息")
#     @allure.title("根据条件获取实习生人员列表信息")
#     @pytest.mark.skip
#     @pytest.mark.parametrize('data',[intern_all_data.get("123")],ids=['123'])
#     def test_get_intern_info(self, data):
#         with allure.step("1. 从data中获取测试请求数据"):
#             data = req_params_Collection(data)
#             ReportEnhancer.add_request_details(url=data.url,method='get',headers= None,params=data.params)
#
#         with allure.step("2. 调用请求接口"):
#             resp = InternManageApi.get_intern_info(data.url,data.params)
#             ReportEnhancer.add_response_details(resp.status_code,resp.json())
#
#         with allure.step("3. 断言响应状态码"):
#             assert_util.assert_code(resp, data.expected_code)
#
#         with allure.step("4. 数据库断言响应字段"):
#             ReportEnhancer.add_sql_details(data.sql,data.sql_params)
#
#
#     @allure.story("实习生人员列表信息")
#     @allure.title("新增实习生人员信息")
#     @pytest.mark.parametrize('data',[intern_all_data.get("123")],ids=['123'])
#     def test_add_intern_info(self, data):
#         with allure.step("1. 从data中获取测试请求数据"):
#             data = req_params_Collection(data)
#             ReportEnhancer.add_request_details(url=data.url,method='post',headers= None,params=data.params)
#
#         with allure.step("2. 调用请求接口"):
#             resp = InternManageApi.add_intern_info(data.url,data.params)
#             ReportEnhancer.add_response_details(resp.status_code,resp.json())
#
#         with allure.step("3. 断言响应状态码"):
#             assert_util.assert_code(resp, data.expected_code)
#             assert_util.assert_contains(resp, data.expected_data)
#
#         with allure.step("4. 数据库断言响应字段"):
#             dbAssert.assert_row_exists(data.sql,data.sql_params,"数据库不存在该数据")
#             ReportEnhancer.add_sql_details(data.sql,data.sql_params)
#
#
#
#     @allure.story("实习生人员列表信息")
#     @allure.title("编辑实习生人员信息")
#     @pytest.mark.parametrize('data',[intern_all_data.get("123")],ids=['123'])
#     def test_update_intern_info(self, data):
#         with allure.step("1. 从data中获取测试请求数据"):
#             data = req_params_Collection(data)
#             ReportEnhancer.add_request_details(url=data.url,method='put',headers= None,params=data.params)
#
#         with allure.step("2. 调用请求接口"):
#             resp = InternManageApi.update_intern_info(data.url,data.params)
#             ReportEnhancer.add_response_details(resp.status_code,resp.json())
#
#         with allure.step("3. 断言响应状态码"):
#             assert_util.assert_code(resp, data.expected_code)
#             assert_util.assert_contains(resp, data.expected_data)
#
#         with allure.step("4. 数据库断言响应字段"):
#             dbAssert.assert_field_value(data.sql,data.sql_params,filed =data.field,msg="数据库中该字段的值不匹配")
#             ReportEnhancer.add_sql_details(data.sql,data.sql_params)
#
#
#
#     @allure.story("实习生人员列表信息")
#     @allure.title("删除实习生人员信息")
#     @pytest.mark.parametrize('data',[intern_all_data.get("123")],ids=['123'])
#     def test_delete_intern_info(self, data):
#         with allure.step("1. 从data中获取测试请求数据"):
#             data = req_params_Collection(data)
#             ReportEnhancer.add_request_details(url=data.url,method='delete',headers= None,params=data.params)
#
#         with allure.step("2. 调用请求接口"):
#             resp = InternManageApi.delete_intern_info(data.url,data.params)
#             ReportEnhancer.add_response_details(resp.status_code,resp.json())
#
#         with allure.step("3. 断言响应状态码"):
#             assert_util.assert_code(resp, data.expected_code)
#             assert_util.assert_contains(resp, data.expected_data)
#
#         with allure.step("4. 数据库断言响应字段"):
#             dbAssert.assert_row_exists(data.sql,data.sql_params,"删除后，数据库中还存在")
#             ReportEnhancer.add_sql_details(data.sql,data.sql_params)
#
#
#
# @allure.suite("实习生轮转记录")
# @allure.feature("实习生轮转记录")
# @pytest.mark.skip(reason="整个模块功能未上线")
# class Test_intern_rotation:
#
#     @allure.story("实习生轮转记录")
#     @allure.title("获取实习生轮转记录")
#     @pytest.mark.skip
#     @pytest.mark.parametrize('data', [intern_rotation_all_data.get("123")], ids=['123'])
#     def test_get_intern_info(self, data):
#         with allure.step("1. 从data中获取测试请求数据"):
#             data = req_params_Collection(data)
#             ReportEnhancer.add_request_details(url=data.url, method='get', headers=None, params=data.params)
#
#         with allure.step("2. 调用请求接口"):
#             resp = InternRotatiobApi.get_intern_rotation_info(data.url, data.params)
#             ReportEnhancer.add_response_details(resp.status_code, resp.json())
#
#         with allure.step("3. 断言响应状态码"):
#             assert_util.assert_code(resp, data.expected_code)
#
#         with allure.step("4. 数据库断言响应字段"):
#             ReportEnhancer.add_sql_details(data.sql, data.sql_params)
#
#     @allure.story("实习生轮转记录")
#     @allure.title("新增实习生轮转记录")
#     @pytest.mark.skip
#     @pytest.mark.parametrize('data', [intern_rotation_all_data.get("123")], ids=['123'])
#     def test_add_intern_info(self, data):
#         with allure.step("1. 从data中获取测试请求数据"):
#             data = req_params_Collection(data)
#             ReportEnhancer.add_request_details(url=data.url, method='post', headers=None, params=data.params)
#
#         with allure.step("2. 调用请求接口"):
#             resp = InternManageApi.add_intern_rotation_info(data.url, data.params)
#             ReportEnhancer.add_response_details(resp.status_code, resp.json())
#
#         with allure.step("3. 断言响应状态码"):
#             assert_util.assert_code(resp, data.expected_code)
#             assert_util.assert_contains(resp, data.expected_data)
#
#         with allure.step("4. 数据库断言响应字段"):
#             dbAssert.assert_row_exists(data.sql, data.sql_params, "数据库不存在该数据")
#             ReportEnhancer.add_sql_details(data.sql, data.sql_params)
#
#     @allure.story("实习生轮转记录")
#     @allure.title("编辑实习生轮转记录")
#     @pytest.mark.skip
#     @pytest.mark.parametrize('data', [intern_rotation_all_data.get("123")], ids=['123'])
#     def test_update_intern_info(self, data):
#         with allure.step("1. 从data中获取测试请求数据"):
#             data = req_params_Collection(data)
#             ReportEnhancer.add_request_details(url=data.url, method='put', headers=None, params=data.params)
#
#         with allure.step("2. 调用请求接口"):
#             resp = InternManageApi.update_intern_rotation_info(data.url, data.params)
#             ReportEnhancer.add_response_details(resp.status_code, resp.json())
#
#         with allure.step("3. 断言响应状态码"):
#             assert_util.assert_code(resp, data.expected_code)
#             assert_util.assert_contains(resp, data.expected_data)
#
#         with allure.step("4. 数据库断言响应字段"):
#             dbAssert.assert_field_value(data.sql, data.sql_params, filed=data.field, msg="数据库中该字段的值不匹配")
#             ReportEnhancer.add_sql_details(data.sql, data.sql_params)
#
#     @allure.story("实习生轮转记录")
#     @allure.title("删除实习生轮转记录")
#     @pytest.mark.skip
#     @pytest.mark.parametrize('data', [intern_rotation_all_data.get("123")], ids=['123'])
#     def test_delete_intern_info(self, data):
#         with allure.step("1. 从data中获取测试请求数据"):
#             data = req_params_Collection(data)
#             ReportEnhancer.add_request_details(url=data.url, method='delete', headers=None, params=data.params)
#
#         with allure.step("2. 调用请求接口"):
#             resp = InternManageApi.delete_intern_rotation_info(data.url, data.params)
#             ReportEnhancer.add_response_details(resp.status_code, resp.json())
#
#         with allure.step("3. 断言响应状态码"):
#             assert_util.assert_code(resp, data.expected_code)
#             assert_util.assert_contains(resp, data.expected_data)
#
#         with allure.step("4. 数据库断言响应字段"):
#             dbAssert.assert_row_exists(data.sql, data.sql_params, "删除后，数据库中还存在")
#             ReportEnhancer.add_sql_details(data.sql, data.sql_params)
