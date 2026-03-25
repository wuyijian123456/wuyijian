import re
from core.logger import log


class VarUtil:
    """全局变量管理工具"""
    _global_cache = {}
    _test_context = {}  # 测试用例级别的上下文

    @classmethod
    def set_var(cls, key, value):
        """设置全局变量"""
        cls._global_cache[key] = value
        log.debug(f"设置全局变量：{key} = {value}")

    @classmethod
    def get_var(cls, key, default=""):
        """获取全局变量"""
        return cls._global_cache.get(key, default)

    @classmethod
    def delete_var(cls, key):
        """删除全局变量"""
        if key in cls._global_cache:
            del cls._global_cache[key]
            log.debug(f"删除全局变量：{key}")

    @classmethod
    def clear_vars(cls):
        """清空所有全局变量"""
        cls._global_cache.clear()
        log.info("已清空所有全局变量")

    @classmethod
    def set_test_var(cls, test_name, key, value):
        """设置测试用例级别的变量"""
        if test_name not in cls._test_context:
            cls._test_context[test_name] = {}
        cls._test_context[test_name][key] = value
        log.debug(f"设置测试变量 [{test_name}]: {key} = {value}")

    @classmethod
    def get_test_var(cls, test_name, key, default=""):
        """获取测试用例级别的变量"""
        return cls._test_context.get(test_name, {}).get(key, default)

    @classmethod
    def clear_test_vars(cls, test_name):
        """清空指定测试用例的变量"""
        if test_name in cls._test_context:
            del cls._test_context[test_name]

    @classmethod
    def replace(cls, data):
        """递归替换数据中的变量占位符 ${var_name}"""
        if isinstance(data, dict):
            return {k: cls.replace(v) for k, v in data.items()}
        if isinstance(data, list):
            return [cls.replace(item) for item in data]
        if isinstance(data, str):
            # 支持 ${var_name} 格式
            pattern = r'\$\{(\w+)\}'
            
            def replacer(match):
                var_name = match.group(1)
                # 先从测试上下文查找，再从全局查找
                value = cls._global_cache.get(var_name, f"${{{var_name}}}")
                return str(value)
            
            result = re.sub(pattern, replacer, data)
            return result
        return data

    @classmethod
    def extract_json_value(cls, json_data, expression):
        """
        从 JSON 数据中提取值并保存到变量
        
        Args:
            json_data (dict): JSON 数据
            expression (str): 提取表达式，如 "data.order_id"
            
        Returns:
            any: 提取的值
        """
        keys = expression.split('.')
        value = json_data
        
        try:
            for key in keys:
                if isinstance(value, dict):
                    value = value[key]
                elif isinstance(value, list):
                    index = int(key)
                    value = value[index]
                else:
                    raise KeyError(f"无法访问 {key} 在 {type(value)} 上")
            
            return value
        except (KeyError, IndexError, ValueError) as e:
            log.error(f"提取 JSON 值失败：{expression}, 错误：{str(e)}")
            raise

    @classmethod
    def save_from_response(cls, response, var_name, json_path=None):
        """
        从响应中提取数据并保存为变量
        
        Args:
            response: requests 响应对象
            var_name (str): 变量名
            json_path (str, optional): JSON 路径，如 "data.user_id"
        """
        try:
            json_data = response.json()
            
            if json_path:
                value = cls.extract_json_value(json_data, json_path)
            else:
                value = json_data
            
            cls.set_var(var_name, value)
            log.info(f"已从响应提取 {var_name} = {value}")
            return value
            
        except Exception as e:
            log.error(f"保存响应数据到变量失败：{str(e)}")
            raise


# 全局实例
var_util = VarUtil()



