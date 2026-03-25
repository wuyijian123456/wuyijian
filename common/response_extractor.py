import jsonpath
from core.logger import log
from common.var_util import var_util


class ResponseExtractor:
    """
    响应数据提取器（用于接口关联）
    
    支持从 API 响应中提取数据并保存为变量，供后续接口使用
    """
    
    @staticmethod
    def extract(response, extraction_rules):
        """
        从响应中提取多个字段
        
        Args:
            response: requests 响应对象
            extraction_rules (dict): 提取规则 {变量名：JSONPath 表达式}
            
        Example:
            extractor.extract(response, {
                "user_id": "$.data.user.id",
                "order_no": "$.data.order.orderNo",
                "token": "$.data.token"
            })
        """
        try:
            json_data = response.json()
            
            for var_name, json_path in extraction_rules.items():
                # 使用 jsonpath 提取
                result = jsonpath.jsonpath(json_data, json_path)
                
                if result:
                    value = result[0] if isinstance(result, list) else result
                    var_util.set_var(var_name, value)
                    log.info(f"提取 {var_name} = {value} (路径：{json_path})")
                else:
                    log.warning(f"未找到匹配的数据：{json_path}")
                    
        except Exception as e:
            log.error(f"提取响应数据失败：{str(e)}")
            raise
    
    @staticmethod
    def extract_one(response, var_name, json_path):
        """
        提取单个字段
        
        Args:
            response: requests 响应对象
            var_name (str): 变量名
            json_path (str): JSONPath 表达式
        """
        ResponseExtractor.extract(response, {var_name: json_path})
    
    @staticmethod
    def extract_all(response):
        """
        提取整个响应体到变量
        
        Args:
            response: requests 响应对象
        """
        try:
            json_data = response.json()
            var_name = f"response_{id(response)}"
            var_util.set_var(var_name, json_data)
            log.info(f"已保存完整响应到变量：{var_name}")
            return json_data
        except Exception as e:
            log.error(f"保存完整响应失败：{str(e)}")
            return None
    
    @staticmethod
    def replace_vars_in_request(test_data):
        """
        在请求数据中替换变量
        
        Args:
            test_data (dict): 测试数据（包含 ${var_name} 占位符）
            
        Returns:
            dict: 替换后的测试数据
        """
        return var_util.replace(test_data)
