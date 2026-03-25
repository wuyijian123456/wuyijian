from core.request import req
from core.logger import log

class PatientApi:
    """病人管理模块接口封装：获取病人列表"""

    @classmethod
    def get_patient_list(cls, token, url, dept_code, in_dept_state):
        """获取在科病人列表
        
        Args:
            token: 用户认证令牌
            url: 请求接口路径
            dept_code: 科室代码
            in_dept_state: 是否在科状态 ("true"/"false")
            
        Returns:
            API 响应对象
        """
        log.info("调用获取病人列表接口")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            "deptCode": dept_code,
            "inDeptState": in_dept_state
        }
        return req.get(url, params=params, headers=headers)