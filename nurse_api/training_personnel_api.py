from core.logger import log
from models.request_model.training_personnel_request import TrainingPersonnelRequest,SelectTrainingPersonnelRequest
from typing import Optional


class TrainingPersonnelAPI:
    """培训人员 API 封装"""

    def __init__(self, client):
        self.client = client


    def create_personnel(self, request: TrainingPersonnelRequest):
        """
        创建培训人员（POST）
        :param request: 请求体对象（id 应为 None）
        """

        resp =  self.client.post(
            url="/api/further/trainee/info",
            data=request.to_dict()  # 自动排除 None
        )
        return resp


    def update_personnel(self, request: TrainingPersonnelRequest):
        """
        更新培训人员（PUT）
        :param personnel_id: 人员ID
        :param request: 请求体对象（必须包含 id）
        """

        # 确保 ID 一致
        # if request.id and request.id != personnel_id:
        #     raise ValueError(f"URL中的ID({personnel_id})与请求体中的ID({request.id})不一致")

        return self.client.put(
            url=f"/api/further/trainee/info",
            data=request.to_dict()
        )

    def select_personnel(self, request: SelectTrainingPersonnelRequest):
        """
        更新培训人员（PUT）
        :param personnel_id: 人员ID
        :param request: 请求体对象（必须包含 id）
        """

        # 确保 ID 一致
        # if request.id and request.id != personnel_id:
        #     raise ValueError(f"URL中的ID({personnel_id})与请求体中的ID({request.id})不一致")

        resp = self.client.get(
            url=f"/api/further/trainee/info",
            params=request.model_dump(exclude_none=True)
        )
        return resp


    # @classmethod
    # def batch_create_personnel(self, requests: List[TrainingPersonnelRequest]):
    #     """
    #     批量创建培训人员（POST）
    #     """
    #
    #
    #     # 转为字典列表
    #     data = [req.to_dict() for req in requests]
    #
    #     return self.client.post(
    #         path="/training/personnel/batch",
    #         json={"list": data}
    #     )
    #
    # @classmethod
    # def delete_personnel(self, personnel_id: int, token: Optional[str] = None):
    #     """
    #     删除培训人员（DELETE）
    #     """
    #     if token:
    #         self.client.set_token(token)
    #
    #     return self.client.delete(path=f"/training/personnel/{personnel_id}")