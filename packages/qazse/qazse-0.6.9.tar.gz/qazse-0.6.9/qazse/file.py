#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------
#       项目名: qazse   
#       文件名: file 
#       作者  : Qazse 
#       时间  : 2019/4/13
#       主页  : http://qiiing.com 
#       功能  :
# ---------------------------------------------------

def read_file_list(file_path, encoding='utf8'):
    """
    读取文件返回列表
    :param file: 文件目录
    :return:
    """
    file_list = []
    files = open(file_path, 'r', encoding=encoding)
    for file in files:
        file_list.append(file.strip())
    files.close()
    return file_list


def write_sql(sql, file_path='sql.sql', encoding='utf8',mode='a+'):
    """
    写sql
    :param sql: sql语句
    :param file_path: 写到目录
    :return:
    """
    with open(file_path, mode, encoding=encoding) as f:
        sql =str(sql)
        if not ';' in sql:
            sql = sql + ';'
        if not '\n' in sql:
            sql = sql + '\n'
        f.write(sql)

def write_text(text, file_path='text.txt', encoding='utf8',mode='a+'):
    """
    写text
    :param text:
    :param file_path: 写到目录
    :return:
    """
    with open(file_path, mode, encoding=encoding) as f:
        text = str(text)
        if not '\n' in text and not 'b' in mode:
            text = text + '\n'
        f.write(text)


def write_file(data, file_path='text.txt',mode='wb+'):
    """
    写文件
    :param data:二进制数据
    :param file_path: 写到目录
    :return:
    """
    with open(file_path, mode) as f:
        f.write(data)

def mkdir(path):
    """
    创建目录
    :param path:
    :return:
    """
    import os
    try:
        os.makedirs(path)
    except:
        pass


def get_md5(bit):
    """
    获取md5
    :param bit:
    :return:
    """
    from hashlib import md5

    return md5(bit).hexdigest()


def del_file(path):
    """
    删除文件
    :param path:
    :return:
    """
    import os
    os.remove(path)