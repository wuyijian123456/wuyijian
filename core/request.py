import requests
from requests import sessions
from core.logger import log


class RequestHandler:
    """请求工具类：封装GET/POST/PUT/DELETE，自动处理URL、超时、日志"""
    def __init__(self,base_url,username,password,timeout,cookie,default_headers):
        self.session = sessions.Session()
        self.base_url = base_url
        self.cookie = cookie
        self.session.headers = default_headers
        self.username = username
        self.password = password
        self.timeout = timeout

    def _send(self, method, url, **kwargs):
        """内部请求方法：统一处理URL、日志、异常"""
        full_url = self.base_url + url if not url.startswith("http") else url
        headers = kwargs.pop("headers", {})
        headers = headers if isinstance(headers, dict) else {}
        self.session.headers = {**self.session.headers, **headers}
        kwargs.setdefault("timeout", self.timeout)
        try:
            log.info(f"===== 开始请求 =====")
            log.info(f"请求方法: {method.upper()}")
            log.info(f"请求URL: {full_url}")
            log.info(f"请求类型: {self.session.headers['Content-Type']}")
            if "params" in kwargs:
                log.info(f"查询参数: {kwargs['params']}")
            if "data" in kwargs:
                log.info(f"表单参数: {kwargs['data']}")
            if "json" in kwargs:
                log.info(f"JSON参数: {kwargs['json']}")

            response = self.session.request(
                method=method,
                url=full_url,
                headers=self.session.headers,
                **kwargs
            )

            log.info(f"响应状态码: {response.status_code}")
            log.info(f"===== 请求结束 =====\n")
            return response

        except requests.exceptions.RequestException as e:
            log.error(f"请求失败: {str(e)}")
            raise

    def login_cookie(self):
        try:
            log.info("通过登录获取cookie")
            response = self.post(url='/api/identity/login?useCookies=true', headers = self.cookie,
                                json={"email": self.username, "password":self.password},
                                )
            self.cookie = {"cookie": response.headers.get("Set-Cookie")}
            self.session.headers.update(self.cookie)
            log.info("✅ cookie 获取成功")
        except Exception as e:
            log.info("---------------登录失败---------------")
            raise e

    def _ensure_cookie_valid(self):
        """检查 cookie 是否有效"""
        if not self.cookie:
            self.login_cookie()

    def get(self, url, params=None, headers=None, **kwargs):
        self._ensure_cookie_valid()
        return self._send("GET", url, params=params, headers=headers, **kwargs)

    def post(self, url, data=None, json=None, headers=None, **kwargs):
        self._ensure_cookie_valid()
        return self._send("POST", url, data=data, json=json, headers=headers, **kwargs)

    def put(self, url, data=None, json=None, headers=None, **kwargs):
        self._ensure_cookie_valid()
        return self._send("PUT", url, data=data, json=json, headers=headers, **kwargs)

    def delete(self, url, params=None, data=None, json=None, headers=None, **kwargs):
        self._ensure_cookie_valid()
        return self._send("DELETE", url, params=params, data=data, json=json, headers=headers, **kwargs)

    def close_session(self):
        self.session.close()



