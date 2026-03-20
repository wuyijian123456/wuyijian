import pytest
import os
import sys
from config.settings import REPORT_DIR
from core.logger import log


def run_test():
    """运行所有测试用例并生成Allure报告"""
    log.info("===== 开始执行接口自动化测试 =====")

    # 1. 运行pytest生成Allure原始数据
    pytest_args = [
        "-vs",
        "testcases",
        f"--alluredir={REPORT_DIR / 'xml'}",
        "--clean-alluredir"  # 清空旧报告
    ]
    pytest.main(pytest_args)

    # 2. 生成Allure HTML报告
    log.info("生成Allure HTML报告...")
    os.system(f"allure generate {REPORT_DIR / 'xml'} -o {REPORT_DIR / 'html'} --clean")

    # 3. 打开报告（可选）
    # os.system(f"allure serve {REPORT_DIR / 'xml'}")

    log.info(f"===== 测试执行完成，报告路径：{REPORT_DIR / 'html'} =====")


if __name__ == "__main__":
    # 添加项目根目录到Python路径（避免导入报错）
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    run_test()