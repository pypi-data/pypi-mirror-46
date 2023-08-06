#!/usr/bin/env python
# encoding: utf-8
"""
@author: 熊利宏
@email:xionglihong@163.com
@phone：15172383635
@project: X工具集->时间库
@file: __init__.py.py
@time: 2019-05-15 下午9:27

说明：本库基于python内置库datetime,在datetime基础上扩展了部分比较好的功能
"""
from arrow.arrow import Arrow
from arrow.factory import ArrowFactory
from arrow.api import get, now, utcnow

# 返回时间格式是否正确
from .expansions import shape
# 返回时间起止时间
from .expansions import start_and_end
