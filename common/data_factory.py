import random
import string
from datetime import datetime, timedelta
from core.logger import log


class DataFactory:
    """
    测试数据工厂
    
    用于生成各种类型的测试数据，支持随机数据、时间数据等
    """
    
    @staticmethod
    def random_string(length=8, chars=None):
        """
        生成随机字符串
        
        Args:
            length (int): 字符串长度
            chars (str, optional): 字符集，默认字母 + 数字
            
        Returns:
            str: 随机字符串
        """
        if chars is None:
            chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    @staticmethod
    def random_email(domain="test.com"):
        """
        生成随机邮箱
        
        Args:
            domain (str): 邮箱域名
            
        Returns:
            str: 随机邮箱地址
        """
        username = DataFactory.random_string(8)
        return f"{username}@{domain}"
    
    @staticmethod
    def random_phone():
        """
        生成随机手机号
        
        Returns:
            str: 11 位手机号
        """
        prefix = random.choice(["138", "139", "150", "151", "158", "159", "186", "187", "188"])
        suffix = ''.join(random.choice(string.digits) for _ in range(8))
        return f"{prefix}{suffix}"
    
    @staticmethod
    def random_id_card():
        """
        生成随机身份证号（简化版）
        
        Returns:
            str: 18 位身份证号
        """
        region = random.choice([
            "110101", "110102", "310101", "310102", "440101", "440102"
        ])
        year = random.randint(1970, 2000)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        birth = f"{year:04d}{month:02d}{day:02d}"
        seq = ''.join(random.choice(string.digits) for _ in range(3))
        check = random.choice(string.digits + "X")
        return f"{region}{birth}{seq}{check}"
    
    @staticmethod
    def random_name():
        """
        生成随机中文姓名
        
        Returns:
            str: 2-3 字姓名
        """
        surnames = ["张", "王", "李", "赵", "刘", "陈", "杨", "黄", "周", "吴"]
        names = ["伟", "芳", "娜", "敏", "静", "丽", "强", "磊", "军", "洋"]
        
        surname = random.choice(surnames)
        given_name = ''.join(random.choice(names) for _ in range(random.randint(1, 2)))
        return f"{surname}{given_name}"
    
    @staticmethod
    def random_password(length=8, include_special=False):
        """
        生成随机密码
        
        Args:
            length (int): 密码长度
            include_special (bool): 是否包含特殊字符
            
        Returns:
            str: 随机密码
        """
        chars = string.ascii_letters + string.digits
        if include_special:
            chars += "!@#$%^&*"
        return ''.join(random.choice(chars) for _ in range(length))
    
    @staticmethod
    def random_number(min_value=0, max_value=1000):
        """
        生成随机整数
        
        Args:
            min_value (int): 最小值
            max_value (int): 最大值
            
        Returns:
            int: 随机整数
        """
        return random.randint(min_value, max_value)
    
    @staticmethod
    def random_float(min_value=0.0, max_value=100.0, decimals=2):
        """
        生成随机浮点数
        
        Args:
            min_value (float): 最小值
            max_value (float): 最大值
            decimals (int): 小数位数
            
        Returns:
            float: 随机浮点数
        """
        return round(random.uniform(min_value, max_value), decimals)
    
    @staticmethod
    def random_date(start_date=None, end_date=None, fmt="%Y-%m-%d"):
        """
        生成随机日期
        
        Args:
            start_date (str/datetime): 开始日期
            end_date (str/datetime): 结束日期
            fmt (str): 日期格式
            
        Returns:
            str: 随机日期
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        if end_date is None:
            end_date = datetime.now()
        
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, fmt)
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, fmt)
        
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        random_date = start_date + timedelta(days=random_days)
        
        return random_date.strftime(fmt)
    
    @staticmethod
    def random_datetime(start_date=None, end_date=None, fmt="%Y-%m-%d %H:%M:%S"):
        """
        生成随机日期时间
        
        Args:
            start_date (str/datetime): 开始日期
            end_date (str/datetime): 结束日期
            fmt (str): 日期格式
            
        Returns:
            str: 随机日期时间
        """
        return DataFactory.random_date(start_date, end_date, fmt)
    
    @staticmethod
    def random_uuid():
        """
        生成随机 UUID（简化版）
        
        Returns:
            str: UUID 格式字符串
        """
        import uuid
        return str(uuid.uuid4())
    
    @staticmethod
    def create_user_data(overrides=None):
        """
        生成用户测试数据
        
        Args:
            overrides (dict, optional): 覆盖默认值
            
        Returns:
            dict: 用户数据
        """
        user_data = {
            "userName": DataFactory.random_name(),
            "email": DataFactory.random_email(),
            "phone": DataFactory.random_phone(),
            "idCard": DataFactory.random_id_card(),
            "password": DataFactory.random_password()
        }
        
        if overrides:
            user_data.update(overrides)
        
        log.debug(f"生成用户数据：{user_data}")
        return user_data
    
    @staticmethod
    def create_order_data(overrides=None):
        """
        生成订单测试数据
        
        Args:
            overrides (dict, optional): 覆盖默认值
            
        Returns:
            dict: 订单数据
        """
        order_data = {
            "orderNo": DataFactory.random_uuid().replace("-", ""),
            "goodsId": DataFactory.random_number(1000, 9999),
            "num": DataFactory.random_number(1, 10),
            "amount": DataFactory.random_float(10.0, 1000.0),
            "remark": DataFactory.random_string(20)
        }
        
        if overrides:
            order_data.update(overrides)
        
        log.debug(f"生成订单数据：{order_data}")
        return order_data
    
    @staticmethod
    def create_patient_data(overrides=None):
        """
        生成病人测试数据
        
        Args:
            overrides (dict, optional): 覆盖默认值
            
        Returns:
            dict: 病人数据
        """
        patient_data = {
            "name": DataFactory.random_name(),
            "idCard": DataFactory.random_id_card(),
            "phone": DataFactory.random_phone(),
            "deptCode": DataFactory.random_string(6).upper(),
            "bedNo": f"{DataFactory.random_number(1, 50)}床"
        }
        
        if overrides:
            patient_data.update(overrides)
        
        log.debug(f"生成病人数据：{patient_data}")
        return patient_data


# 全局实例
data_factory = DataFactory()
