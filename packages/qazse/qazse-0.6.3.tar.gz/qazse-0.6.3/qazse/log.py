#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------
#       项目名: qazse   
#       文件名: log 
#       作者  : Qazse 
#       时间  : 2019/4/13
#       主页  : http://qiiing.com 
#       功能  :
# ---------------------------------------------------

# logging.disable(logging.CRITICAL)   # 禁止输出日志
import logging
import os
import sys as _sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_sys.path.append(BASE_DIR)

def log(logger_name='log-log', log_file=os.path.join(BASE_DIR, 'log', 'log.log'), level=logging.DEBUG,
        console_level=logging.DEBUG):
    try:
        os.mkdir('log')
    except:
        pass
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)  # 添加日志等级

    # 创建控制台 console handler
    ch = logging.StreamHandler()
    # 设置控制台输出时的日志等级
    ch.setLevel(console_level)

    # 创建文件 handler
    fh = logging.FileHandler(filename=log_file, encoding='utf-8')
    # 设置写入文件的日志等级
    fh.setLevel(logging.DEBUG)
    # 创建 formatter
    formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(name)s %(levelname)s %(message)s')

    # 添加formatter
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # 把ch fh 添加到logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger