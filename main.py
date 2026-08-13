import pytest
import os
import sys
import argparse
from config.env_config import REPORT_DIR
from core.logger import log


# ==================== 入口函数 ====================

def run_test(env: str, retry: int, test_path: str, tags: str):
    """运行指定环境的测试用例并生成Allure报告"""
    log.info("===== 开始执行接口自动化测试 =====")

    pytest_args = [
        "-vs",
        test_path,
        f"--alluredir={REPORT_DIR / 'xml'}",
        "--clean-alluredir",
        f"--env={env}",
        f"--retry={retry}",
    ]
    if tags:
        pytest_args.append(f"--tags={tags}")

    log.info(f"===== {pytest_args} =====")
    pytest.main(pytest_args)

    # log.info("生成Allure HTML报告...")
    # os.system(f"allure generate {REPORT_DIR / 'xml'} -o {REPORT_DIR / 'html'} --clean")
    # os.system(f"allure serve {REPORT_DIR / 'xml'}")
    #
    # log.info(f"===== 测试执行完成，报告路径：{REPORT_DIR / 'html'} =====")


# ==================== 命令行入口 ====================

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    parser = argparse.ArgumentParser(description="接口自动化测试脚本")
    parser.add_argument("--env", default="uat", help="运行环境：test, prod, uat")
    parser.add_argument("--retry", type=int, default=0, help="失败重试次数")
    parser.add_argument("--path", default="nurse_testcases", help="测试用例路径")
    parser.add_argument("--tags", default="", help="运行指定标签的测试用例")
    args = parser.parse_args()

    run_test(args.env, args.retry, args.path, args.tags)