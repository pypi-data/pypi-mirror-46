#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------
#       项目名: qazse   
#       文件名: seo 
#       作者  : Qazse 
#       时间  : 2019/4/13
#       主页  : http://qiiing.com 
#       功能  :
# ---------------------------------------------------
import requests


def baidu_weight(text):
    """
    获取百度权重
    :param text:
    :return:
    """
    from bs4 import BeautifulSoup
    import difflib

    url = "https://www.baidu.com/s"
    querystring = {"wd": text}
    headers = {
        'accept': "application/json, text/javascript",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-CN,zh;q=0.9",
        'content-type': "application/x-www-form-urlencoded",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        'x-requested-with': "XMLHttpRequest",
        'cache-control': "no-cache",
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    max_index = 0
    h3_list = soup.find_all('em')
    for h3 in h3_list:
        s1 = h3.text
        index = difflib.SequenceMatcher(None, text, s1).quick_ratio()
        if max_index <= index:
            max_index = index
    return max_index
