from core.logger import log
import pytest
from common.data_factory import data_factory
from common.params_set import deep_merge
from common.yaml_util import yaml_util
from nurse_api.intern_api import InternManageApi,InternRotationApi
from nurse_api.training_personnel_api import TrainingPersonnelAPI
from nurse_api.user_api import UserApi
from nurse_api.dictionary_api import DictionaryApi, StatisticsApi, CategoryApi, CategoryItemApi

@pytest.fixture(scope="module")
def intern_manage_api(api_client):
    return InternManageApi(api_client)

@pytest.fixture()
def intern_rotation_api(api_client):
    return InternRotationApi(api_client)

@pytest.fixture(scope="function")
def generate_intern_id(intern_manage_api,db_client):
    intern_template= yaml_util.read_yaml('intern_info_template.yaml',is_dir=True)
    log.info(f"{intern_template}")
    factory_data = data_factory.intern_info()
    final_data = deep_merge(intern_template['intern_info_params'],factory_data)
    log.info(f"{final_data}")
    resp = intern_manage_api.add_intern_info(url='/api/intern/info',params = final_data)
    assert resp.status_code == 200
    record_id = resp.json()["id"]
    yield record_id
    try:
        db_client.execute(sql="delete from intern_info where id = %s",params = record_id)
    except Exception as e:
        print(f"⚠️ 清理记录 {record_id} 失败: {e}")


@pytest.fixture(scope="module")
def generate_intern_model(intern_manage_api,db_client):
    intern_template= yaml_util.read_yaml('intern_info_template.yaml',is_dir=True)
    log.info(f"{intern_template}")
    factory_data = data_factory.intern_info()
    final_data = deep_merge(intern_template['intern_info_params'],factory_data)
    log.info(f"{final_data}")
    resp = intern_manage_api.add_intern_info(url='/api/intern/info',params = final_data)
    assert resp.status_code == 200
    record_model = resp.json()
    yield record_model
    try:
        db_client.execute(sql="delete from intern_info where id = %s",params = record_model['id'])
    except Exception as e:
        print(f"⚠️ 清理记录 {record_model['id']} 失败: {e}")

@pytest.fixture(scope='function')
def user_api(api_client):
    return UserApi(api_client)

@pytest.fixture()
def dictionary_api(api_client):
    return DictionaryApi(api_client)


@pytest.fixture()
def statistics_api(api_client):
    return StatisticsApi(api_client)

@pytest.fixture()
def category_api(api_client):
    return CategoryApi(api_client)

@pytest.fixture()
def category_item_api(api_client):
    return CategoryItemApi(api_client)


@pytest.fixture()
def training_personnel_api(api_client):
    return TrainingPersonnelAPI(api_client)



