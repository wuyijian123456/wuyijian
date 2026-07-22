from core.request import req
from core.logger import log



class Dictionaryapi:

    @staticmethod
    def get_dict_by_allcode(url,params):
        log.info("根据code获取字典")
        response= req.get(url,params=params)
        return response