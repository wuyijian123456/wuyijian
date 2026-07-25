
import pymysql
import pytest
import os
from core.request import req
from core.logger import log
from common.var_replace_util import var_util





@pytest.fixture(scope="session",autouse=True)
def login_cookie():
    log.info("通过登录获取cookie")
    headers = {"cookie": ".AspNetCore.Antiforgery.VyLW6ORzMgk=CfDJ8JvsZNnSXPRBk_THcn9tuMUOxWQMdv0GklKMlQH82N0fJ1zJ_qNWGS39KoFL9BPD5YpcQp05km6SX1f6liwb9S4FLJYKamv-dBcZ7L-GzEvi2GjiP5VphtIPIzRBBm3RrHeSqKRyEaVMO4bm1fjHLhE"}
    response = req.post(url='/api/identity/login',params={"useCookies":"true"},json={"email":"admin","password":"Password123!"},
                        headers=headers)
    cookie = response.headers.get("Set-Cookie")
    var_util.set_var("cookie",cookie)
    yield cookie


# def pytest_addoption(parser):
#     # 不需要 default 参数了
#     parser.addoption("--env", action="store", help="运行环境：test, prod")







