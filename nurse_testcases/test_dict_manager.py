import json
from common.data_factory import data_factory
from common.db_util import db
from core.assert_util import assert_util,dbAssert
from nurse_api.dictionary_api import Dictionaryapi, statisticsapi, categoryapi
import allure
import pytest
import os
from common.yaml_util import yaml_util
from common.var_replace_util import var_util, VarUtil
from core.logger import log
from common.params_set import req_params_Collection
from core.report_enhancer import ReportEnhancer
# 加载用户模块测试数据

_dict_yaml_path = os.path.join('dict', "test_dict.yaml")
_dict_all_data = yaml_util.read_yaml(_dict_yaml_path)
log.info(f"{_dict_all_data.get('dictionary_item_success')}")

@allure.suite("字典管理123")
@allure.feature("字典管理456")
class TestDictManager:
    @allure.story("获取字典")
    @allure.title("根据codes获取字典")
    @pytest.mark.parametrize("data",[_dict_all_data.get("dictionary_item_success",{})],ids=['dictionary_success'])
    def test_current_user_permissions(self,data):
        with allure.step("1. 从data中获取测试请求数据"):
            data = req_params_Collection(data)
            ReportEnhancer.add_request_details(url=data.url, method='get',
                                               params=(data.params, data.data, data.json
                                                       ))
        with allure.step("2. 调用请求接口"):
            resp = Dictionaryapi.get_dict_by_allcode(data.url,data.params,)
            ReportEnhancer.add_response_details(resp.status_code,resp.json())
        with allure.step("3. 断言响应状态码"):
            assert_util.assert_code(resp, data.expected_code)
        with allure.step("4. 数据库断言响应字段"):
            ReportEnhancer.add_sql_details(data.sql,data.sql_params)
            pass



@allure.suite("字典管理123")
@allure.feature("字典管理456")
class TestStatistics:
    @allure.story("获取字典")
    @allure.title("根据codes获取字典")
    @pytest.mark.parametrize("data",[_dict_all_data.get("statistics_success",{})],ids=['statistics_success'])
    def test_Statistics_data(self,data):
        with allure.step("1. 从data中获取测试请求数据"):
            data = req_params_Collection(data)
            ReportEnhancer.add_request_details(url=data.url, method='get',
                                               params=(data.params, data.data, data.json))
        with allure.step("2. 调用请求接口"):
            resp = statisticsapi.get_statistics_data(data.url,data.params)
            ReportEnhancer.add_response_details(resp.status_code,resp.json())
        with allure.step("3. 接口响应断言"):
            assert_util.assert_code(resp, data.expected_code)
        with allure.step("4. 数据库断言响应字段"):
            ReportEnhancer.add_sql_details(data.sql,data.sql_params)
            dbAssert.assert_row_exists(data.sql,params=(data.sql_params,))
        with allure.step("5. 提取数据,接口关联"):
            pass
        with allure.step("6. 数据清理,防止数据污染"):
            pass

