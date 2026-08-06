"""重试装饰器 - 从环境变量 PYTEST_RETRY 读取重试次数"""
import os
import time
from functools import wraps
from typing import Optional

from core.logger import log


def retry(max_attempts: Optional[int] = None, delay: float = 1, backoff: int = 2, exceptions: tuple = (Exception,)):
    """
    失败重试装饰器

    Args:
        max_attempts (int | None): 最大尝试次数。None 时读取环境变量 PYTEST_RETRY，
            未设置则默认 2 次。
        delay (float): 初始等待时间（秒），默认 1 秒
        backoff (int): 延迟倍数（指数退避），默认 2 倍
        exceptions (tuple): 需要重试的异常类型，默认所有异常

    Example:
        @retry                        # 读取 PYTEST_RETRY 环境变量
        @retry(max_attempts=3)        # 显式指定次数
    """
    if max_attempts is None:
        env_retry = int(os.environ.get("PYTEST_RETRY", "0"))
        max_attempts = max(env_retry + 1, 2) if env_retry > 0 else 2

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    log.info(f"执行 {func.__name__}，第 {attempt}/{max_attempts} 次尝试")
                    return func(*args, **kwargs)

                except exceptions as e:
                    last_exception = e
                    log.warning(f"{func.__name__} 执行失败：{str(e)}")

                    if attempt < max_attempts:
                        log.info(f"等待 {current_delay}s 后重试...")
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        log.error(f"{func.__name__} 达到最大重试次数，最终失败")
                        raise last_exception
            return None
        return wrapper
    return decorator


def flaky(max_runs=2, min_passes=1):
    """
    不稳定测试容忍装饰器（允许一定比例的失败）
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            success_count = 0
            for run in range(max_runs):
                try:
                    log.info(f"运行 {func.__name__}，第 {run + 1}/{max_runs} 次")
                    func(*args, **kwargs)
                    success_count += 1
                except Exception as e:
                    log.warning(f"{func.__name__} 第 {run + 1} 次运行失败：{str(e)}")

            if success_count >= min_passes:
                log.info(f"{func.__name__} 通过：成功 {success_count}/{max_runs} 次")
                return
            else:
                log.error(f"{func.__name__} 失败：仅成功 {success_count}/{max_runs} 次，要求至少 {min_passes} 次")
                raise Exception(f"测试不稳定：成功 {success_count}/{max_runs} 次")

        return wrapper
    return decorator
