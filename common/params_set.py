from common.var_replace_util import var_util
from core.logger import log
from typing import Optional, Any,Dict
from dataclasses import dataclass
from copy import deepcopy
from typing import Dict, Any


@dataclass
class RequestParams:
    url: Optional[str] = None
    params: Dict[str, Any] = None
    data: Dict[str, Any] = None
    json: Dict[str, Any] = None
    expected_code: Optional[int] = None
    expected_data: Optional[Any] = None
    sql: Dict[str, Any] = None
    sql_params: Dict[str, Any] = None
    filed: Dict[str, Any] = None

    def __post_init__(self):
        # 确保所有字段都有默认值
        if self.params is None:
            self.params = {}
        if self.data is None:
            self.data = {}
        if self.json is None:
            self.json = {}
        if self.sql is None:
            self.sql = {}
        if self.sql_params is None:
            self.sql_params = {}
        if self.filed is None:
            self.filed = {}


def req_params_Collection(params_data):
    params_data = var_util.replace(params_data)

    result = RequestParams(
        url=params_data.get("url"),
        params=params_data.get("params", {}),
        expected_code=params_data.get("expected_code"),
        expected_data=params_data.get("expected_key"),
        sql=params_data.get("sql", {}),
        sql_params=params_data.get("sql_params", {}),
        filed=params_data.get("filed", {})
    )

    if "data" in params_data:
        result.data = params_data.get("data", {})
        log.info(result.data)
    if "json" in params_data:
        result.json = params_data.get("json", {})
        log.info(result.json)

    log.info(f"参数集合：url：{result.url},params:{result.params}\n"
             f"expected_code:{result.expected_code},expected_data:{result.expected_data},sql:{result.sql},filed:{result.filed}")

    return result


def deep_merge(base: Dict, updates: Dict) -> Dict:
    """
    递归深度合并字典
    规则：updates 中的键值对会覆盖 base，但对于嵌套字典会递归合并
    """
    result = deepcopy(base)
    for key, value in updates.items():
        if isinstance(value, dict) and key in result and isinstance(result[key], dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result

def compose_test_data(template: Dict, factory_obj: Dict, test_overrides: Dict = None) -> Dict:
    """
    三层数据合成器
    :param template: YAML/JSON 加载的基础模板
    :param factory_obj: 夹具/工厂返回的动态对象（如依赖ID、动态手机号）
    :param test_overrides: 测试用例级别的特定覆盖
    :return: 最终合成的测试数据
    """
    # 第一层：模板 -> 第二层：工厂对象（覆盖模板） -> 第三层：测试覆盖（覆盖工厂）
    data = deep_merge(template, factory_obj)
    if test_overrides:
        data = deep_merge(data, test_overrides)
    return data


