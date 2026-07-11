import pymysql
import pytest
import os
from core.request import req
from core.logger import log
from common.var_replace_util import var_util




@pytest.fixture(scope="session")
def login_cookie():
    log.info("通过登录获取cookie")
    headers = {"cookie": ".AspNetCore.Antiforgery.VyLW6ORzMgk=CfDJ8JvsZNnSXPRBk_THcn9tuMXs8pZcbHqVFas9GAbfe5ApJirZXi3Qb0hBNmdwVq8INe1qXQjSlvC2ojcheED58rhF0sChRmlvrXt0oHDziYMMkEUqcYdPyNAFD98AzR17wswYbhPFDf0yciZncKYGa4I"}
    response = req.post(url='/api/identity/login',params={"useCookies":"true"},json={"email":"admin","password":"Password123!"},
                        headers=headers)
    cookie = response.headers.get("set-cookie")
    var_util.set_var("cookie",cookie)
    yield cookie


