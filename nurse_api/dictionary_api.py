from core.logger import log

class Dictionaryapi:
    def __init__(self,client):
        self.client = client


    def get_dict_by_allcode(self,url,params):
        log.info("根据code获取字典")
        response= self.client.get(url,params=params)
        return response


class statisticsapi:
    def __init__(self,client):
        self.client = client


    def get_statistics_data(self,url,params):
        log.info("获取分析数据")
        response= self.client.get(url,params=params)
        return response


class categoryapi:
    def __init__(self,client):
        self.client = client

    def get_category_data(self,url,params):
        log.info("获取目录字典数据")
        response= self.client.get(url,params=params)
        return response


    def add_category_data(self,url,data):
        log.info("添加目录字典数据")
        response= self.client.post(url,data=data)
        return response


    def update_category_data(self,url,data):
        log.info("修改目录字典数据")
        response= self.client.put(url,data=data)
        return response


    def delete_category_data(self,url,data,headers= None):
        log.info("删除目录字典数据")
        response= self.client.delete(url,params=data)
        return response


class CategoryItemApi:

    def __init__(self,client):
        self.client = client


    def get_category_item_data(self,url,params):
        log.info("获取目录字典子项目数据")
        response= self.client.get(url,params=params)
        return response


    def add_category_item_data(self,url,data):
        log.info("添加目录字典子项目数据")
        response= self.client.post(url,data=data)
        return response


    def update_category_item_data(self,url,data):
        log.info("修改目录字典子项目数据")
        response= self.client.put(url,data=data)
        return response


    def delete_category_item_data(self,url,params):
        log.info("删除目录字典子项目数据")
        response= self.client.delete(url,params=params)
        return response

