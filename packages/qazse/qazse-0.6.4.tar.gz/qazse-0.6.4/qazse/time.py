#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------
#       项目名: qazse   
#       文件名: time 
#       作者  : Qazse 
#       时间  : 2019/4/13
#       主页  : http://qiiing.com 
#       功能  :
# ---------------------------------------------------
import time


def timestamp(timestamp=time.time(), thirteen=False):
    """
    获取时间戳
    :param timestamp: 时间戳
    :param thirteen: 取三十位
    :return:
    """
    if thirteen:
        return int(timestamp)
    else:
        return int(timestamp * 1000)


def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    """
    将时间转化为时间戳
    :param date:
    :param format_string:
    :return:
    """
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp


def timestamp_to_date(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    """
    将时间戳转换为时间
    :param time_stamp:
    :param format_string:
    :return:
    """
    time_array = time.localtime(time_stamp)
    str_date = time.strftime(format_string, time_array)
    return str_date


def now(get13 = False):
    """
    返回现在整数时间戳
    :param get13:
    :return:
    """
    if get13:
        return int(round(time.time() * 1000))
    else:
        return int(time.time())