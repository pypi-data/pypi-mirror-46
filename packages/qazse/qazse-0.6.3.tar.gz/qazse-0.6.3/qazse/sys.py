#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------
#       项目名: qazse   
#       文件名: wq 
#       作者  : Qazse 
#       时间  : 2019/4/13
#       主页  : http://qiiing.com 
#       功能  :
# ---------------------------------------------------


def write_text_clipboard(text):
    """
    写文本到剪切板
    :param text:
    :return:
    """
    import pyperclip
    pyperclip.copy(text)


def copy_text_from_clipboard():
    """
    读取剪切板的文本
    :return:
    """
    import pyperclip
    return pyperclip.paste()