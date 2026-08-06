import requests
from requests import sessions
from config.env_config import get as env_get
from core.logger import log
from common.var_replace_util import var_util

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
}


class RequestHandler:
    """请求工具类：封装GET/POST/PUT/DELETE，自动处理URL、超时、日志"""
    def __init__(self):
        self.session = sessions.Session()

    def _send(self, method, url, **kwargs):
        """内部请求方法：统一处理URL、日志、异常"""
        full_url = env_get("base_url") + url if not url.startswith("http") else url
        headers = kwargs.pop("headers", {})
        headers = headers if isinstance(headers, dict) else {}
        merged = {**DEFAULT_HEADERS, **headers}
        runtime_cookie = var_util.get_var("cookie")
        if runtime_cookie:
            merged["cookie"] = runtime_cookie
        headers = merged
        kwargs.setdefault("timeout", env_get("timeout"))

        try:
            log.info(f"===== 开始请求 =====")
            log.info(f"请求方法: {method.upper()}")
            log.info(f"请求URL: {full_url}")
            log.info(f"请求类型: {headers['Content-Type']}")
            if "params" in kwargs:
                log.info(f"查询参数: {kwargs['params']}")
            if "data" in kwargs:
                log.info(f"表单参数: {kwargs['data']}")
            if "json" in kwargs:
                log.info(f"JSON参数: {kwargs['json']}")

            response = self.session.request(
                method=method,
                url=full_url,
                headers=headers,
                **kwargs
            )

            log.info(f"响应状态码: {response.status_code}")
            log.info(f"===== 请求结束 =====\n")
            return response

        except requests.exceptions.RequestException as e:
            log.error(f"请求失败: {str(e)}")
            raise

    def get(self, url, params=None, headers=None, **kwargs):
        return self._send("GET", url, params=params, headers=headers, **kwargs)

    def post(self, url, data=None, json=None, headers=None, **kwargs):
        return self._send("POST", url, data=data, json=json, headers=headers, **kwargs)

    def put(self, url, data=None, json=None, headers=None, **kwargs):
        return self._send("PUT", url, data=data, json=json, headers=headers, **kwargs)

    def delete(self, url, params=None, data=None, json=None, headers=None, **kwargs):
        return self._send("DELETE", url, params=params, data=data, json=json, headers=headers, **kwargs)

    def close_session(self):
        self.session.close()


req = RequestHandler()
