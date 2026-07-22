from core.assert_util import assert_util,db
from nurse_api.dictionary_api import Dictionaryapi
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
log.info(_dict_yaml_path)

@allure.suite("字典管理123")
@allure.feature("字典管理456")
class Testuser:
    @allure.story("获取字典")
    @allure.title("根据codes获取字典")
    @pytest.mark.parametrize("data",[_dict_all_data.get("dictionary_item_success",{})],ids=['dictionary_success'])
    def test_current_user_permissions(self,data):
        with allure.step("1. 从data中获取测试请求数据"):
            url, params, data, json, cookie, expected_code, expected_data, sql, sql_params, filed = req_params_Collection(
                data)
            #处理参数
            # params = [('categoryCodes', code) for code in params.get('categoryCodes',{})]
            ReportEnhancer.add_request_details(url=url, method='get', headers={"cookie": cookie},
                                               params=(params, data, json))
        with allure.step("2. 调用请求接口"):
            resp = Dictionaryapi.get_dict_by_allcode(url,params)
            ReportEnhancer.add_response_details(resp.status_code,resp.json())
        with allure.step("3. 断言响应状态码"):
            assert_util.assert_code(resp, expected_code)
        with allure.step("4. 数据库断言响应字段"):
            pass
