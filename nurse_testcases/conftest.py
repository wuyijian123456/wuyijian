import pymysql
import pytest
import os
from core.request import RequestHandler
from core.logger import log
from common.var_replace_util import var_util
from nurse_api.intern_api import InternManageApi,InternRotatiobApi
from nurse_api.user_api import User_api
from nurse_api.dictionary_api import Dictionaryapi, statisticsapi, categoryapi, CategoryItemApi

@pytest.fixture()
def InternManageApi(api_client):
    return InternManageApi(api_client)

@pytest.fixture()
def InternRotatiobApi(api_client):
    return InternRotatiobApi(api_client)

@pytest.fixture()
def generate_intern_id(InternManageApi):
    resp = InternManageApi.add_rotation_info(url='',params={})
    assert resp.status_code == 200
    record_id = resp.json()["data"]["id"]
    yield record_id
    try:
        InternManageApi.delete_intern_info(url='', params= record_id)
    except Exception as e:
        print(f"⚠️ 清理记录 {record_id} 失败: {e}")

@pytest.fixture(scope='function')
def user_api(api_client):
    return User_api(api_client)

@pytest.fixture()
def dictionary_api(api_client):
    return Dictionaryapi(api_client)


@pytest.fixture()
def statistics_api(api_client):
    return statisticsapi(api_client)

@pytest.fixture()
def category_api(api_client):
    return categoryapi(api_client)

@pytest.fixture()
def category_item_api(api_client):
    return CategoryItemApi(api_client)



