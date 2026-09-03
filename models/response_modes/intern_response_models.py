from pydantic import BaseModel, Field, validator, Extra
from typing import Annotated,Union,Any,List,Dict,Optional
from datetime import datetime


class PresonInfoModel(BaseModel):
    name: str = Field(max_length=10)
    idNumber: str
    gender: str
    birthDate: str
    age: Annotated[Optional[int],Field(ge=0, le=120,description="年龄")]
    phoneNumber: str
    height: str


class EducationModel(BaseModel):
    schoolName: str
    major: str
    education:str
    schoolPosition: Optional[str]


class InternList(BaseModel):
    items: List[Any]
    totalCount: int

class InternRotationResponse(BaseModel):
    deptCode: str
    id: str
    internId: str
    mentor: str
    startDate: datetime = Field(..., description="开始日期")
    endDate: datetime = Field(..., description="结束日期")

    class Config:
        extra = Extra.forbid


class InternDetailResponse(BaseModel):
    id: str = Field(..., description="实习生唯一ID（UUID）")
    name: str = Field(..., description="姓名")
    idNumber: str = Field(..., description="身份证号")
    gender: str = Field(..., description="性别")
    birthDate: datetime = Field(..., description="出生日期")
    age: int = Field(..., description="年龄")
    schoolName: str = Field(..., description="学校名称")
    education: str = Field(..., description="学历（degree1 代表本科等）")
    major: Optional[str] = Field(None, description="专业（可为空）")
    semester: Optional[str] = Field(None, description="学期（可为空）")
    internStartDate: datetime = Field(..., description="实习开始日期")
    internEndDate: datetime = Field(..., description="实习结束日期")
    height: str = Field(..., description="身高（字符串，如'176'）")
    phoneNumber: str = Field(..., description="手机号")
    isSelfArranged: bool = Field(..., description="是否自行安排")
    isAccommodation: bool = Field(..., description="是否提供住宿")
    specialty: Optional[str] = Field(None, description="专业特长（可为空）")
    schoolPosition: Optional[str] = Field(None, description="校内职务（可为空）")
    currentDeptName: Optional[str] = Field(None, description="当前部门（可为空）")
    currentMentor: Optional[str] = Field(None, description="当前导师（可为空）")
    currentRotationDays: int = Field(..., description="当前轮岗天数")
    deptTotalDays: int = Field(..., description="部门总天数")
    completedDeptCount: int = Field(..., description="已完成部门数")
    totalDeptCount: int = Field(..., description="总部门数")
    rotationProgress: str = Field(..., description="轮岗进度（如'0/0'）")
    nextDeptName: Optional[str] = Field(None, description="下一个部门（可为空）")
    totalLeaveCount: int = Field(..., description="总请假天数")

    # 可选：为日期字段配置格式（非必须）
    class Config:
        # 允许从属性或字典创建
        from_attributes = True
        extra = Extra.forbid
        # 设置日期序列化格式
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }




