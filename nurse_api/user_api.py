from core.request import req
from core.logger import log



class Userapi:

    @staticmethod
    def get_user_permissions(url):
        log.info("获取用户的按钮和菜单权限")
        response= req.get(url)
        return response

    @staticmethod
    def get_user_menus(url):
        log.info("获取用户菜单详细信息")
        response= req.get(url,)
        return response

    @staticmethod
    def get_user_departments(url,params):
        log.info("获取科室列表信息")
        response= req.get(url,params =params)
        return response

