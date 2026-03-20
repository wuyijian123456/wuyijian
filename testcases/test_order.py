import allure
import json
from api.order_api import OrderApi
from core.assert_util import assert_util
from config.settings import DATA_DIR

# 读取JSON测试数据

try:
    with open(DATA_DIR / "order_data.json", "r", encoding="utf-8") as f:
        order_data = json.load(f)
except FileNotFoundError:
    # 异常1：文件不存在（最常见）
    print(f"错误：未找到文件 {DATA_DIR / 'order_data.json'}，请检查文件路径是否正确")
except json.JSONDecodeError:
    # 异常2：JSON 格式错误（比如语法错误、标点缺失）
    print(f"错误：{DATA_DIR / 'order_data.json'} 文件内容不是合法的 JSON 格式，请检查文件内容")
    order_data = {}
except PermissionError:
    # 异常3：没有文件读取权限
    print(f"错误：没有读取 {DATA_DIR / 'order_data.json'} 文件的权限，请检查文件权限设置")
    order_data = {}
except Exception as e:
    # 异常4：其他未预期的错误（兜底）
    print(f"读取订单数据时发生未知错误：{str(e)}")
    order_data = {}


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