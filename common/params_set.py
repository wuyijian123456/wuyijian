from common.var_replace_util import var_util
from core.logger import log
from typing import Optional, Any,Dict
from dataclasses import dataclass

# def req_params_Collection(params_data):
#     data ={}
#     json ={}
#     params_data = var_util.replace(params_data)
#     # log.info(params_data)
#     url = params_data.get("url")
#     params = params_data.get("params", {})
#     if "data" in params_data.keys():
#         data = params_data.get("data",{})
#         log.info(data)
#     if "json" in params_data.keys():
#         json = params_data.get("json",{})
#         log.info(json)
#     expected_code = params_data.get("expected_code")
#     expected_data = params_data.get("expected_data")
#     sql = params_data.get("sql",{})
#     sql_params = params_data.get("sql_params", {})
#     filed = params_data.get("filed",{})
#     log.info(f"参数集合：url：{url},params:{params}"
#              f"expected_code:{expected_code},expected_data:{expected_data},sql:{sql},filed:{filed}")
#     return url,params,data,json,expected_code,expected_data,sql,sql_params,filed


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

    log.info(f"参数集合：url：{result.url},params:{result.params}"
             f"expected_code:{result.expected_code},expected_data:{result.expected_data},sql:{result.sql},filed:{result.filed}")

    return result


