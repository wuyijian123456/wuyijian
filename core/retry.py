import time
from functools import wraps
from core.logger import log


def retry(max_attempts=3, delay=1, backoff=2, exceptions=(Exception,)):
    """
    失败重试装饰器
    
    Args:
        max_attempts (int): 最大重试次数，默认 3 次
        delay (float): 初始等待时间（秒），默认 1 秒
        backoff (int): 延迟倍数（指数退避），默认 2 倍
        exceptions (tuple): 需要重试的异常类型，默认所有异常
        
    Returns:
        function: 装饰后的函数
        
    Example:
        @retry(max_attempts=3, delay=1)
        def test_api():
            pass
    """
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
                        current_delay *= backoff  # 指数退避
                    else:
                        log.error(f"{func.__name__} 达到最大重试次数，最终失败")
                        raise last_exception
                        
            return None
            
        return wrapper
    return decorator


def flaky(max_runs=2, min_passes=1):
    """
    不稳定测试容忍装饰器（允许一定比例的失败）
    
    Args:
        max_runs (int): 最大运行次数
        min_passes (int): 最小成功次数
        
    Example:
        @flaky(max_runs=3, min_passes=2)  # 运行 3 次，至少成功 2 次
        def test_unstable_api():
            pass
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
