from datetime import datetime, timedelta
from typing import Optional, List
import random
from uuid import UUID

from common.data_factory import data_factory as base_data_factory
from faker import Faker
from models.request_model.training_personnel_request import TrainingPersonnelRequest, SelectTrainingPersonnelRequest

fake = Faker('zh_CN')


class TrainingPersonnelFactory:
    """培训人员测试数据工厂"""

    @staticmethod
    def base_personnel() -> TrainingPersonnelRequest:
        """
        基础人员数据（所有字段都有值）
        """
        start_date,end_date = base_data_factory.random_date_scope(fmt="%Y-%m-%d")
        # 确保转换为 datetime 对象
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

        duration_days = (end_date_obj - start_date_obj).days

        return TrainingPersonnelRequest(
            id=base_data_factory.random_uuid(),
            name=fake.name(),
            unitName=fake.company() + "有限公司",
            gender=random.choice(["男", "女"]),
            trainingLocation=fake.city() + "培训中心",
            unitLevel=random.choice(["level1", "level2", "level3", "level3"]),
            unitType=random.choice(["type1", "type1", "type2", "type2"]),
            personnelCategory=random.choice(["管理人员", "技术人员", "一线员工", "实习生"]),
            education=random.choice(["本科", "硕士", "博士", "专科", "高中"]),
            phoneNumber=fake.phone_number(),
            position=random.choice(["经理", "主管", "专员", "工程师", "助理"]),
            title=random.choice(["高级工程师", "工程师", "助理工程师", "技术员"]),
            age=str(random.randint(22, 50)),
            major=fake.job(),
            trainingStartDate=start_date_obj,
            trainingEndDate=end_date_obj,
            trainingDuration=str(duration_days * 8),  # 假设每天8小时
            trainingDays=str(duration_days),
            trainingDepartment=fake.company() + "培训部",
            certificateNumber=f"CTF{random.randint(100000, 999999)}",
            employeeCardNumber=f"EMP{random.randint(100000, 999999)}",
            isAccommodation=random.choice([True, False]),
            remark=fake.sentence()
        )

    @staticmethod
    def minimal_personnel() -> TrainingPersonnelRequest:
        """
        最小数据（只有必填字段，其他为 None）
        """
        start_date,end_date = base_data_factory.random_date_scope(fmt="%Y-%m-%d")
        # 确保转换为 datetime 对象
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        duration_days = (end_date_obj - start_date_obj).days
        return TrainingPersonnelRequest(
            name="张三",
            gender=random.choice(["男", "女"]),
            unitName="测试科技有限公司",
            major=fake.job(),
            phoneNumber="13800138000",
            personnelCategory=random.choice(["管理人员", "技术人员", "一线员工", "实习生"]),
            position=random.choice(["经理", "主管", "专员", "工程师", "助理"]),
            trainingLocation=fake.city() + "培训中心",
            trainingStartDate=start_date_obj,
            trainingEndDate=end_date_obj,
            trainingDuration=str(duration_days * 8),
            trainingDays=str(duration_days),
            unitLevel=random.choice(["level1", "level2", "level3", "level3"]),
            unitType=random.choice(["type1", "type1", "type2", "type2"])
        )

    @staticmethod
    def for_create() -> TrainingPersonnelRequest:
        """
        创建场景（id 为 None）
        """
        base = TrainingPersonnelFactory.base_personnel()
        # 创建时 id 不应该有值
        return base.copy(update={"id": None})

    @staticmethod
    def for_update(personnel_id: UUID) -> TrainingPersonnelRequest:
        """
        更新场景（必须有 id）
        """
        base = TrainingPersonnelFactory.base_personnel()
        return base.copy(update={"id": personnel_id})

    @staticmethod
    def with_name(name: str) -> TrainingPersonnelRequest:
        """
        自定义姓名
        """
        base = TrainingPersonnelFactory.base_personnel()
        return base.copy(update={"name": name})

    @staticmethod
    def with_phone(phone: str) -> TrainingPersonnelRequest:
        """
        自定义手机号
        """
        base = TrainingPersonnelFactory.base_personnel()
        return base.copy(update={"phoneNumber": phone})

    @staticmethod
    def with_training_dates(start_date: datetime, end_date: datetime) -> TrainingPersonnelRequest:
        """
        自定义培训时间
        """
        base = TrainingPersonnelFactory.base_personnel()
        delta = end_date - start_date
        return base.copy(update={
            "trainingStartDate": start_date,
            "trainingEndDate": end_date,
            "trainingDays": delta.days,
            "trainingDuration": delta.days * 8
        })

    @staticmethod
    def with_accommodation(is_accommodation: bool) -> TrainingPersonnelRequest:
        """
        设置是否住宿
        """
        base = TrainingPersonnelFactory.base_personnel()
        return base.copy(update={"isAccommodation": is_accommodation})

    # ========== 非法数据（用于异常测试） ==========

    @staticmethod
    def invalid_phone_wrong_format() -> TrainingPersonnelRequest:
        """非法：手机号格式错误"""
        base = TrainingPersonnelFactory.minimal_personnel()
        copied = base.model_copy(update={"phoneNumber": "123456"})
        return TrainingPersonnelRequest.model_validate(copied.model_dump())

    @staticmethod
    def invalid_age_too_young() -> TrainingPersonnelRequest:
        """非法：年龄小于18"""
        base = TrainingPersonnelFactory.base_personnel()
        return base.copy(update={"age": 16})

    @staticmethod
    def invalid_age_too_old() -> TrainingPersonnelRequest:
        """非法：年龄大于100"""
        base = TrainingPersonnelFactory.base_personnel()
        return base.copy(update={"age": 120})

    @staticmethod
    def invalid_training_dates() -> TrainingPersonnelRequest:
        """非法：开始时间 > 结束时间"""
        base = TrainingPersonnelFactory.base_personnel()
        now = datetime.now()
        return base.copy(update={
            "trainingStartDate": now,
            "trainingEndDate": now - timedelta(days=30)  # 结束时间早于开始
        })

    @staticmethod
    def invalid_gender() -> TrainingPersonnelRequest:
        """非法：性别值错误"""
        base = TrainingPersonnelFactory.base_personnel()
        return base.copy(update={"gender": "X"})

    @staticmethod
    def invalid_name_too_long() -> TrainingPersonnelRequest:
        """非法：姓名超过50个字符"""
        base = TrainingPersonnelFactory.base_personnel()
        return base.copy(update={"name": "张" * 51})

    @staticmethod
    def invalid_remark_too_long() -> TrainingPersonnelRequest:
        """非法：备注超过500个字符"""
        base = TrainingPersonnelFactory.base_personnel()
        return base.copy(update={"remark": "备" * 501})



class SelectTrainingPersonnelFactory:

    @staticmethod
    def create_base_personnel(name: str = None) -> SelectTrainingPersonnelRequest:

        return SelectTrainingPersonnelRequest(keyword = name,skip = 0,limit= 20)