from core.request import req
from core.logger import log
from common import yaml_util

class OrderApi:
    """订单模块接口封装：创建订单、查询订单、取消订单"""
    # CREATE_ORDER_URL = "/order/create"
    # QUERY_ORDER_URL = "/order/query"
    # CANCEL_ORDER_URL = "/order/cancel"

    @classmethod
    def create_order(cls,URL, token, goods_id, num):
        """创建订单"""
        log.info("调用创建订单接口")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        data = {
            "goods_id": goods_id,
            "num": num
        }
        return req.post(URL, json=data, headers=headers)

    @classmethod
    def query_order(cls, URL, token, order_id):
        """查询订单"""
        log.info("调用查询订单接口")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            "order_id": order_id
        }
        return req.get(URL, params=params, headers=headers)

    @classmethod
    def cancel_order(cls, URL,token, order_id):
        """取消订单"""
        log.info("调用取消订单接口")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        data = {
            "order_id": order_id
        }
        return req.post(URL, json=data, headers=headers)