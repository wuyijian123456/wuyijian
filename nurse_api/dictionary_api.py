from core.request import req
from core.logger import log



class Dictionaryapi:

    @staticmethod
    def get_dict_by_allcode(url,params):
        log.info("根据code获取字典")
        response= req.get(url,params=params)
        return response


class statisticsapi:

    @staticmethod
    def get_statistics_data(url,params):
        log.info("获取分析数据")
        response= req.get(url,params=params)
        return response

class categoryapi:

    @staticmethod
    def get_category_data(url,params):
        log.info("获取目录字典数据")
        response= req.get(url,params=params)
        return response

    @staticmethod
    def add_category_data(url,data):
        log.info("添加目录字典数据")
        response= req.post(url,data=data)
        return response

    @staticmethod
    def update_category_data(url,data):
        log.info("修改目录字典数据")
        response= req.put(url,data=data)
        return response

    @staticmethod
    def delete_category_data(url,data,headers= None):
        log.info("删除目录字典数据")
        response= req.delete(url,params=data)
        return response


class CategoryItemApi:


    @staticmethod
    def get_category_item_data(url,params):
        log.info("获取目录字典子项目数据")
        response= req.get(url,params=params)
        return response

    @staticmethod
    def add_category_item_data(url,data):
        log.info("添加目录字典子项目数据")
        response= req.post(url,data=data)
        return response

    @staticmethod
    def update_category_item_data(url,data):
        log.info("修改目录字典子项目数据")
        response= req.put(url,data=data)
        return response

    @staticmethod
    def delete_category_item_data(url,params):
        log.info("删除目录字典子项目数据")
        response= req.delete(url,params=params)
        return response

