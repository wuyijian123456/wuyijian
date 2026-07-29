import requests
from requests import sessions
from config.settings import BASE_URL, TIMEOUT,DEFAULT_HEADERS
from core.logger import log
from common.var_replace_util import var_util



class RequestHandler:
    """请求工具类：封装GET/POST/PUT/DELETE，自动处理URL、超时、日志"""
    def __init__(self):
        self.session = sessions.Session()  # 保持会话（自动处理Cookie）

    def _send(self, method, url, **kwargs):
        """内部请求方法：统一处理URL、日志、异常"""
        # 拼接完整URL
        full_url = BASE_URL + url if not url.startswith("http") else url
        # 合并默认头和自定义头
        # 设置默认头，并在每次请求时动态读取 cookie
        headers = kwargs.pop("headers", {})
        headers = headers if isinstance(headers, dict) else {}
        merged = {**DEFAULT_HEADERS, **headers}
        runtime_cookie = var_util.get_var("cookie")
        if runtime_cookie:
            merged["cookie"] = runtime_cookie
        headers = merged
        # 设置超时
        kwargs.setdefault("timeout", TIMEOUT)

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

            # 发送请求
            response = self.session.request(
                method=method,
                url=full_url,
                headers=headers,
                **kwargs
            )
            # response.raise_for_status()  # 非200状态码抛出异常

            log.info(f"响应状态码: {response.status_code}")
            log.info(f"响应内容: {response.text}")
            log.info(f"===== 请求结束 =====\n")
            return response

        except requests.exceptions.RequestException as e:
            log.error(f"请求失败: {str(e)}")
            raise  # 抛出异常，让用例捕获

    def get(self, url, params=None, headers=None, **kwargs):
        """GET请求"""
        return self._send("GET", url, params=params, headers=headers, **kwargs)

    def post(self, url, data=None, json=None, headers=None, **kwargs):
        """POST请求"""
        return self._send("POST", url, data=data, json=json, headers=headers, **kwargs)

    def put(self, url, data=None, json=None, headers=None, **kwargs):
        """PUT请求"""
        return self._send("PUT", url, data=data, json=json, headers=headers, **kwargs)

    def delete(self, url,params=None,data=None,json=None, headers=None, **kwargs):
        """DELETE请求"""
        return self._send("DELETE", url,params=params, data=data, json=json, headers=headers, **kwargs)


    def close_session(self):
        """关闭会话"""
        self.session.close()

# 全局请求实例（避免重复创建）
req = RequestHandler()