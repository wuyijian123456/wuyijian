from pydantic import BaseModel, Field, validator, root_validator, model_validator, field_serializer, field_validator
from typing import Optional
from datetime import date, datetime
from typing import List


class TrainingPersonnelRequest(BaseModel):
    """
    培训人员信息请求体
    包含 25+ 个字段，大部分可选
    """

    # ========== 基本信息（7个） ==========
    id: Optional[str] = Field(None, description="人员ID（更新时必填）")
    name: Optional[str] = Field(..., min_length=1, max_length=50, description="姓名")
    unitName: Optional[str] = Field(..., min_length=1, max_length=200, description="单位名称")
    gender: Optional[str] = Field(..., pattern="^(M|F|男|女)$", description="性别: M/男/F/女")
    trainingLocation: Optional[str] = Field(..., min_length=1, max_length=200, description="培训地点")
    unitLevel: Optional[str] = Field(..., description="单位级别" )
    unitType: Optional[str] = Field(..., description="单位类型")

    # ========== 人员信息（7个） ==========
    personnelCategory: Optional[str] = Field(..., description="人员类别")
    education: Optional[str] = Field(None, description="学历")
    phoneNumber: str = Field(..., pattern=r'^1\d{10}$', description="手机号")
    position: Optional[str] = Field(None, max_length=100, description="职位")
    title: Optional[str] = Field(None, max_length=100, description="职称")
    age: Optional[str] = Field(None, description="年龄（18-100）")
    major: Optional[str] = Field(..., max_length=100, description="专业")

    # ========== 培训信息（6个） ==========
    trainingStartDate: Optional[datetime] = Field(..., description="培训开始时间")
    trainingEndDate: Optional[datetime] = Field(..., description="培训结束时间")
    trainingDuration: Optional[str] = Field(None, description="培训时长（小时）")
    trainingDays: Optional[str] = Field(..., description="培训天数")
    trainingDepartment: Optional[str] = Field(None, max_length=200, description="培训部门")
    certificateNumber: Optional[str] = Field(None, max_length=50, description="证书编号")

    # ========== 其他信息（4个） ==========
    employeeCardNumber: Optional[str] = Field(None, max_length=50, description="员工卡号")
    isAccommodation: Optional[bool] = Field(None, description="是否住宿")
    remark: Optional[str] = Field(None, max_length=500, description="备注")

    # ========== 自定义校验 ==========

    # 或者使用 validator
    @field_validator('phoneNumber')
    def validate_phone(cls, v):
        import re
        if not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('手机号格式错误，必须为11位数字且以1开头')
        return v

    @model_validator(mode='after')  # ✅ V2 推荐
    def validate_training_dates(self) -> 'TrainingPersonnelRequest':  # ✅ V2 签名
        start = self.trainingStartDate
        end = self.trainingEndDate
        if start is not None and end is not None and start >= end:
            raise ValueError("培训开始时间必须早于结束时间")
        return self

    @model_validator(mode='after')
    def validate_and_calc_dates(self) -> 'TrainingPersonnelRequest':
        start = self.trainingStartDate
        end = self.trainingEndDate

        if start is not None and end is not None:
            if start >= end:
                raise ValueError("培训开始时间必须早于结束时间")

            delta = end - start
            if self.trainingDuration is None:
                self.trainingDuration = int(delta.total_seconds() / 3600)
            if self.trainingDays is None:
                self.trainingDays = delta.days

        return self




    # Pydantic v2 的推荐方式
    @field_serializer('trainingStartDate', 'trainingEndDate')
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%dT%H:%M:%S")

    def to_dict(self, exclude_none: bool = True) -> dict:
        """
        转为字典
        :param exclude_none: 是否排除 None 值（默认 True）
        """
        if exclude_none:
            return self.model_dump_json(exclude_none=False)
        return self.model_dump_json(indent=2)



class SelectTrainingPersonnelRequest(BaseModel):
    keyword: Optional[str] = Field(None, description="关键字查询")
    skip: Optional[int] = Field(..., description="页码")
    limit: Optional[int] = Field(..., description="每页条数")

    def to_dict(self, exclude_none: bool = True) -> dict:
        """
        转为字典
        :param exclude_none: 是否排除 None 值（默认 True）
        """
        if exclude_none:
            return self.model_dump_json(exclude_none=False)
        return self.model_dump_json(indent=2)
