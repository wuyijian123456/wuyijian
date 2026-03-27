from common.yaml_util import yaml_util


class TestDataLoader:
    """
    测试数据加载器
    
    统一管理所有测试数据的加载，按需获取指定模块的数据
    """
    
    # 缓存已加载的数据
    _data_cache = {}
    
    @staticmethod
    def load(module_name):
        """
        加载指定模块的测试数据
        
        Args:
            module_name (str): 模块名称（不含.yaml 后缀）
            
        Returns:
            dict: 测试数据
            
        Example:
            login_data = TestDataLoader.load("login_data")
            password_data = TestDataLoader.load("password_data")
        """
        if module_name not in TestDataLoader._data_cache:
            file_name = f"{module_name}.yaml"
            data = yaml_util.read_yaml(file_name)
            TestDataLoader._data_cache[module_name] = data
            return data
        return TestDataLoader._data_cache[module_name]
    
    @staticmethod
    def get_login_data():
        """获取登录测试数据"""
        return TestDataLoader.load("login_data")
    
    @staticmethod
    def get_user_info_data():
        """获取用户信息测试数据"""
        return TestDataLoader.load("user_info_data")
    
    @staticmethod
    def get_password_data():
        """获取密码修改测试数据"""
        return TestDataLoader.load("password_data")
    
    @staticmethod
    def get_patient_data():
        """获取病人列表测试数据"""
        return TestDataLoader.load("get_patient_list")
    
    @staticmethod
    def clear_cache():
        """清空缓存（用于重新加载数据）"""
        TestDataLoader._data_cache.clear()
