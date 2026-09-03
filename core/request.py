from pathlib import Path
from typing import Optional

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
            log.info(f"请求类型: {self.session.headers}")
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
            response = self.post(url='/api/identity/login?useCookies=true', headers=self.cookie,
                                json={"email": self.username, "password":self.password},
                                )
            self.session.headers.update({"Cookie":self.cookie})
            log.info(self.session.headers)
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

    def post(self, url, params=None,data=None, json=None, headers=None, **kwargs):
        self._ensure_cookie_valid()
        return self._send("POST", url, params=params,data=data, json=json, headers=headers, **kwargs)

    def put(self, url, data=None, json=None, headers=None, **kwargs):
        self._ensure_cookie_valid()
        return self._send("PUT", url, data=data, json=json, headers=headers, **kwargs)

    def delete(self, url, params=None, data=None, json=None, headers=None, **kwargs):
        self._ensure_cookie_valid()
        return self._send("DELETE", url, params=params, data=data, json=json, headers=headers, **kwargs)

    def upload(self, url: str, file_path: str, field_name: str = "file",
               extra_data: Optional[dict] = None, **kwargs):
        """文件上传

        Args:
            path:       上传接口路径
            file_path:  本地文件路径
            field_name: 表单字段名
            extra_data: 额外的表单数据

        Example:
            biz = client.upload("/api/file/upload", "data/avatar.png")
        """
        full_url = self.base_url + url if not url.startswith("http") else url
        from common.upload_util import build_upload_file

        files = build_upload_file(file_path, field_name)
        # 上传时不设 Content-Type（让 requests 自动生成 multipart boundary）
        temp_headers = self.session.headers.copy()
        self.session.headers.pop("Content-Type", None)
        self.session.headers.update({"Cookie":self.cookie})
        self.session.headers = self.session.headers
        log.info(self.session.headers)
        try:
            return self.session.request(method="post", url=full_url, files=files, data=extra_data, **kwargs)
        finally:
            # 恢复默认 headers
            self.session.headers = temp_headers


    def download(self, path: str, save_path: str, **kwargs) -> str:
        """
        文件下载

        Args:
            path:下载接口路径
            save_path: 保存路径

        Returns:
            保存后的文件绝对路径

        Example:
            filepath = client.download("/api/file/download/test.pdf", "downloads/test.pdf")
        """
        url = self._build_url(path)
        save_path_obj = Path(save_path)
        save_path_obj.parent.mkdir(parents=True, exist_ok=True)

        if "timeout" not in kwargs:
            kwargs["timeout"] = max(self.timeout, 60)  # 下载超时至少 60s

        log.info("HTTP DOWNLOAD | {} → {}", path, save_path)

        resp = self.session.get(url, stream=True, **kwargs)
        resp.raise_for_status()

        total_size = int(resp.headers.get("content-length", 0))
        downloaded = 0

        with open(save_path_obj, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)

        log.info("HTTP DOWNLOAD | 完成 | {} bytes → {}", downloaded, save_path)
        return str(save_path_obj.resolve())

    def close_session(self):
        self.session.close()



