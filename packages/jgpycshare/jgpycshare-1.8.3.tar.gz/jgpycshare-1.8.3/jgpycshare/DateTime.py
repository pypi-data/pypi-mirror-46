# -*- coding: utf-8 -*-
"""
    author: jiege
    url: http://jieguone.top
    copyright: © jieguone.top
    license: none
    date : 2019/4/3 23:11
    ide : PyCharm
"""
import time


class DateTime:

    def __init__(self, thisDate=0):
        self.thisDate = thisDate

    def __str__(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.thisDate))

    def ToString(self, str_format='%Y-%m-%d %H:%M:%S'):
        return time.strftime(str_format, time.localtime(self.thisDate))

    @staticmethod
    def Now():
        return DateTime(thisDate=time.time())

    def AddDays(self, days):
        return DateTime(thisDate=self.thisDate + days * 86400)

    def AddHours(self, hours):
        return DateTime(thisDate=self.thisDate + hours * 3600)

    def AddMinutes(self, minutes):
        return DateTime(thisDate=self.thisDate + minutes * 60)

    def AddSecond(self, seconds):
        return DateTime(thisDate=self.thisDate + seconds)


# if __name__ == '__main__':
#     date = DateTime.Now().AddMinutes(-1)
#     print(date.ToString())