from pydantic import BaseModel, Field, validator, root_validator, model_validator, field_serializer, Extra
from typing import Optional,List,Any
from datetime import date, datetime


class TrainingPersonnelResponse(BaseModel):
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
    phoneNumber: Optional[str] = Field(..., pattern=r'^1\d{10}$', description="手机号")
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

    class Config:
        # 允许从属性或字典创建
        from_attributes = True
        extra = Extra.forbid
        # 设置日期序列化格式
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SelectTrainingPersonnelResponse(BaseModel):
    totalCount: int
    items: List[Any]

    class Config:
        # 允许从属性或字典创建
        from_attributes = True
        extra = Extra.forbid
        # 设置日期序列化格式
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }