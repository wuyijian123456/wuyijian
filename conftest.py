import pytest
from api.user_api import UserApi
from core.logger import log
from common.yaml_util import yaml_util

# 作用域：session（整个测试会话只执行一次）
@pytest.fixture(scope="session")
def login_token():
    """登录获取token（全局复用）"""
    log.info("===== 前置操作：登录获取token =====")
    # 读取登录成功数据
    login_data = yaml_util.read_yaml("user_data.yaml")["login_success"]
    resp = UserApi.login(login_data["username"], login_data["password"])
    # 提取token
    token = resp.json()["access_token"]
    log.info(f"获取到token：{token}")
    yield token  # 返回token给用例
    log.info("===== 后置操作：清理登录态 =====")

# 作用域：function（每个用例执行一次）
@pytest.fixture(scope="function")
def order_id(login_token):
    """创建订单（每个订单用例前置）"""
    log.info("===== 前置操作：创建测试订单 =====")
    resp = UserApi.create_order(login_token, 1001, 1)
    order_id = resp.json()["data"]["order_id"]
    yield order_id
    log.info(f"===== 后置操作：删除测试订单 {order_id} =====")