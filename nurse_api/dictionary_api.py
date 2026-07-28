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