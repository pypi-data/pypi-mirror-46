#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------
#       项目名: qazse   
#       文件名: db 
#       作者  : Qazse 
#       时间  : 2019/4/18
#       主页  : http://qiiing.com 
#       功能  :
# ---------------------------------------------------
import redis

class redis_db():

    def __init__(self,host='192.168.1.10',port=6379,db=0,password=''):
        self.r = redis.Redis(host=host, port=port, db=db,password=password)


    def list_to_set(self,list,name='discharge'):
        """
        写list 到 set
        :param list:
        :param name:
        :return:
        """
        for data in list:
            self.r.sadd(name,data)

    def val_to_set(self,val,name='discharge'):
        """
        写值到set
        :param val:
        :param name:
        :return: 失败 返回 0
        """
        return self.r.sadd(name,val)


def export_db_to_model(host_prot, username, password, db, tables=None, outfile='models.py'):
    """
    导出数据库模型到文件
    :param host:
    :param username:
    :param password:
    :param tables:
    :param outfile:
    :return:
    """
    if tables:
        cmd = 'sqlacodegen --outfile=%s mysql://%s:%s@%s/%s --tables %s' %(outfile,username,password,host_prot,db,','.join(tables))
    else:
        cmd = 'sqlacodegen --outfile=%s mysql://%s:%s@%s/%s' % (outfile, username, password, host_prot, db)
    import os
    os.popen(cmd)


def mongodb_db(host=None,port=27017,password=None):
    """
    返回一个mongodb存储对象
    :param mongo_db_link:链接地址
    :return:
    """
    from pymongo import MongoClient

    if not host:
        host = 'localhost'
    return MongoClient(host=host,port=port,password=password)

if __name__ == '__main__':
    mongodb_db('192.168.1.10').test.test.insert({"name":"zhangsan","age":18})