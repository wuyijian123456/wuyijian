import pytest
import os
import json

from common.var_replace_util import var_util
from config.env_config import set_active_env
from core.logger import log
from core.request import RequestHandler
from common.cleanup import CleanUpManager
from common.db_util import DBUtil
from core.assert_util import DatabaseAssert


# 测试结果存储
test_results = []

# ==================== 命令行选项 ====================
def pytest_addoption(parser):
    """添加自定义命令行选项"""
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="运行环境：test, prod"
    )
    parser.addoption(
        "--retry",
        action="store",
        type=int,
        default=0,
        help="失败重试次数"
    )
    parser.addoption(
        "--tags",
        action="store",
        default="",
        help="运行指定标签的测试用例"
    )
    parser.addoption(
        "--output",
        action="store",
        default="test_results.json",
        help="测试结果输出文件路径"
    )


def pytest_configure(config):
    """初始化环境配置"""
    env = config.getoption("--env", default="uat")
    config.env = env
    config.env_config = set_active_env(env)
    retry_count = config.getoption("--retry", default=0)
    os.environ["PYTEST_RETRY"] = str(retry_count)

    log.info(f"环境配置: {env}")
    log.info(f"环境配置: {config.env_config}")
    log.info(f"重试次数: {retry_count}")

# ==================== 夹具 ====================

@pytest.fixture(scope ='session')
def env(request):
    return request.config.env

@pytest.fixture(scope ='session')
def env_config(request):
    return request.config.env_config

@pytest.fixture(scope ='session')
def env_config_mysql(request):
    return request.config.env_config['mysql']

@pytest.fixture(scope ='session')
def retry_count(request):
    return int(os.environ.get("PYTEST_RETRY", "0"))


@pytest.fixture(scope ='session')
def api_client(env_config):
    """全局
    ApiClient
    fixture
    整个测试会话只初始化一次，Token
    自动管理
    """
    base_url = env_config["base_url"]
    username = env_config["username"]
    password = env_config["password"]
    timeout = env_config["timeout"]
    Cookie = env_config["Cookie"]
    default_headers = env_config["default_headers"]
    client = RequestHandler(base_url,username,password,timeout,Cookie,default_headers)
    client.login_cookie()
    return client


@pytest.fixture(scope ='session')
def db_client(env_config_mysql):
    db = DBUtil(env_config_mysql)
    yield db
    db.close()

@pytest.fixture(scope ='session')
def db_assert(db_client):
    return DatabaseAssert(db_client)




# ==================== 全局 Fixture ====================


@pytest.fixture(scope="function",autouse=True)
def test_context(request):
    """测试上下文管理器"""
    test_name = request.node.name
    log.info(f"\n{'='*60}")
    log.info(f"开始执行测试：{test_name}")
    log.info(f"{'='*60}")
    yield {"test_name": test_name}
    var_util.clear_test_vars(test_name)
    CleanUpManager.execute_for_test(test_name)
    log.info(f"测试完成：{test_name}\n")


# ==================== Hook 函数 ====================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """捕获测试结果"""
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call':
        test_name = item.name
        status = 'passed' if report.passed else ('failed' if report.failed else 'skipped')
        duration = report.duration

        test_results.append({
            'name': test_name,
            'status': status,
            'duration': duration
        })

        if report.failed:
            log.error(f"测试失败：{test_name} - {report.longreprtext[:200] if report.longreprtext else ''}")
        elif report.passed:
            log.info(f"测试通过：{test_name}")


# ==================== 测试结束处理 ====================
def pytest_collection_finish(session):
    """收集完成时显示统计"""
    log.info(f"共收集到 {len(session.items)} 个测试用例")

def pytest_sessionfinish(session, exitstatus):
    """会话结束时保存测试结果"""
    output_path = session.config.getoption("--output", default="test_results.json")

    cfg = session.config

    # 计算统计信息
    total = len(test_results)
    passed = sum(1 for r in test_results if r['status'] == 'passed')
    failed = sum(1 for r in test_results if r['status'] == 'failed')
    skipped = sum(1 for r in test_results if r['status'] == 'skipped')
    total_duration = sum(r['duration'] for r in test_results)

    # 保存结果
    result_data = {
        'environment': {
            'env': cfg.env,
            'retry_count': int(os.environ.get("PYTEST_RETRY", "0")),
            'base_url': cfg.env_config.get('base_url', '')
        },
        'summary': {
            'total': total,
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'total_duration': round(total_duration, 2)
        },
        'test_cases': test_results
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)

    log.info(f"\n{'='*60}")
    log.info(f"测试完成统计:")
    log.info(f"  总计: {total}")
    log.info(f"  通过: {passed}")
    log.info(f"  失败: {failed}")
    log.info(f"  跳过: {skipped}")
    log.info(f"  总耗时: {total_duration:.2f}s")
    log.info(f"  结果文件: {output_path}")
    log.info(f"{'='*60}")




