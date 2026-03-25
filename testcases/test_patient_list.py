import allure
import pytest
from api.patient_api import PatientApi
from core.assert_util import assert_util
from common.yaml_util import yaml_util
from common.var_replace_util import var_util
from common.cleanup import CleanUpManager
from core.retry import retry
from core.error_handler import on_failure
from core.report_enhancer import performance_monitor

# 读取病人列表测试数据
try:
    patient_info = yaml_util.read_yaml("get_patient_list.yaml")["get_patient_list"]
except Exception as e:
    print(f"读取病人列表配置文件失败：{str(e)}")
    patient_info = {}


@allure.feature("病人列表管理")
class TestPatientList:
    """病人列表查询测试类"""
    
    @allure.story("根据科室查询病人列表")
    @allure.title("查询在科病人列表")
    @pytest.mark.smoke
    @pytest.mark.P0
    @retry(max_attempts=3, delay=1)
    @on_failure
    @performance_monitor
    def test_get_patient_list(self, login_token, test_context):
        """根据科室查询在科病人列表"""
        test_name = test_context["test_name"]
        
        with allure.step("1. 准备请求参数"):
            dept_code = patient_info.get("deptCode", "")
            in_dept_state = patient_info.get("inDeptState", "true")
            log.info(f"科室代码：{dept_code}")
            log.info(f"在科状态：{in_dept_state}")
            allure.attach(name="请求参数", body=f"科室代码：{dept_code}, 在科状态：{in_dept_state}")
        
        with allure.step("2. 调用查询病人列表接口"):
            response = PatientApi.get_patient_list(
                token=login_token,
                url=patient_info.get("url", ""),
                dept_code=dept_code,
                in_dept_state=in_dept_state
            )
            allure.attach(name="响应状态码", body=str(response.status_code))
        
        with allure.step("3. 断言响应状态码"):
            assert_util.assert_code(response, patient_info.get("expected_code", 200))
        
        with allure.step("4. 断言响应包含成功消息"):
            assert_util.assert_contains(response, patient_info.get("expected_msg", "操作成功"))
            allure.attach(name="预期消息", body=patient_info.get("expected_msg", "操作成功"))
        
        # 注册清理任务（如果有需要清理的数据）
        CleanUpManager.register(
            test_name,
            lambda: print(f"清理测试 {test_name} 的数据")
        )