@allure.feature("字典管理456")
class Testcategory:
    @allure.story("字典目录")
    @allure.title("获取字典目录")
    @pytest.mark.parametrize("data",[_dict_all_data.get("category_success",{})],ids=['category_success'])
    def test_category_data(self,data):
        with allure.step("1. 从data中获取测试请求数据"):
            data = req_params_Collection(data)

            ReportEnhancer.add_request_details(url=data.url, method='get',
                                               params=(data.params, data.data, data.json))
        with allure.step("2. 调用请求接口"):
            resp = categoryapi.get_category_data(data.url,data.params)
            ReportEnhancer.add_response_details(resp.status_code,resp.json())
        with allure.step("3. 接口响应断言"):
            assert_util.assert_contains(resp, data.expected_data)
        with allure.step("4. 数据库断言响应字段"):
            pass
        with allure.step("5. 提取数据,接口关联"):
            pass
        with allure.step("6. 数据清理,防止数据污染"):
            pass

    @allure.story("字典目录")
    @allure.title("新增字典目录")
    @pytest.mark.order(num=1)
    @pytest.mark.parametrize("data",[_dict_all_data.get("add_category_success",{})],ids=['add_category_success'])
    def test_add_category_data(self,data):
        with allure.step("1. 从data中获取测试请求数据"):
            data = req_params_Collection(data)
            data.data["code"] = data_factory.random_string(length=3)
            ReportEnhancer.add_request_details(url=data.url, method='post',
                                               params=(data.params, data.data, data.json))
        with allure.step("2. 调用请求接口"):
            resp = categoryapi.add_category_data(data.url,json.dumps(data.data, ensure_ascii=False))
            ReportEnhancer.add_response_details(resp.status_code,resp.text)
        with allure.step("3. 接口响应断言"):
            assert_util.assert_contains(resp, data.data["code"])
        with allure.step("4. 数据库断言响应字段"):
            ReportEnhancer.add_sql_details(data.sql,data.data["code"])
            dbAssert.assert_row_exists(data.sql,params=(data.data["code"],),msg="数据库成功断言")
        with allure.step("5. 提取数据,接口关联"):
            VarUtil.set_var('category_code',data.data["code"])
            category_code = VarUtil.get_var('category_code')
            log.info(category_code)
            reslut = db.query_one(f"select id from sys_dictionary_category where code ='{category_code}'")
            log.info(reslut)
            VarUtil.set_var('category_id', reslut["id"])
            log.info(var_util.get_var('category_id'))
        with allure.step("6. 数据清理,防止数据污染"):
            pass





    @allure.story("字典目录")
    @allure.title("修改字典目录")
    @pytest.mark.parametrize("data",[_dict_all_data.get("update_category_success",{})],ids=['update_category_success'])
    def test_update_category_data(self,data):
        with allure.step("1. 从data中获取测试请求数据"):
            data = req_params_Collection(data)
            log.info(data)
            ReportEnhancer.add_request_details(url=data.url, method='put',
                                               params=(data.params, data.data, data.json))
        with allure.step("2. 调用请求接口"):
            resp = categoryapi.update_category_data(data.url,json.dumps(data.data, ensure_ascii=False))
            ReportEnhancer.add_response_details(resp.status_code,resp.text)
        with allure.step("3. 接口响应断言"):
            assert_util.assert_contains(resp, data.expected_data)
        with allure.step("4. 数据库断言响应字段"):
            # ReportEnhancer.add_sql_details(data.sql,data.sql_params)
            # dbAssert.assert_field_value(data.sql,params=(data.sql_params,))
            pass
        with allure.step("5. 提取数据,接口关联"):
            pass
        with allure.step("6. 数据清理,防止数据污染"):
            pass


    @allure.story("字典目录")
    @allure.title("删除字典目录")
    @pytest.mark.parametrize("data",[_dict_all_data.get("delete_category_success",{})],ids=['delete_category_success'])
    def test_delete_category_data(self,data):
        with allure.step("1. 从data中获取测试请求数据"):
            data = req_params_Collection(data)
            log.info(data)
            ReportEnhancer.add_request_details(url=data.url, method='delete',
                                               params=(data.params, data.data, data.json))
        with allure.step("2. 调用请求接口"):
            resp = categoryapi.delete_category_data(data.url,data.data)
            ReportEnhancer.add_response_details(resp.status_code,resp.text)
        with allure.step("3. 接口响应断言"):
            assert_util.assert_code(resp, data.expected_code)
        with allure.step("4. 数据库断言响应字段"):
            # ReportEnhancer.add_sql_details(data.sql,data.sql_params)
            # dbAssert.assert_row_not_exists(data.sql,params=(data.sql_params,))
            pass
        with allure.step("5. 提取数据,接口关联"):
            pass
        with allure.step("6. 数据清理,防止数据污染"):
            pass



