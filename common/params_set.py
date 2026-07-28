from common.var_replace_util import var_util
from core.logger import log

def req_params_Collection(params_data):
    data ={}
    json ={}
    params_data = var_util.replace(params_data)
    # log.info(params_data)
    url = params_data.get("url")
    params = params_data.get("params", {})
    if "data" in params_data.keys():
        data = params_data.get("data",{})
        log.info(data)
    if "json" in params_data.keys():
        json = params_data.get("json",{})
        log.info(json)
    # cookie = params_data.get("cookie")
    expected_code = params_data.get("expected_code")
    expected_data = params_data.get("expected_data")
    sql = params_data.get("sql",{})
    sql_params = params_data.get("sql_params", {})
    filed = params_data.get("filed",{})
    log.info(f"参数集合：url：{url},params:{params}"
             f"expected_code:{expected_code},expected_data:{expected_data},sql:{sql},filed:{filed}")
    return url,params,data,json,expected_code,expected_data,sql,sql_params,filed