import pytest
from core.assert_util import assert_util
from core.logger import log
import allure
from core.report_enhancer import ReportEnhancer
from models.request_model.training_personnel_request import TrainingPersonnelRequest
from models.response_modes.training_personnel_response import TrainingPersonnelResponse, SelectTrainingPersonnelResponse
from nurse_api.training_personnel_api import TrainingPersonnelAPI
from factories.training_personnel_factory import TrainingPersonnelFactory, SelectTrainingPersonnelFactory
from pydantic import ValidationError
from datetime import datetime, timedelta


class TestTrainingPersonnel:
    """
    培训人员接口测试
    覆盖 25+ 个字段的各种场景
    """
    # ========== 正向用例 ==========

    def test_create_personnel_with_full_fields(self, training_personnel_api,db_client):
        """测试创建：所有字段完整"""
        with allure.step("1. 从data中获取测试请求数据"):
            request = TrainingPersonnelFactory.base_personnel()
            # 创建时 id 应为 None
            request.id = None
            log.info(f"请求参数：{request}")
            ReportEnhancer.add_request_details(url='/api/further/trainee/info', method='post', params=request.to_dict())
        with allure.step("2. 调用请求接口"):
            response = training_personnel_api.create_personnel(request)
            ReportEnhancer.add_response_details(response.status_code,response.json())
        with allure.step("3. 断言响应状态码"):
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == request.name
            assert_util.validate_response(data,TrainingPersonnelResponse)
        with allure.step("4. 数据库断言响应字段"):
            sql = "SELECT * FROM further_trainee_info WHERE id =%s"
            params = data['id']
            db_client.query_one(sql,params)
        with allure.step("5. 数据清理"):
            sql = "delete FROM further_trainee_info WHERE id =%s"
            params = data['id']
            db_client.execute(sql,(params,))




    def test_create_personnel_minimal(self,training_personnel_api,db_client):
        """测试创建：只有必填字段"""
        with allure.step("1. 从data中获取测试请求数据"):
            request = TrainingPersonnelFactory.minimal_personnel()
            ReportEnhancer.add_request_details(url='/api/further/trainee/info', method='post', params=request.to_dict())
        with allure.step("2. 调用请求接口"):
            response = training_personnel_api.create_personnel(request)
            ReportEnhancer.add_response_details(response.status_code, response.json())
        with allure.step("3. 断言响应状态码"):
            assert response.status_code == 200
            data = response.json()
            assert data["id"] is not None

        with allure.step("5. 数据清理"):
            sql = "delete FROM further_trainee_info WHERE id =%s"
            params = data['id']
            db_client.execute(sql,(params,))

    def test_update_personnel(self,training_personnel_api,db_client):
        """测试更新：修改姓名和手机号"""

        # 先创建
        create_req = TrainingPersonnelFactory.for_create()
        create_resp = training_personnel_api.create_personnel(create_req)
        created_id = create_resp.json()["id"]

        # 再更新
        update_req = TrainingPersonnelFactory.for_update(created_id)
        update_req.name = "李四"  # 修改姓名
        update_req.phoneNumber = "13900139000"  # 修改手机号

        response = training_personnel_api.update_personnel(update_req)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "李四"
        assert data["phoneNumber"] == "13900139000"

        with allure.step("5. 数据清理"):
            sql = "delete FROM further_trainee_info WHERE id =%s"
            params = data['id']
            db_client.execute(sql,(params,))

    def test_create_with_accommodation(self,training_personnel_api,db_client):
        """测试创建：是否住宿"""
        for accommodation in [True, False]:
            request = TrainingPersonnelFactory.with_accommodation(accommodation)
            request.id = None

            response = training_personnel_api.create_personnel(request)

            assert response.status_code == 200
            assert response.json()["isAccommodation"] == accommodation
            with allure.step("5. 数据清理"):
                sql = "delete FROM further_trainee_info WHERE id =%s"
                params = response.json()['id']
                db_client.execute(sql, (params,))


    @pytest.mark.parametrize("name", ["","张三","叶旭","信息有限公司"])
    def test_select_personnel(self,name,training_personnel_api):
        # 查询
        req = SelectTrainingPersonnelFactory.create_base_personnel(name)
        resp = training_personnel_api.select_personnel(req)
        assert resp.status_code == 200
        assert_util.validate_response(resp.json(),SelectTrainingPersonnelResponse)


    # ========== 反向用例（Pydantic 拦截） ==========

    def test_invalid_phone(self):
        """测试手机号格式错误（Pydantic 拦截）"""
        with pytest.raises(ValidationError) as exc:
            request = TrainingPersonnelFactory.invalid_phone_wrong_format()
        assert "string_pattern" in str(exc.value)


    # ========== 数据驱动测试 ==========

    @pytest.mark.parametrize("gender,expected", [
        ("男", "男"),
        ("女", "女")
    ])
    def test_gender_values(self, gender, expected,training_personnel_api,db_client):
        """数据驱动：测试所有合法的性别值"""
        request = TrainingPersonnelFactory.base_personnel()
        request.id = None
        request.gender = gender

        response = training_personnel_api.create_personnel(request)

        assert response.status_code == 200
        assert response.json()["gender"] == expected

        with allure.step("5. 数据清理"):
            sql = "delete FROM further_trainee_info WHERE id =%s"
            params = response.json()['id']
            db_client.execute(sql,(params,))


    @pytest.mark.parametrize("education", ["degree1", "degree2", "degree3", "degree4", "degree5"])
    def test_education_values(self, education,training_personnel_api,db_client):
        """数据驱动：测试所有学历"""
        request = TrainingPersonnelFactory.base_personnel()
        request.id = None
        request.education = education

        response = training_personnel_api.create_personnel(request)

        assert response.status_code == 200
        assert response.json()["education"] == education

        with allure.step("5. 数据清理"):
            sql = "delete FROM further_trainee_info WHERE id =%s"
            params = response.json()['id']
            db_client.execute(sql,(params,))



    #
    # # ========== 自动计算测试 ==========
    #
    # def test_auto_calculate_duration(self, token):
    #     """测试自动计算培训时长"""
    #     now = datetime.now()
    #     start_date = now - timedelta(days=10)
    #     end_date = now
    #
    #     # 不传 training_duration 和 training_days，让 Pydantic 自动计算
    #     request = TrainingPersonnelRequest(
    #         name="自动计算测试",
    #         unit_name="测试公司",
    #         phone_number="13800138000",
    #         training_start_date=start_date,
    #         training_end_date=end_date
    #         # 不传 training_duration 和 training_days
    #     )
    #
    #     # 断言自动计算成功
    #     assert request.training_days == 10  # 10天
    #     assert request.training_duration == 80  # 10天 * 8小时
    #
    # # ========== 批量创建测试 ==========
    #
    # def test_batch_create_personnel(self, token):
    #     """测试批量创建（5个人员）"""
    #     requests = []
    #     for i in range(5):
    #         req = TrainingPersonnelFactory.for_create()
    #         req.name = f"批量测试_{i + 1}"
    #         requests.append(req)
    #
    #     response = TrainingPersonnelAPI.batch_create_personnel(requests, token)
    #
    #     assert response.status_code == 200
    #     data = response.json()
    #     assert data["code"] == 0
    #     assert len(data["data"]["list"]) == 5