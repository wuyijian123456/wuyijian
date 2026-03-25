import pytest
from api.user_api import UserApi
from core.logger import log
from common.yaml_util import yaml_util
from common.var_replace_util import var_util
from common.cleanup import CleanUpManager
from core.retry import retry, flaky
from core.error_handler import on_failure

# ==================== 全局 Fixture ====================

# 作用域：session（整个测试会话只执行一次）
@pytest.fixture(scope="session")
def login_token():
    """登录获取 token（全局复用）"""
    log.info("===== 前置操作：登录获取 token =====")
    # 读取登录成功数据
    login_data = yaml_util.read_yaml("user_data.yaml")["login_success"]
    resp = UserApi.login(login_data["url"],login_data["username"], login_data["password"])
    # 提取 token
    token = resp.json()["access_token"]
    log.info(f"获取到 token：{token}")
    
    # 保存到全局变量
    var_util.set_var("login_token", token)
    
    yield token  # 返回 token 给用例
    log.info("===== 后置操作：清理登录态 =====")


# 作用域：function（每个用例执行一次）
@pytest.fixture(scope="function")
def test_context(request):
    """
    测试上下文管理器
    
    提供：
    - 测试名称
    - 变量隔离
    - 自动清理
    """
    test_name = request.node.name
    log.info(f"\n{'='*60}")
    log.info(f"开始执行测试：{test_name}")
    log.info(f"{'='*60}")
    
    # 创建测试级别的上下文
    yield {"test_name": test_name}
    
    # 清理测试级别的变量
    var_util.clear_test_vars(test_name)
    
    # 执行注册的清理任务
    CleanUpManager.execute_for_test(test_name)
    
    log.info(f"测试完成：{test_name}\n")


# ==================== Hook 函数 ====================

# 注意：自定义标记已在 pytest.ini 中配置，无需在此重复注册


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试运行报告钩子
    
    用于捕获测试结果，执行后置操作
    """
    # 执行所有其他钩子
    outcome = yield
    report = outcome.get_result()
    
    # 在测试完成后执行
    if report.when == 'call':
        if report.failed:
            # 测试失败，可以在这里添加额外处理
            log.error(f"测试失败：{item.name}")
        elif report.passed:
            log.info(f"测试通过：{item.name}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_setup(item):
    """测试 setup 钩子"""
    log.debug(f"准备测试：{item.name}")
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item):
    """测试 teardown 钩子"""
    log.debug(f"清理测试：{item.name}")
    yield


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