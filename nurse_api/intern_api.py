from core.logger import  log

class InternManageApi:

    def __init__(self,client):
        self.client = client


    def get_intern_info(self,url,params):
        log.info("获取实习生人员列表信息")
        resp = self.client.get(url,params)
        return resp



    def add_intern_info(self,url,params):
        log.info("新增实习生人员列表信息")
        resp = self.client.post(url,json=params)
        return resp



    def update_intern_info(self,url,params):
        log.info("编辑实习生人员列表信息")
        resp = self.client.put(url,json=params)
        return resp





    def delete_intern_info(self,url,params,json):
        log.info("世界实习生人员列表信息")
        resp = self.client.delete(url,params,json=json)
        return resp




class InternRotationApi:

    def __init__(self,client):
        self.client = client

    def get_intern_rotation_info(self, url,params):
        log.info("获取实习生轮转记录")
        resp = self.client.get(url,params)
        return resp



    def add_intern_rotation_info(self,url,params):
        log.info("新增实习生轮转记录")
        resp = self.client.post(url,json=params)
        return resp



    def update_intern_rotation_info(self,url,params):
        log.info("编辑实习生轮转记录")
        resp = self.client.put(url,json=params)
        return resp




    def delete_intern_rotation_info(self,url,params):
        log.info("编辑实习生轮转记录")
        resp = self.client.delete(url,params)
        return resp
