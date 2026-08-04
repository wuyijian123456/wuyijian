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
    def random_name_birthday_and_id():
        """
        生成出生日期，并生成对应的身份证号（前6位+出生日期+顺序码+校验码）
        适合接口测试，需要身份证号字段的场景
        """
        # 1. 生成随机出生日期（18-60岁）
        now = datetime.now()
        age = random.randint(18, 30)
        birth_date = now - timedelta(days=365 * age + random.randint(0, 365))
        birth_date = birth_date.replace(hour=0, minute=0, second=0, microsecond=0)

        # 2. 格式化日期
        birth_str = birth_date.strftime('%Y%m%d')

        # 3. 构造身份证号（前6位地区码 + 出生日期 + 3位顺序码 + 校验码）
        area_code = random.choice(['110101', '440301', '310101', '510107'])  # 北京/深圳/上海/成都
        order_code = f"{random.randint(0, 999):03d}"  # 顺序码
        # 校验码（简单示例，实际需要算法，这里固定为X）
        if order_code[-1]  in (1, 3, 5, 7, 9):
            gender = '男'
        else:
            gender = '女'

        check_code = random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'X'])

        id_card = area_code + birth_str + order_code + check_code

        return {
            'name': DataFactory.random_name(),
            'birthday': birth_date.isoformat(),
            'id_card': id_card,
            'age': age,
            'gender': gender
        }

    @staticmethod
    def random_datetime(start_date=None, end_date=None, fmt="%Y-%m-%dT%H:%M:%S"):
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

    @staticmethod
    def  random_school_major():
        school= ['北京大学','清华大学','南京大学','复旦大学']
        major = ['解剖学','护理学','药剂学','麻醉学','中医学']
        return {
            'school':random.choice(school),
            'major': random.choice(major)
        }

    @staticmethod
    def random_prefix_name(prefix,length=1):

        name = prefix + DataFactory.random_string(length)
        return name


# 全局实例
data_factory = DataFactory()


a = data_factory.random_name_birthday_and_id()
b = data_factory.random_school_major()
c = data_factory.random_datetime()
print(c)


