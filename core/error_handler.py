import os
import time
from datetime import datetime
from core.logger import log


class ErrorHandler:
    """
    错误处理器
    
    负责捕获异常、截图、保存错误现场信息
    """
    
    _error_screenshots_dir = "report/screenshots"
    
    @staticmethod
    def capture_screenshot(filename=None):
        """
        截取当前屏幕（需要浏览器支持）
        
        Args:
            filename (str, optional): 文件名，默认使用时间戳
            
        Returns:
            str: 截图文件路径
        """
        try:
            # 创建截图目录
            os.makedirs(ErrorHandler._error_screenshots_dir, exist_ok=True)
            
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                filename = f"error_{timestamp}.png"
            
            filepath = os.path.join(ErrorHandler._error_screenshots_dir, filename)
            
            # 注意：这里需要实际的浏览器驱动才能截图
            # 如果是 API 测试，可以改为保存错误日志或响应数据
            log.warning(f"截图功能需要浏览器支持，当前保存错误日志到：{filepath}")
            
            # TODO: 如果是 Web UI 测试，在这里调用 driver.save_screenshot(filepath)
            # 对于 API 测试，保存最后的错误信息
            with open(filepath + ".log", "w", encoding="utf-8") as f:
                f.write(f"Error captured at: {datetime.now()}\n")
            
            return filepath
            
        except Exception as e:
            log.error(f"截图失败：{str(e)}")
            return None
    
    @staticmethod
    def save_error_context(error_msg, context_data=None):
        """
        保存错误上下文信息
        
        Args:
            error_msg (str): 错误消息
            context_data (dict, optional): 上下文数据
        """
        try:
            os.makedirs(ErrorHandler._error_screenshots_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"error_context_{timestamp}.txt"
            filepath = os.path.join(ErrorHandler._error_screenshots_dir, filename)
            
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
            
            log.info(f"错误上下文已保存到：{filepath}")
            
        except Exception as e:
            log.error(f"保存错误上下文失败：{str(e)}")
    
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
                
                # 截图
                screenshot_path = ErrorHandler.capture_screenshot()
                
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
            
            # 截图和保存错误信息
            ErrorHandler.capture_screenshot()
            ErrorHandler.save_error_context(str(e), {"test": func.__name__})
            
            raise
    
    return wrapper
