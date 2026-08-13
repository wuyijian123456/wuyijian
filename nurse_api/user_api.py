from core.logger import log


class UserApi:

    def __init__(self,client):
        self.client = client


    def get_user_permissions(self,url):
        log.info("获取用户的按钮和菜单权限")
        response= self.client.get(url)
        return response


    def get_user_menus(self,url):
        log.info("获取用户菜单详细信息")
        response= self.client.get(url,)
        return response


    def get_user_departments(self,url,params):
        log.info("获取科室列表信息")
        response= self.client.get(url,params =params)
        return response

