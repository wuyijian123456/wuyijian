import pytest
import os
import yaml
import json
from pathlib import Path
from api.user_api import UserApi
from config.env_config import BASE_DIR, set_active_env
from core.logger import log
from common.yaml_util import yaml_util
from common.var_replace_util import var_util
from common.cleanup import CleanUpManager
from core.retry import retry, flaky
from core.error_handler import on_failure

# 测试结果存储
test_results = []


# ==================== 全局 Fixture ====================

@pytest.fixture(scope="session")
def login_token():
    """登录获取 token（全局复用）"""
    log.info("===== 前置操作：登录获取 token =====")
    yaml_path = os.path.join("user", "test_cases.yaml")
    all_data = yaml_util.read_yaml(yaml_path)
    login_data = all_data.get("login_success", {})
    resp = UserApi.login(login_data["url"], login_data["username"], login_data["password"])
    token = resp.json()["access_token"]
    log.info(f"获取到 token：{token}")
    var_util.set_var("login_token", token)
    yield token


@pytest.fixture(scope="function")
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
    env = config.getoption("--env", default="test")
    config.env = env
    config.env_config = set_active_env(env)

    retry_count = config.getoption("--retry", default=0)
    os.environ["PYTEST_RETRY"] = str(retry_count)

    log.info(f"环境配置: {env}")
    log.info(f"重试次数: {retry_count}")

# ==================== 夹具 ====================

@pytest.fixture
def env(request):
    return request.config.env

@pytest.fixture
def env_config(request):
    return request.config.env_config

@pytest.fixture
def retry_count(request):
    return int(os.environ.get("PYTEST_RETRY", "0"))


# ==================== 测试结束处理 ====================
def pytest_collection_finish(session):
    """收集完成时显示统计"""
    log.info(f"共收集到 {session.testscollected} 个测试用例")

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




