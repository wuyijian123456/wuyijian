import os
from common.yaml_util import yaml_util


class TestData:
    """
    测试数据管理器
    
    统一管理所有测试数据，支持懒加载和缓存
    自动遍历 data 目录下的子目录，按功能模块组织数据
    """
    
    # 全局缓存
    _cache = {}
    
    # data 目录路径
    _data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    
    @classmethod
    def get(cls, module_name, key=None):
        """
        获取测试数据
        
        Args:
            module_name (str): 模块名称（格式："子目录名/文件名" 或 "文件名"）
            key (str, optional): 数据键名，不传则返回全部数据
            
        Returns:
            dict: 测试数据
            
        Example:
            # 获取 user 模块的登录数据
            data = TestData.get("user/login_data", "login_success")
            
            # 获取 patient 模块的病人列表数据
            data = TestData.get("patient/get_patient_list")
        """
        if module_name not in cls._cache:
            # 支持两种路径格式
            if '/' in module_name:
                # 包含子目录：user/login_data
                parts = module_name.split('/')
                sub_dir = parts[0]
                file_name = '/'.join(parts[1:])
                yaml_path = os.path.join(cls._data_dir, sub_dir, f"{file_name}.yaml")
            else:
                # 直接在 data 目录下
                yaml_path = os.path.join(cls._data_dir, f"{module_name}.yaml")
            
            cls._cache[module_name] = yaml_util.read_yaml(yaml_path)
        
        data = cls._cache[module_name]
        return data[key] if key else data
    
    @classmethod
    def get_all_modules(cls):
        """
        获取所有功能模块的测试数据
        
        Returns:
            dict: {模块名：数据} 的字典
        """
        modules = {}
        
        for root, dirs, files in os.walk(cls._data_dir):
            for file in files:
                if file.endswith('.yaml'):
                    # 获取相对路径（去掉 data 目录部分）
                    rel_path = os.path.relpath(root, cls._data_dir)
                    file_name = os.path.splitext(file)[0]
                    
                    if rel_path == '.':
                        module_name = file_name
                    else:
                        module_name = f"{rel_path}/{file_name}"
                    
                    modules[module_name] = cls.get(module_name)
        
        return modules
    
    @classmethod
    def clear(cls):
        """清空缓存"""
        cls._cache.clear()
