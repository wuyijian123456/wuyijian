from core.logger import log


class CleanUpManager:
    """
    测试数据清理管理器
    
    用于在用例执行后自动清理测试数据，保持环境整洁
    """
    
    _cleanup_stack = []  # 清理任务栈
    _test_context = {}   # 测试上下文
    
    @classmethod
    def register(cls, test_name, cleanup_func, *args, **kwargs):
        """
        注册清理任务
        
        Args:
            test_name (str): 测试用例名称
            cleanup_func (function): 清理函数
            *args: 清理函数的参数
            **kwargs: 清理函数的关键字参数
            
        Example:
            CleanUpManager.register(
                "test_create_order",
                OrderApi.delete_order,
                order_id="12345"
            )
        """
        task = {
            "test_name": test_name,
            "func": cleanup_func,
            "args": args,
            "kwargs": kwargs,
            "executed": False
        }
        cls._cleanup_stack.append(task)
        log.debug(f"注册清理任务：{test_name} -> {cleanup_func.__name__}")
    
    @classmethod
    def register_batch(cls, test_name, cleanup_tasks):
        """
        批量注册清理任务
        
        Args:
            test_name (str): 测试用例名称
            cleanup_tasks (list): 清理任务列表
                [
                    {"func": func1, "args": (), "kwargs": {}},
                    {"func": func2, "args": (arg1,), "kwargs": {"key": value}}
                ]
        """
        for task in cleanup_tasks:
            cls.register(
                test_name,
                task.get("func"),
                *task.get("args", ()),
                **task.get("kwargs", {})
            )
    
    @classmethod
    def execute_for_test(cls, test_name):
        """
        执行指定测试的所有清理任务
        
        Args:
            test_name (str): 测试用例名称
        """
        tasks = [t for t in cls._cleanup_stack if t["test_name"] == test_name and not t["executed"]]
        
        if not tasks:
            log.debug(f"没有需要执行的清理任务：{test_name}")
            return
        
        log.info(f"开始执行 {test_name} 的清理任务，共 {len(tasks)} 个")
        
        success_count = 0
        fail_count = 0
        
        for task in tasks:
            try:
                log.debug(f"执行清理：{task['func'].__name__}")
                task["func"](*task["args"], **task["kwargs"])
                task["executed"] = True
                success_count += 1
            except Exception as e:
                log.error(f"清理任务执行失败：{task['func'].__name__}, 错误：{str(e)}")
                fail_count += 1
        
        log.info(f"清理任务完成：成功 {success_count} 个，失败 {fail_count} 个")
    
    @classmethod
    def execute_all(cls):
        """执行所有未执行的清理任务"""
        pending_tasks = [t for t in cls._cleanup_stack if not t["executed"]]
        
        if not pending_tasks:
            return
        
        log.info(f"执行所有剩余清理任务，共 {len(pending_tasks)} 个")
        
        for task in pending_tasks:
            try:
                task["func"](*task["args"], **task["kwargs"])
                task["executed"] = True
                log.debug(f"清理任务完成：{task['test_name']} -> {task['func'].__name__}")
            except Exception as e:
                log.error(f"清理任务失败：{task['func'].__name__}, 错误：{str(e)}")
    
    @classmethod
    def clear(cls):
        """清空所有清理任务"""
        cls._cleanup_stack.clear()
        log.debug("已清空所有清理任务")
    
    @classmethod
    def context(cls, test_name):
        """
        返回清理任务的上下文管理器
        
        Args:
            test_name (str): 测试用例名称
            
        Example:
            with CleanUpManager.context("test_order"):
                # 创建测试数据
                CleanUpManager.register("test_order", delete_func, order_id)
        """
        return CleanUpContext(test_name)


class CleanUpContext:
    """清理上下文管理器"""
    
    def __init__(self, test_name):
        self.test_name = test_name
    
    def __enter__(self):
        log.debug(f"进入清理上下文：{self.test_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        log.debug(f"退出清理上下文：{self.test_name}")
        CleanUpManager.execute_for_test(self.test_name)
        return False  # 不抑制异常
