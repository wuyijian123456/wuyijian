
import pymysql
import pytest
import os
from core.request import req
from core.logger import log
from common.var_replace_util import var_util





@pytest.fixture(scope="session",autouse=True)
def login_cookie():
    log.info("通过登录获取cookie")
    headers = {"cookie": ".AspNetCore.Identity.Application=CfDJ8JvsZNnSXPRBk_THcn9tuMUGBCqv2i1SPiBtkx7kpuM05oCdxRGbxTuQY1hpBlk8AlGKLCCY0LHaSF7u-wPWGyPI8Hl4TFbAncv1ixi5YdkjT6HliTcaXdtmD1J7lJHIlV5d839HqAuRj8AN4AD4CRab2W6JoC0D2Fr8BPwy7Ip7Zb5yy-2fvulzygk-PJ9rNbheOz9HHiETGh3Ztm7lUJRel88u_u1JZKCe5DxkoGnaNXTro3O1lrdaV_cTC5HHtzxSwTWrmFO4BAIb7zUXsITxrwklhBf29ceM6WNu7vO0DLrdvtg-qYCxYPlXRHTfq5UbjmXuDIN-j1GSJm1VhL2utDHXRLZgkMMvxkNf70mvPwgbVIhRyjdSMdULKikw18NZO5vRE2Vlcen-S3LFSgT_yFSA2WGhCqnj7IYgDesu7rZxhWNnX6GLXzuL_9IBudnPD1zlGMoR85dWM3d4B0hhq03qeVECyFxyS4eK_vPrXvsnUUYQGnLSFmB1F-ajZ6jWvJfel_NdqIuTJ0PjQAfj6F2R2QyN5C1tkv4tUnuk-iO0XsajLvj18xEFOwAIBak9Ermlwv_h8Ogl-Dp82irItRR-Uuv5Qo7FPwA4498RPLBLSrggsxJDiJPXMC7ErornuvwxyKlYJcoH7W2FvFry_AH46hn6lHXOhGXjM6WuQEzUr5MRDPnCzbA8QpjUgJVAM1JnNWhiXSGx7lFvfOczrY6Xj92085VQpgUQG_Ixdl8P59e0jfStJEmzo8_lnnqcllULBIScwQejD_BK_9McbtC-3UZWP3Jv6QRXIa6YaDkbDLOb-Tz5v3uoqSSaJnBYW9UxU9exwkDFDijEsYth8H4CsX170Y7KQMrNTifXeo2lT157gVDu33o3Ziba8kuFv6ENinDRk407WqQEGheVz7cZfMnHkJOGTlV426_wA3bLwVVyiBC7-96Ydsg1Tfu0KraXXbzr60LqyJSw1WE2aEpcTDQR4zm9yKPkHxtioEkATCG88erUiJszfzRkZ_57D_fwSROv9mpnvrX75MOwu-RYAHXlUm8_r1lr4D1ORconq0oqAQY_dsAOynxAZA; expires=Wed, 05 Aug 2026 05:16:03 GMT; path=/; samesite=lax; httponly"}
    response = req.post(url='/api/identity/login',params={"useCookies":"true"},json={"email":"admin","password":"Password123!"},
                        headers=headers)
    cookie = response.headers.get("Set-Cookie")
    var_util.set_var("cookie",cookie)
    yield cookie









