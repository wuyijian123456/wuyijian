from core.request import req
from core.logger import log

class UserApi:
    """用户模块接口封装：登录、获取用户信息、修改密码"""

    @classmethod
    def login(cls, url,username, password):
        """用户登录"""
        log.info("调用登录接口")
        data = {
            "username": username,
            "password": password,
            "client_id":"vue.client",
            "client_secret":"",
            "grant_type":"password",
            "verifier_code":"",
            "code_session":""
        }
        headers ={'content-type':'application/x-www-form-urlencoded'}
        return req.post(url, data=data,headers=headers)

    @classmethod
    def get_user_info(cls,url, token):
        """获取用户信息（需要token）"""
        log.info("调用获取用户信息接口")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        return req.get(url, headers=headers)

    @classmethod
    def update_password(cls, url, token, old_pwd, new_pwd):
        """修改密码"""
        log.info("调用修改密码接口")
        headers = {
            "Authorization": f"Bearer {token}"
        }

        data = {
            "checkPassword": old_pwd,
            "currentPassword": new_pwd,
            "newPassword": new_pwd
        }
        params = {'__tenant': 'H0002'}
        return req.post(url, json=data, headers=headers, params=params)