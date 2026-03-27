import os
import time
from datetime import datetime
from core.logger import log


class ErrorHandler:
    """
    错误处理器
    
    负责捕获异常、保存错误现场信息
    """
    
    _error_logs_dir = "report/error_logs"
    
    @staticmethod
    def save_error_context(error_msg, context_data=None):
        """
        保存错误上下文信息
        
        Args:
            error_msg (str): 错误消息
            context_data (dict, optional): 上下文数据
        """
        try:
            os.makedirs(ErrorHandler._error_logs_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"error_log_{timestamp}.txt"
            filepath = os.path.join(ErrorHandler._error_logs_dir, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("=" * 80 + "\n")
                f.write(f"错误时间：{datetime.now()}\n")
                f.write(f"错误信息：{error_msg}\n")
                
                if context_data:
                    f.write("\n上下文数据:\n")
                    f.write("-" * 40 + "\n")
                    for key, value in context_data.items():
                        f.write(f"{key}: {value}\n")
                
                f.write("=" * 80 + "\n")
            
            log.info(f"错误日志已保存到：{filepath}")
            
        except Exception as e:
            log.error(f"保存错误日志失败：{str(e)}")
    
    @staticmethod
    def handle_exception(func):
        """
        异常处理装饰器
        
        Args:
            func: 被装饰的函数
            
        Returns:
            function: 包装后的函数
        """
        from functools import wraps
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log.error(f"执行 {func.__name__} 时发生异常：{str(e)}")
                
                # 保存错误上下文
                context = {
                    "function": func.__name__,
                    "args": args,
                    "kwargs": kwargs,
                    "exception_type": type(e).__name__
                }
                ErrorHandler.save_error_context(str(e), context)
                
                # 重新抛出异常
                raise
                
        return wrapper


def on_failure(func):
    """
    测试失败时的后置处理装饰器
    
    Args:
        func: 测试函数
        
    Example:
        @on_failure
        def test_api():
            pass
    """
    from functools import wraps
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log.error(f"测试失败：{func.__name__}, 错误：{str(e)}")
            
            # 执行失败后的清理操作
            try:
                # 可以在这里注册额外的清理逻辑
                log.info("执行失败后的清理操作...")
            except Exception as cleanup_error:
                log.error(f"清理操作失败：{str(cleanup_error)}")
            
            # 保存错误日志
            ErrorHandler.save_error_context(str(e), {"test": func.__name__})
            
            raise
    
    return wrapper
