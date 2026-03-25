import json
import time
from datetime import datetime
from core.logger import log


class ReportEnhancer:
    """
    测试报告增强器
    
    用于生成更详细、更美观的测试报告
    """
    
    @staticmethod
    def add_attachment(file_path, description=""):
        """
        向 Allure 报告添加附件
        
        Args:
            file_path (str): 文件路径
            description (str): 描述信息
        """
        try:
            import allure
            allure.attach.file(
                file_path,
                name=description or file_path.split('/')[-1],
                attachment_type=allure.attachment_type.TEXT
            )
            log.debug(f"已添加附件到报告：{file_path}")
        except ImportError:
            log.warning("Allure 未安装，无法添加附件")
    
    @staticmethod
    def add_step_info(step_name, details=None):
        """
        添加步骤信息到报告
        
        Args:
            step_name (str): 步骤名称
            details (dict, optional): 详细信息
        """
        try:
            import allure
            with allure.step(f"步骤：{step_name}"):
                if details:
                    allure.attach(
                        json.dumps(details, ensure_ascii=False, indent=2),
                        name="详细信息",
                        attachment_type=allure.attachment_type.JSON
                    )
        except ImportError:
            pass
    
    @staticmethod
    def add_screenshot(screenshot_path):
        """
        添加截图到报告
        
        Args:
            screenshot_path (str): 截图文件路径
        """
        try:
            import allure
            allure.attach.file(
                screenshot_path,
                name="错误截图",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            log.error(f"添加截图失败：{str(e)}")
    
    @staticmethod
    def add_request_details(url, method, headers, params):
        """
        添加请求详情到报告
        
        Args:
            url (str): 请求 URL
            method (str): 请求方法
            headers (dict): 请求头
            params (dict): 请求参数
        """
        try:
            import allure
            with allure.step("请求详情"):
                allure.attach(
                    f"{method} {url}",
                    name="请求地址",
                    attachment_type=allure.attachment_type.TEXT
                )
                if headers:
                    allure.attach(
                        json.dumps(headers, ensure_ascii=False, indent=2),
                        name="请求头",
                        attachment_type=allure.attachment_type.JSON
                    )
                if params:
                    allure.attach(
                        json.dumps(params, ensure_ascii=False, indent=2),
                        name="请求参数",
                        attachment_type=allure.attachment_type.JSON
                    )
        except Exception as e:
            log.error(f"添加请求详情失败：{str(e)}")
    
    @staticmethod
    def add_response_details(status_code, response_data):
        """
        添加响应详情到报告
        
        Args:
            status_code (int): 状态码
            response_data (dict): 响应数据
        """
        try:
            import allure
            with allure.step("响应详情"):
                allure.attach(
                    f"Status Code: {status_code}",
                    name="状态码",
                    attachment_type=allure.attachment_type.TEXT
                )
                if response_data:
                    allure.attach(
                        json.dumps(response_data, ensure_ascii=False, indent=2),
                        name="响应内容",
                        attachment_type=allure.attachment_type.JSON
                    )
        except Exception as e:
            log.error(f"添加响应详情失败：{str(e)}")
    
    @staticmethod
    def add_sql_details(sql, params=None, result=None):
        """
        添加 SQL 执行详情到报告
        
        Args:
            sql (str): SQL 语句
            params (dict, optional): 参数
            result (list, optional): 查询结果
        """
        try:
            import allure
            with allure.step("SQL 执行"):
                allure.attach(
                    sql,
                    name="SQL 语句",
                    attachment_type=allure.attachment_type.TEXT
                )
                if params:
                    allure.attach(
                        json.dumps(params, ensure_ascii=False, indent=2),
                        name="SQL 参数",
                        attachment_type=allure.attachment_type.JSON
                    )
                if result:
                    allure.attach(
                        json.dumps(result, ensure_ascii=False, indent=2),
                        name="查询结果",
                        attachment_type=allure.attachment_type.JSON
                    )
        except Exception as e:
            log.error(f"添加 SQL 详情失败：{str(e)}")
    
    @staticmethod
    def generate_summary(test_results):
        """
        生成测试总结
        
        Args:
            test_results (list): 测试结果列表
                [{"name": "test1", "status": "passed", "duration": 1.2}, ...]
        """
        total = len(test_results)
        passed = sum(1 for r in test_results if r.get("status") == "passed")
        failed = sum(1 for r in test_results if r.get("status") == "failed")
        skipped = sum(1 for r in test_results if r.get("status") == "skipped")
        
        summary = {
            "总用例数": total,
            "通过": passed,
            "失败": failed,
            "跳过": skipped,
            "通过率": f"{(passed/total*100):.2f}%" if total > 0 else "0%",
            "执行时间": f"{sum(r.get('duration', 0) for r in test_results):.2f}s"
        }
        
        log.info("=" * 60)
        log.info("测试执行总结")
        log.info("=" * 60)
        for key, value in summary.items():
            log.info(f"{key}: {value}")
        log.info("=" * 60)
        
        return summary


# ==================== 性能监控装饰器 ====================

def performance_monitor(func):
    """
    性能监控装饰器
    
    记录函数执行时间
    
    Args:
        func: 被装饰的函数
    """
    from functools import wraps
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        log.debug(f"开始执行：{func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            log.info(f"{func.__name__} 执行完成，耗时：{duration:.3f}s")
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            log.error(f"{func.__name__} 执行失败，耗时：{duration:.3f}s, 错误：{str(e)}")
            raise
    
    return wrapper


# ==================== 测试覆盖率统计 ====================

class CoverageTracker:
    """测试覆盖率追踪器"""
    
    _tracked_tests = []
    
    @classmethod
    def track_test(cls, test_name, feature, story):
        """
        追踪测试用例执行
        
        Args:
            test_name (str): 测试名称
            feature (str): 功能模块
            story (str): 用户故事
        """
        cls._tracked_tests.append({
            "name": test_name,
            "feature": feature,
            "story": story,
            "timestamp": datetime.now()
        })
    
    @classmethod
    def get_coverage_report(cls):
        """获取覆盖率报告"""
        features = set(t["feature"] for t in cls._tracked_tests)
        
        report = {
            "总测试数": len(cls._tracked_tests),
            "覆盖功能数": len(features),
            "功能列表": list(features),
            "测试详情": cls._tracked_tests
        }
        
        return report
    
    @classmethod
    def clear(cls):
        """清空追踪记录"""
        cls._tracked_tests.clear()
