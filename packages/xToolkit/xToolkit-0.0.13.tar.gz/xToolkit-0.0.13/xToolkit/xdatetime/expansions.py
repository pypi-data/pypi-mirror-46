#!/usr/bin/env python
# encoding: utf-8
"""
@author: 熊利宏
@email:xionglihong@163.com
@phone：15172383635
@project: xToolkit
@file: expansions.py
@time: 2019-05-19 下午8:56
"""

from .expansion import XDateTime


# 查询格式
def shape(date, *args, **kwargs):
    """
    判断是否为日期格式,如果格式正确返回True,反之返回False.
    """
    return XDateTime.shape(date, *args, **kwargs)


# 查询时间区间
def start_and_end(genre="M", space=0, *args, **kwargs):
    """
    计算指定时间段的第一天和最后一天
    :param genre:"M"代表月,"Y"代表年
    :param space: 代表间距　正数代表以后,负数代表以前,绝对值必须为正整数
    :return:返回值为列表

    默认返回值：
    本月的第一天,和最后一天的列表,比如[2019-05-01,2019-05-31]
    """
    return XDateTime.start_and_end(genre, space, *args, **kwargs)
