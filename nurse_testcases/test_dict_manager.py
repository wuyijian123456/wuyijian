from core.assert_util import assert_util,dbAssert
from nurse_api.dictionary_api import Dictionaryapi, statisticsapi
import allure
import pytest
import os
from common.yaml_util import yaml_util
from common.var_replace_util import var_util
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
            ReportEnhancer.add_request_details(url=data['url'], method='get',
                                               params=(data['params'], data.get('data',{}), data.get('json',{})))
        with allure.step("2. 调用请求接口"):
            resp = Dictionaryapi.get_dict_by_allcode(data.get('url'),data['params'])
            ReportEnhancer.add_response_details(resp.status_code,resp.json())
        with allure.step("3. 断言响应状态码"):
            assert_util.assert_code(resp, data.get('expected_code',{}))
        with allure.step("4. 数据库断言响应字段"):
            ReportEnhancer.add_sql_details(data.get('sql',{}),data.get('sql_params',{}))
            pass



@allure.suite("字典管理123")
@allure.feature("字典管理456")
class TestStatistics:
    @allure.story("获取字典")
    @allure.title("根据codes获取字典")
    @pytest.mark.parametrize("data",[_dict_all_data.get("statistics_success",{})],ids=['dictionary_success'])
    def test_Statistics_data(self,data):
        with allure.step("1. 从data中获取测试请求数据"):
            ReportEnhancer.add_request_details(url=data['url'], method='get',
                                               params=(data['params'], data.get('data',{}), data.get('json',{})))
        with allure.step("2. 调用请求接口"):
            resp = statisticsapi.get_statistics_data(data.get('url'),data['params'])
            ReportEnhancer.add_response_details(resp.status_code,resp.json())
        with allure.step("3. 断言响应状态码"):
            assert_util.assert_code(resp, data.get('expected_code',{}))
        with allure.step("4. 数据库断言响应字段"):
            ReportEnhancer.add_sql_details(data.get('sql',{}),data.get('sql_params',{}))
            dbAssert.assert_row_exists(data.get('sql',{}),params=(data.get('sql_params'),))

