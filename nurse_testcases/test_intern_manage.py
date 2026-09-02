import json

from common.db_util import DBUtil
from common.response_extractor import ResponseExtractor
from common.data_factory import data_factory
from core.assert_util import assert_util
import allure
import pytest
import os
from common.yaml_util import yaml_util
from common.var_replace_util import var_util, VarUtil
from core.logger import log
from common.params_set import req_params_Collection, deep_merge, compose_test_data
from core.report_enhancer import ReportEnhancer
from models.response_modes.intern_response_models import InternList,InternDetailResponse,InternRotationResponse

# 加载实习生模块测试数据

intern_yaml_path = os.path.join('intern', "test_intern.yaml")
intern_rotation_yaml_path = os.path.join('intern', "test_intern_rotation.yaml")
intern_all_data = yaml_util.read_yaml(intern_yaml_path)
intern_rotation_all_data = yaml_util.read_yaml(intern_rotation_yaml_path)
log.info(f"{intern_all_data},{intern_rotation_all_data}")


@allure.suite("实习生管理")
@allure.feature("实习生管理")

class Test_intern_manage:

    @allure.story("实习生人员列表信息")
    @allure.title("根据条件获取实习生人员列表信息")
    @pytest.mark.parametrize('data',[intern_all_data.get("get_intern_list_success",{})],
                             ids =["get_intern_list_success"])
    def test_get_intern_info(self,intern_manage_api,generate_intern_id,db_assert,data):
        with allure.step("1. 从data中获取测试请求数据"):
            data = req_params_Collection(data)
            ReportEnhancer.add_request_details(url=data.url,method='get',params=data.params)

        with allure.step("2. 调用请求接口"):
            resp = intern_manage_api.get_intern_info(data.url,data.params)
            ReportEnhancer.add_response_details(resp.status_code,resp.json())
            id = resp.json()["items"][0]['id']
        with allure.step("3. 断言响应状态码"):
            assert_util.assert_code(resp, data.expected_code)
            assert_util.assert_contains(resp,data.expected_data)
            assert_util.validate_response(resp.json(),InternList)
        with allure.step("4. 数据库断言响应字段"):
            db_assert.assert_row_exists("select * from intern_info where id =%s",params=id,msg="数据不存在")
            ReportEnhancer.add_sql_details(data.sql,data.sql_params)

    @allure.story("实习生人员列表信息")
    @allure.title("根据关键字条件获取实习生人员列表信息")
    @pytest.mark.parametrize('data',[intern_all_data.get("get_intern_list_by_keyword_name",{}),intern_all_data.get("get_intern_list_by_keyword_schoolname",{})],
                             ids =["get_intern_list_by_keyword","get_intern_list_by_keyword_schoolname"])
    def test_get_intern_info_by_keyword(self,intern_manage_api,db_assert, data):
        with allure.step("1. 从data中获取测试请求数据"):
            data = req_params_Collection(data)
            ReportEnhancer.add_request_details(url=data.url,method='get',params=data.params)

        with allure.step("2. 调用请求接口"):
            resp = intern_manage_api.get_intern_info(data.url,data.params)
            ReportEnhancer.add_response_details(resp.status_code,resp.json())
            total = resp.json()["totalCount"]
        with allure.step("3. 断言响应状态码"):
            assert_util.assert_code(resp, data.expected_code)
            assert_util.assert_contains(resp, data.expected_data)
            assert_util.validate_response(resp.json(),InternList)
        with allure.step("4. 数据库断言响应字段"):
            db_assert.assert_count_equal(data.sql,data.sql_params,total,"总数不匹配")
            ReportEnhancer.add_sql_details(data.sql,data.sql_params)


    @allure.story("实习生人员列表信息")
    @allure.title("根据id条件获取实习生人员列表信息")
    @pytest.mark.parametrize('data',[intern_all_data.get("get_intern_info_by_id",{})],ids =["get_intern_info_by_id"])
    def test_get_intern_info_by_id(self,intern_manage_api,db_assert,generate_intern_id, data):
        with allure.step("1. 从data中获取测试请求数据"):
            data = req_params_Collection(data)
            data.params["id"] = generate_intern_id
            data.expected_data = generate_intern_id
            ReportEnhancer.add_request_details(url=data.url,method='get',params=data.params)
        with allure.step("2. 调用请求接口"):
            resp = intern_manage_api.get_intern_info(data.url,data.params)
            ReportEnhancer.add_response_details(resp.status_code,resp.json())
        with allure.step("3. 断言响应状态码"):
            assert_util.assert_code(resp, data.expected_code)
            assert_util.assert_contains(resp,data.expected_data)
            assert_util.validate_response(resp.json(),InternDetailResponse)
        with allure.step("4. 数据库断言响应字段"):
            db_assert.assert_row_exists("select * from intern_info where id =%s",params=generate_intern_id,msg="数据不存在")
            ReportEnhancer.add_sql_details(data.sql,data.sql_params)


    @allure.story("实习生人员列表信息")
    @allure.title("新增实习生人员信息")
    @pytest.mark.parametrize('data',[intern_all_data.get("add_intern_info_success",{})],ids=['add_intern_info_success'])
    def test_add_intern_info(self, data,intern_manage_api,db_assert):
        with allure.step("1. 从data中获取测试请求数据"):
            data = req_params_Collection(data)
            intern_template = yaml_util.read_yaml('intern_info_template.yaml', is_dir=True)
            factory_data = data_factory.intern_info()
            data.params = compose_test_data(intern_template['intern_info_params'],factory_data)
            ReportEnhancer.add_request_details(url=data.url,method='post',params=data.params)

        with allure.step("2. 调用请求接口"):
            resp = intern_manage_api.add_intern_info(data.url,data.params)
            ReportEnhancer.add_response_details(resp.status_code,resp.json())

        with allure.step("3. 断言响应状态码"):
            assert_util.assert_code(resp, data.expected_code)
            assert_util.validate_response(resp.json(), InternDetailResponse)
            data.sql_params = resp.json()["id"]

        with allure.step("4. 数据库断言响应字段"):
            db_assert.assert_row_exists(data.sql,data.sql_params,"数据库不存在该数据")
            ReportEnhancer.add_sql_details(data.sql,data.sql_params)



    @allure.story("实习生人员列表信息")
    @allure.title("编辑实习生人员信息")
    @pytest.mark.parametrize('data',[intern_all_data.get("update_intern_info_success")],ids=['update_intern_info_success'])
    def test_update_intern_info(self, data,intern_manage_api,generate_intern_model,db_assert):
        with allure.step("1. 从data中获取测试请求数据"):
            data = req_params_Collection(data)
            factory_obj = data_factory.random_school_major()
            log.info(factory_obj.get("schoolName"))
            log.info(factory_obj.get("major"))
            data.params = compose_test_data(generate_intern_model,factory_obj)
            data.expected_data = factory_obj.get("major")
            ReportEnhancer.add_request_details(url=data.url,method='put',params=data.params)

        with allure.step("2. 调用请求接口"):
            resp = intern_manage_api.update_intern_info(data.url,data.params)
            ReportEnhancer.add_response_details(resp.status_code,resp.json())

        with allure.step("3. 断言响应状态码"):
            assert_util.assert_code(resp, data.expected_code)
            assert_util.assert_contains(resp, data.expected_data)
            assert_util.validate_response(resp.json(), InternDetailResponse)

        with allure.step("4. 数据库断言响应字段"):
            # db_assert.assert_field_value(data.sql,data.sql_params,filed =data.field,msg="数据库中该字段的值不匹配")
            # ReportEnhancer.add_sql_details(data.sql,data.sql_params)
            pass



    @allure.story("实习生人员列表信息")
    @allure.title("删除实习生人员信息")
    @pytest.mark.parametrize('data',[intern_all_data.get("end_intern_info_success")],ids=['end_intern_info_success'])
    def test_delete_intern_info(self, data,intern_manage_api,generate_intern_id,db_client):
        with allure.step("1. 从data中获取测试请求数据"):
            data = req_params_Collection(data)
            data.params["id"] = generate_intern_id
            data.expected_data = generate_intern_id
            ReportEnhancer.add_request_details(url=data.url,method='post',params=data.params)

        with allure.step("2. 调用请求接口"):
            resp = intern_manage_api.end_intern_info(data.url,data.params,data.json)
            ReportEnhancer.add_response_details(resp.status_code)

        with allure.step("3. 断言响应状态码"):
            log.info(f"{resp.text}, {data.expected_code}")
            assert_util.assert_code(resp, data.expected_code)

            # assert_util.assert_contains(resp, data.expected_data)

        with allure.step("4. 数据库断言响应字段"):
            # db_assert.assert_row_not_exists(data.sql,data.sql_params,"删除后，数据库中还存在")
            # ReportEnhancer.add_sql_details(data.sql,data.sql_params)
            pass

        with allure.step("5. 清理测试数据"):
            sql = "delete from intern_info WHERE id = %s"
            params = data.params["id"]
            db_client.execute(sql,(params,))


    @allure.story("实习生人员列表信息")
    @allure.title("删除实习生人员信息")
    @pytest.mark.parametrize('data',[intern_all_data.get("end_two_intern_info_success")],ids=['end_two_intern_info_success'])
    def test_two_delete_intern_info(self, data,intern_manage_api,generate_intern_id,db_client):
        with allure.step("1. 从data中获取测试请求数据"):
            data = req_params_Collection(data)
            data.params["id"] = generate_intern_id
            data.expected_data = data.params["id"]
            ReportEnhancer.add_request_details(url=data.url,method='post',params=data.params)

        with allure.step("2. 调用请求接口"):
            resp = intern_manage_api.end_intern_info(data.url,data.params,data.json)
            assert resp.status_code == 200
            resp = intern_manage_api.end_intern_info(data.url, data.params, data.json)
            ReportEnhancer.add_response_details(resp.status_code)

        with allure.step("3. 断言响应状态码"):
            log.info(f"{resp.text}, {data.expected_code}")
            assert_util.assert_code(resp, data.expected_code)

            # assert_util.assert_contains(resp, data.expected_data)

        with allure.step("4. 数据库断言响应字段"):
            # db_assert.assert_row_exists(data.sql,data.sql_params,"删除后，数据库中还存在")
            # ReportEnhancer.add_sql_details(data.sql,data.sql_params)
            pass
        with allure.step("5. 清理测试数据"):
            sql = "delete from intern_info WHERE id = %s"
            params = data.params["id"]
            db_client.execute(sql,(params,))




