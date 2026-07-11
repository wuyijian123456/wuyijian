from core.request import req
from core.logger import log



class Userapi:

    def get_user_permissions(self,url,cookie:str):
        log.info("获取用户的按钮和菜单权限")
        header ={"cookie":cookie}
        response= req.get(url,headers=header)
        return response


    def get_user_menus(self,url,cookie):
        log.info("获取用户菜单详细信息")
        header ={"cookie":cookie}
        response= req.get(url,headers=header)
        return response