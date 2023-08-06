#!/usr/bin/env python
# encoding: utf-8
"""
@author: 熊利宏
@email:xionglihong@163.com
@phone：15172383635
@project: xToolkit
@file: expansion.py
@time: 2019-05-15 下午9:55
"""

import time
import arrow


class XDateTime(object):
    """
    日期时间常用功能
    """

    @classmethod
    def shape(self, date, *args, **kwargs):
        """
        判断是否为日期格式,如果格式正确返回True,反之返回False.
        """
        try:
            time.strptime(date, "%Y-%m-%d")
            return True
        except:
            return False

    @classmethod
    def start_and_end(self, genre="M", space=0, format="YYYY-MM-DD", *args, **kwargs):
        """
        计算指定时间段的第一天和最后一天
        :param genre:"M"代表月,"Y"代表年
        :param space: 代表间距　正数代表以后,负数代表以前,绝对值必须为正整数
        :return:返回值为列表

        默认返回值：
        上一个月的第一天,和最后一天的列表,比如[2019-05-01,2019-05-31]
        """
        # 如果类型为月
        if genre == "M":
            # 指定月第一天
            start = eval("""arrow.now().shift(months={}).format("YYYY-MM-01")""".format(space))
            # 指定月的最后一天
            end = eval("""arrow.get("{}").shift(months=1).shift(days=-1).format("YYYY-MM-DD")""".format(start))

            return [start, end]
        # 如果类型为年
        elif genre == "Y":
            # 指定年第一天
            start = eval("""arrow.now().shift(years={}).format("YYYY-01-01")""".format(space))
            # 指定年的最后一天
            end = eval("""arrow.get("{}").shift(years=1).shift(days=-1).format("YYYY-MM-DD")""".format(start))

            return [start, end]
        # 类型的值只能是M或者Y
        else:
            raise RuntimeError('genre is M or Y')
