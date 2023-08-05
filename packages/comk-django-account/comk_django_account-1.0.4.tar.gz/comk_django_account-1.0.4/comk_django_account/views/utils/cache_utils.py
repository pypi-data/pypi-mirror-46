from datetime import datetime, timedelta

from django.core.cache import cache


class CacheUtils():
    def __init__(self):
        pass

    def GetInterfaceTimes(self, key):
        '''
        获取接口调用次数

        :param hpzl:
        :param hphm:
        :return:
        '''
        value = cache.get(key)

        if value:
            cache.incr(key)
            return cache.get(key)
        else:
            now = datetime.now()
            end_time = datetime(now.year, now.month, now.day, 0, 0, 0) + timedelta(days=1)
            countdown_time = int((end_time - now).total_seconds())
            cache.set(key, 1, countdown_time)
            return cache.get(key)
