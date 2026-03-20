import allure
import json
from api.order_api import OrderApi
from core.assert_util import assert_util
from config.settings import DATA_DIR

# 读取JSON测试数据


with open(DATA_DIR / "order_data.json", "r", encoding="utf-8") as f:
    order_data = json.load(f)


@allure.feature("订单模块")
class TestOrder:
    @allure.story("创建订单")
    @allure.title("正常创建订单")
    def test_create_order(self, login_token):
        """创建订单用例"""
        data = order_data["create_order_success"]
        resp = OrderApi.create_order(login_token, data["goods_id"], data["num"])

        assert_util.assert_code(resp, data["expected_code"])
        assert_util.assert_contains(resp, data["expected_msg"])

    @allure.story("查询订单")
    @allure.title("查询已创建的订单")
    def test_query_order(self, login_token, order_id):
        """查询订单用例"""
        resp = OrderApi.query_order(login_token, order_id)

        assert_util.assert_code(resp, 200)
        assert_util.assert_json_key(resp, "code", "msg", "data")
        assert_util.assert_json_value(resp, "data.order_id", order_id)

    @allure.story("取消订单")
    @allure.title("取消已创建的订单")
    def test_cancel_order(self, login_token, order_id):
        """取消订单用例"""
        resp = OrderApi.cancel_order(login_token, order_id)

        assert_util.assert_code(resp, 200)
        assert_util.assert_contains(resp, order_data["cancel_order_success"]["expected_msg"])