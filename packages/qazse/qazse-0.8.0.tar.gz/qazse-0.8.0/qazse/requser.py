#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------
#       项目名: qazse   
#       文件名: requser 
#       作者  : Qazse 
#       时间  : 2019/4/13
#       主页  : http://qiiing.com 
#       功能  :
# ---------------------------------------------------

import requests
import qazse


def useragent(device=0):
    """
    返回一个头
    :param device:
    :return:
    """
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
        'cache-control': "no-cache",
    }
    return headers


def request_get(url, params=None, proxy=None, encoding=None, **kwargs):
    """
    get参数
    :param url:
    :param params:
    :param proxy:
    :param kwargs:
    :return:
    """
    from requests.adapters import HTTPAdapter
    if proxy:
        proxies = {
            'http': 'http://%s' % proxy,
            'https': 'https://%s' % proxy
        }
    else:
        proxies = {
            'http': None,
            'https': None
        }
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    try:
        response = requests.get(url, params, proxies=proxies, headers=useragent(), **kwargs)
        if encoding:
            response.encoding = encoding
        return response
    except requests.exceptions.RequestException as e:
        print(e)
        return None


def max_request_get(urls_info, max_pool=100, config=None):
    """
    多线程读HTTP
    :param urls: dict
        {
            url:'http://xxx', 地址
            data:'xxx',   数据
            proxy:'data', 代理
            method:"GET", 方法
            headers:"",   头
            save_name:"", 保存文件名
            save_type:1   保存方法 1 文件 2 mongodb
        }
    :param max_pool: 最大线程
    :param config:
        {
            directory:"path", 保存路径
            save_db:"",       保存mongodb 对象
            save_status_200:true, 只保存http=200
            show_log:true       显示日志
        }

    eg:

    if __name__ == '__main__':

    db = qazse.db.mongodb_db('192.168.1.10')
    db = db.hf
    set = db.article
    urls = []
    for id in range(1,7000): # id范围
        url = {
            "url": 'https://m.aihanfu.com/index.php?m=wap&c=api&a=get_one_info&catid=53&id=%s&zipImg=0' % resid,
            "name": '%s.json' % id,
            "save_type":2
        }
        urls.append(url)
    config = {
        "save_db":set
    }
    qazse.requser.max_request_get(urls,max_pool=100,config=config) # 线程数量

    :return:
    """
    directory = config.get('directory', 'data')
    save_status_200 = config.get('save_status_200', True)
    show_log = config.get('show_log', True)
    save_db = config.get('save_db', qazse.db.mongodb_db())
    import json
    import aiohttp, asyncio
    from qazse import file

    file.mkdir(directory)

    async def main(pool):  # aiohttp必须放在异步函数中使用
        tasks = []
        sem = asyncio.Semaphore(pool)  # 限制同时请求的数量
        for url_info in urls_info:
            tasks.append(control_sem(sem, url_info))
        await asyncio.wait(tasks)

    async def control_sem(sem, url_info):  # 限制信号量
        async with sem:
            await fetch(url_info)

    async def fetch(url_info):
        # 解析配置
        url = url_info.get('url')
        data = url_info.get('data', '')
        method = url_info.get('method', 'GET')
        proxy = url_info.get('proxy', '')
        headers = url_info.get('headers', useragent())
        save_name = url_info.get('save_name', '%s.html' % url)
        save_type = url_info.get('save_type', 1)


        async with aiohttp.request(method, url_info.get('url'), data=data, headers=headers, proxy=proxy) as resp:
            if show_log:
                print('Download', url, method, proxy, resp.status,save_status_200,save_type)
            if save_status_200 and resp.status == 200:
                if save_type == 1:
                    file.write_file(await resp.read(), file_path=directory + '/' + save_name)
                elif save_type == 2:
                    data = await resp.read()
                    try:
                        save_db.insert(json.loads(data))
                    except json.decoder.JSONDecodeError:
                        pass
            elif not save_status_200:
                if save_type == 1:
                    file.write_file(await resp.read(), file_path=directory + '/' + save_name)
                elif save_type == 2:
                    data = await resp.read()
                    try:
                        save_db.insert(json.loads(data))
                    except json.decoder.JSONDecodeError:
                        pass

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(pool=max_pool))


