import pytest
from common.test_data import TestData


def generate_test_cases(module_name, test_type="api"):
    """
    动态生成测试用例数据
    
    Args:
        module_name (str): 模块名称（对应 YAML 文件名，支持子目录格式）
        test_type (str): 测试类型 "api" 或 "db"
        
    Returns:
        list: 测试用例数据列表
        
    Example:
        # 为登录模块生成测试用例
        cases = generate_test_cases("user/login_data")
    """
    all_data = TestData.get(module_name)
    test_cases = []
    
    for case_name, case_data in all_data.items():
        # 跳过配置项（不以特定前缀开头的可能是配置）
        if not any(case_name.startswith(prefix) for prefix in ['login_', 'update_password_', 'user_info_', 'get_patient_list_']):
            continue
            
        test_cases.append((case_name, case_data))
    
    return test_cases


def get_test_data(module_name, *case_names):
    """
    获取指定测试用例的数据
    
    Args:
        module_name (str): 模块名称（支持子目录格式）
        *case_names: 用例名称列表
        
    Returns:
        list: 测试数据列表
    """
    all_data = TestData.get(module_name)
    return [all_data[name] for name in case_names if name in all_data]


def get_module_cases(module_prefix):
    """
    获取指定模块前缀的所有测试用例
    
    Args:
        module_prefix (str): 模块前缀（如 "user/" 或 "patient/"）
        
    Returns:
        dict: {用例名：测试数据}
    """
    all_modules = TestData.get_all_modules()
    module_cases = {}
    
    for module_name, data in all_modules.items():
        if module_name.startswith(module_prefix):
            for case_name, case_data in data.items():
                full_case_name = f"{module_name}/{case_name}"
                module_cases[full_case_name] = case_data
    
    return module_cases
