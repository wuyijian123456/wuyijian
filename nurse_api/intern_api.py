from core.request import req
from core.logger import  log

class InternManageApi:


    @staticmethod
    def get_intern_info(url,params):
        log.info("获取实习生人员列表信息")
        resp = req.get(url,params)
        return resp


    @staticmethod
    def add_intern_info(url,params):
        log.info("新增实习生人员列表信息")
        resp = req.post(url,json=params)
        return resp


    @staticmethod
    def update_intern_info(url,params):
        log.info("编辑实习生人员列表信息")
        resp = req.put(url,json=params)
        return resp




    @staticmethod
    def delete_intern_info(url,params):
        log.info("编辑实习生人员列表信息")
        resp = req.delete(url,params)
        return resp




class InternRotatiobApi:


    @staticmethod
    def get_intern_rotation_info(url,params):
        log.info("获取实习生轮转记录")
        resp = req.get(url,params)
        return resp


    @staticmethod
    def add_intern_rotation_info(url,params):
        log.info("新增实习生轮转记录")
        resp = req.post(url,json=params)
        return resp


    @staticmethod
    def update_intern_rotation_info(url,params):
        log.info("编辑实习生轮转记录")
        resp = req.put(url,json=params)
        return resp




    @staticmethod
    def delete_intern_rotation_info(url,params):
        log.info("编辑实习生轮转记录")
        resp = req.delete(url,params)
        return resp