@allure.suite("实习生轮转记录")
@allure.feature("实习生轮转记录")
class Test_intern_rotation:
    @allure.story("实习生轮转记录")
    @allure.title("获取实习生轮转记录")
    @pytest.mark.parametrize('data', [intern_rotation_all_data.get("get_intern_rotation_list_success")], ids=['get_intern_rotation_list_success'])
    def test_get_intern_rotation_info(self, data,generate_intern_id,intern_rotation_api):
        with allure.step("1. 从data中获取测试请求数据"):
            data = req_params_Collection(data)
            data.params['internId'] = generate_intern_id
            ReportEnhancer.add_request_details(url=data.url, method='get', params=data.params)

        with allure.step("2. 调用请求接口"):
            resp = intern_rotation_api.get_intern_rotation_info(data.url, data.params)
            ReportEnhancer.add_response_details(resp.status_code, resp.json())

        with allure.step("3. 断言响应状态码"):
            assert_util.assert_code(resp, data.expected_code)


        with allure.step("4. 数据库断言响应字段"):
            pass
            # ReportEnhancer.add_sql_details(data.sql, data.sql_params)

    @allure.story("实习生轮转记录")
    @allure.title("新增实习生轮转记录")

    @pytest.mark.parametrize('data', [intern_rotation_all_data.get("add_intern_rotation_success")], ids=['add_intern_rotation_success'])
    def test_add_intern_rotation_info(self, data,intern_rotation_api,generate_intern_id,db_assert,db_client):
        with allure.step("1. 从data中获取测试请求数据"):
            data = req_params_Collection(data)
            data.params = data_factory.create_rotation_req_data()
            data.params['internId'] = generate_intern_id
            ReportEnhancer.add_request_details(url=data.url, method='post',  params=data.params)

        with allure.step("2. 调用请求接口"):
            resp = intern_rotation_api.add_intern_rotation_info(data.url, data.params)
            ReportEnhancer.add_response_details(resp.status_code, resp.json())

        with allure.step("3. 断言响应状态码"):
            assert_util.assert_code(resp, data.expected_code)
            assert_util.validate_response(resp.json(),InternRotationResponse)


        with allure.step("4. 数据库断言响应字段"):
            data.sql_params = resp.json()['id']
            db_assert.assert_row_exists(data.sql, data.sql_params, "数据库不存在该数据")
            ReportEnhancer.add_sql_details(data.sql, data.sql_params)

        with allure.step("5. 清理测试数据"):
            sql = "DELETE FROM intern_rotation_record WHERE id =%s"
            params = resp.json()['id']
            db_client.execute(sql,(params,))

    @allure.story("实习生轮转记录")
    @allure.title("编辑实习生轮转记录")
    @pytest.mark.parametrize('data', [intern_rotation_all_data.get("update_intern_rotation_success")], ids=['update_intern_rotation_success'])
    def test_update_intern_rotation_info(self, data, intern_rotation_api,generate_intern_id,db_client):
        with allure.step("1. 从data中获取测试请求数据"):
            data = req_params_Collection(data)
            data.params = data_factory.create_rotation_req_data()
            data.params['internId'] = generate_intern_id
            ReportEnhancer.add_request_details(url=data.url, method='put',  params=data.params)

        with allure.step("2. 调用请求接口"):
            # 新增轮转记录
            resp = intern_rotation_api.add_intern_rotation_info(data.url, data.params)
            assert resp.status_code == 200
            data.params['id'] = resp.json()['id']
            # 编辑轮转记录
            data.params['deptCode'] = '1151'
            data.params['mentor'] = '101'
            resp = intern_rotation_api.update_intern_rotation_info(data.url, data.params)
            ReportEnhancer.add_response_details(resp.status_code, resp.json())

        with allure.step("3. 断言响应状态码"):
            assert_util.assert_code(resp, data.expected_code)
            assert_util.validate_response(resp.json(),InternRotationResponse)

        with allure.step("4. 数据库断言响应字段"):
            sql = "SELECT * FROM intern_rotation_record WHERE id =%s"
            params = data.params['id']
            filed = db_client.query(sql=sql,params=(params,))
            assert filed[0]['dept_code'] == '1151'
            assert filed[0]['mentor'] == '101'
            ReportEnhancer.add_sql_details(sql, params = None,result = filed)

        with allure.step("5. 清理测试数据"):
            sql = "DELETE FROM intern_rotation_record WHERE id =%s"
            params = resp.json()['id']
            db_client.execute(sql,(params,))

    @allure.story("实习生轮转记录")
    @allure.title("删除实习生轮转记录")
    @pytest.mark.parametrize('data', [intern_rotation_all_data.get("delete_intern_rotation_success")], ids=['delete_intern_rotation_success'])
    def test_delete_intern_rotation_info(self, data,intern_rotation_api,generate_intern_id,db_assert):
        with allure.step("1. 从data中获取测试请求数据"):
            data = req_params_Collection(data)
            data.params = data_factory.create_rotation_req_data()
            data.params['internId'] = generate_intern_id
            ReportEnhancer.add_request_details(url=data.url, method='delete', params=data.params)

        with allure.step("2. 调用请求接口"):
            #新增轮转记录
            resp = intern_rotation_api.add_intern_rotation_info(data.url, data.params)
            assert resp.status_code == 200
            data.params['id'] = resp.json()['id']
            resp = intern_rotation_api.delete_intern_rotation_info(data.url, data.params)
            assert resp.status_code == 200
            ReportEnhancer.add_response_details(resp.status_code)

        with allure.step("3. 断言响应状态码"):
            assert_util.assert_code(resp, data.expected_code)

        with allure.step("4. 数据库断言响应字段"):
            data.sql_params = data.params['id']
            db_assert.assert_row_not_exists(data.sql, data.sql_params, "删除后，数据库中还存在")
            ReportEnhancer.add_sql_details(data.sql, data.sql_params)
