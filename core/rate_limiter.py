import time
from functools import wraps
from threading import Semaphore, Lock
from core.logger import log


class RateLimiter:
    """
    速率限制器
    
    用于控制 API 请求的频率，避免触发限流
    """
    
    def __init__(self, calls_per_second=10):
        """
        初始化速率限制器
        
        Args:
            calls_per_second (int): 每秒允许的请求数
        """
        self.calls_per_second = calls_per_second
        self.interval = 1.0 / calls_per_second
        self.last_call_time = 0
        self.lock = Lock()
    
    def acquire(self):
        """获取请求许可"""
        with self.lock:
            current_time = time.time()
            elapsed = current_time - self.last_call_time
            
            if elapsed < self.interval:
                wait_time = self.interval - elapsed
                log.debug(f"速率限制：等待 {wait_time:.3f}s")
                time.sleep(wait_time)
            
            self.last_call_time = time.time()
    
    def __call__(self, func):
        """装饰器方式调用"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.acquire()
            return func(*args, **kwargs)
        return wrapper


class ConcurrencyController:
    """
    并发控制器
    
    用于控制同时执行的测试用例数量
    """
    
    def __init__(self, max_concurrent=5):
        """
        初始化并发控制器
        
        Args:
            max_concurrent (int): 最大并发数
        """
        self.max_concurrent = max_concurrent
        self.semaphore = Semaphore(max_concurrent)
        self.active_count = 0
        self.lock = Lock()
    
    def acquire(self):
        """获取并发许可"""
        self.semaphore.acquire()
        with self.lock:
            self.active_count += 1
            log.debug(f"并发数：{self.active_count}/{self.max_concurrent}")
    
    def release(self):
        """释放并发许可"""
        with self.lock:
            self.active_count -= 1
        self.semaphore.release()
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False


def rate_limit(calls_per_second=10):
    """
    速率限制装饰器
    
    Args:
        calls_per_second (int): 每秒允许的请求数
        
    Example:
        @rate_limit(calls_per_second=5)
        def test_api():
            pass
    """
    limiter = RateLimiter(calls_per_second)
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            limiter.acquire()
            try:
                return func(*args, **kwargs)
            finally:
                pass  # 可以在这里添加后续处理
        return wrapper
    return decorator


def concurrent_limit(max_concurrent=5):
    """
    并发限制装饰器
    
    Args:
        max_concurrent (int): 最大并发数
        
    Example:
        @concurrent_limit(max_concurrent=3)
        def test_parallel():
            pass
    """
    controller = ConcurrencyController(max_concurrent)
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            controller.acquire()
            try:
                return func(*args, **kwargs)
            finally:
                controller.release()
        return wrapper
    return decorator


# 全局默认速率限制器（10 次/秒）
default_rate_limiter = RateLimiter(calls_per_second=10)
