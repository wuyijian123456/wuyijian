from core.request import req
from core.logger import log

class UserApi:
    """用户模块接口封装：登录、获取用户信息、修改密码"""
    # 接口路径
    LOGIN_URL = "/api/oauth/connect/token"
    USER_INFO_URL = "/api/identity/profile/my"
    UPDATE_PWD_URL = "/api/identity/my-profile/change-password"

    @classmethod
    def login(cls, username, password):
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
        return req.post(cls.LOGIN_URL, data=data,headers=headers)

    @classmethod
    def get_user_info(cls, token):
        """获取用户信息（需要token）"""
        log.info("调用获取用户信息接口")
        headers = {
            "Authorization": f"Bearer {token}"
        }
        return req.get(cls.USER_INFO_URL, headers=headers)

    @classmethod
    def update_password(cls, token, old_pwd, new_pwd):
        """修改密码"""
        log.info("调用修改密码接口")
        headers = {
            "Authorization": f"Bearer {token}"
        }

        data = {
            "checkPassword": old_pwd,
            "currentPassword": new_pwd,
            "newPassword":new_pwd
        }
        params ={'__tenant':'H0002'}
        return req.post(cls.UPDATE_PWD_URL, json=data, headers=headers,**params)