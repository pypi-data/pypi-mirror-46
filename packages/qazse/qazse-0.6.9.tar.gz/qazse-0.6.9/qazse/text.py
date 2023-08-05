#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------
#       项目名: qazse   
#       文件名: text 
#       作者  : Qazse 
#       时间  : 2019/4/13
#       主页  : http://qiiing.com 
#       功能  :
# ---------------------------------------------------
import re


def remove_emoji(text):
    """
    删除emoji
    :param text:
    :return:
    """
    try:
        data = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        data = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return data.sub(u'', text)


def md5_str(text):
    """
    获取MD5
    :param text:
    :return:
    """
    from hashlib import md5

    return md5(str(text).encode()).hexdigest()

def md5_str_bit(content):
    """
    取md5 数据
    :param content:
    :return:
    """
    from hashlib import md5

    return md5(content).hexdigest()


def remove_keyword(text,keywords):
    """
    删除指定关键字,支持正则
    :param text:
    :param keyword:
    :return:
    """
    import re
    for keyword in keywords:
        # text = str(text).replace(keyword,'')
        text = re.sub(keyword,'',text)
    return remove_n_r(text)

def remove_url(text):
    """
    删除网页中的Url
    :param text:
    :return:
    """
    return re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','',text)


def remove_n_r(text):
    """
    删除空格。换行符
    :param text:
    :return:
    """
    return str(text).strip()

def remove_html_tag(html,tags = None):
    """
    删除HTML中的标签
    :param html:
    :param tags:
    :return:
    """
    from w3lib.html import remove_tags
    if tags:
        return remove_tags(html,which_ones=(tags))
    else:
        return remove_tags(html,keep=())

def json_dumps(json_data):
    """
    还原json文本
    :param json_data:
    :return:
    """
    import json
    return json.dumps(json_data)


if __name__ == '__main__':
    text = '<p>非常好看，穿出设计师设计出来的那种范来了，就完美了。</p><p><img src="49839281888"/></p>'
    print(remove_url(text))