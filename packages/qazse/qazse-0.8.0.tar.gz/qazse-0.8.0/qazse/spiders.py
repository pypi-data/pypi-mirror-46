#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------
#       项目名: qazse   
#       文件名: spiders 
#       作者  : Qazse 
#       时间  : 2019/4/13
#       主页  : http://qiiing.com 
#       功能  :
# ---------------------------------------------------
import qazse


def ask_get(resp_text,url, question_title_css='', question_content_css='', answers_css='', remove_keyword='', type='auto',
            coding=None):
    """
    问答提取工具
    :param resp_text:返回的内容
    :param question_title_css: 例如.question-name
    :param question_content_css:
    :param answers_css: list css样式
    :param remove_keyword: list
    :param type: 类型 baidu wukong zhihu auto
    :param coding:编码类型
    :return: list
    """
    from bs4 import BeautifulSoup

    wukong_question_title = '.question-name'
    wukong_question_content = '.question-text'
    wukong_answers = ['.answer-text']
    wukong_remove = ['分享', '举报', '展开全部', '\d+评论', '评论']

    baidu_question_title = '.ask-title'
    baidu_question_content = '.line.mt-5.q-content'
    baidu_answers = ['.line.content']
    baidu_remove = ['分享', '举报', '展开全部', '\d+评论', '评论']

    zhihu_question_title = '.QuestionHeader-title'
    zhihu_question_content = '.RichText.ztext'
    zhihu_answers = ['.RichContent-inner']
    zhihu_remove = ['分享', '举报', '展开全部', '\d+评论', '评论','谢邀','邀请']

    if type == 'auto':
        if 'baidu' in url:
            type = 'baidu'
        elif 'wukong' in url:
            type = 'wukong'
        elif 'zhidao.baidu.com' in url:
            type = 'zhihu'

    if type == 'baidu':
        question_title_css = baidu_question_title
        question_content_css = baidu_question_content
        answers_css = baidu_answers
        remove_keyword = baidu_remove
    elif type == 'wukong':
        question_title_css = wukong_question_title
        question_content_css = wukong_question_content
        answers_css = wukong_answers
        remove_keyword = wukong_remove
    elif type == 'zhihu':
        question_title_css = zhihu_question_title
        question_content_css = zhihu_question_content
        answers_css = zhihu_answers
        remove_keyword = zhihu_remove
    soup = BeautifulSoup(resp_text, features="lxml")
    question_title = soup.select_one(question_title_css).text
    question_title = qazse.text.remove_n_r(question_title)
    question_content = soup.select_one(question_content_css).text if (soup.select_one(question_content_css)) else ''
    question_content = qazse.text.remove_n_r(question_content)
    question_md5 = qazse.text.md5_str(question_title + question_content)
    answers = list()
    for css in answers_css:
        answers = answers + soup.select(css)
    answers_list = []
    for index, answer in enumerate(answers):
        answer = qazse.text.remove_keyword(answer.text, remove_keyword)
        answer_md5 = qazse.text.md5_str(answer)
        answers_list.append({
            'content': answer,
            'md5': answer_md5
        })
    return {
        "question_title": question_title,
        "question_content": question_content,
        "question_md5": question_md5,
        "answers": answers_list,
        "answer_count": len(answers_list),
        "url": url,
        "type": type,
    }


def article_get(resp_text,url,title_css,content_css,remove_keyword=''):
    """
    提取文章
    :param resp_text:
    :param url:
    :param title_css:
    :param content_css:
    :param remove_keyword:
    :return:
    """
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(resp_text, features="lxml")
    title = soup.select_one(title_css).text
    title = qazse.text.remove_n_r(title)
    title = qazse.text.remove_keyword(title, remove_keyword)
    content = soup.select_one(content_css)
    content = qazse.text.remove_n_r(content)
    content = qazse.text.remove_keyword(content, remove_keyword)
    md5 = qazse.text.md5_str(title + content)
    return {
        "title": title,
        "content": content,
        "md5": md5,
        "url": url,
    }
    pass

def browser(type = 1):
    """
    启动一个浏览器
    :param type: 1 chrome  2 firefox
    :return:
    """
    from selenium import webdriver
    if type == 1:
        b = webdriver.Chrome()
    elif type ==2:
        b = webdriver.Firefox()
    else:
        print('游览器类型不正确 1 chrome  2 firefox')
        return ''
    return b

def check_ban(page_source):
    """
    检查当前是否被禁止
    :param page_source:
    :return:
    """
    if '验证' in page_source:
        return True
    elif '异常' in page_source:
        return True
    else:
        return False

def check_ban_browser(browser,type = 1):
    """
    检测浏览器是否被禁止，如果被禁止将重启浏览器
    :param browser:
    :param method: 重启完毕要执行的函数
    :param type
    :return:
    """
    from selenium import webdriver
    if check_ban(browser.page_source):
        url = browser.back()
        url = browser.current_url
        browser.quit()
        if type == 1:
            browser = webdriver.Chrome()
        elif type ==2:
            browser = webdriver.Firefox()
        browser.get(url)
        browser.implicitly_wait(30)
        return browser,False
    else:
        return browser,True

def sogou_spider(keywords):
    """
    搜狗微信爬虫
    会激活一个google浏览器 环境尚未自动化配置 //todo
    2019年5月6日 16:53:25
    :param keywords:关键词们
    :return:
    """
    from bs4 import BeautifulSoup
    data = []
    b = browser()
    for keyword in keywords:
        def input_keyword(keyword,b):
            b.maximize_window()
            b.get('https://weixin.sogou.com/')
            b.implicitly_wait(30)
            b.find_element_by_class_name('query').clear()
            b.find_element_by_class_name('query').send_keys(keyword)
            b.find_element_by_class_name('swz').click()

        input_keyword(keyword,b)
        b,status = check_ban_browser(b)
        print(b.current_url)
        while status and b.current_url == 'https://weixin.sogou.com/':
            input_keyword(keyword,b)

        while '下一页' in b.page_source:
            b, status = check_ban_browser(b)
            while status and b.current_url == 'https://weixin.sogou.com/':
                input_keyword(keyword, b)

            b.implicitly_wait(30)
            soup = BeautifulSoup(b.page_source,'lxml')
            urls = soup.select('.txt-box h3 a')
            for url in urls:
                data.append({
                    'keyword':keyword,
                    'title':url.text,
                    'url':url['data-share']
                })
            b.find_element_by_link_text('下一页').click()
    b.quit()
    return data
