#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------
#       项目名: qazse   
#       文件名: upload 
#       作者  : Qazse 
#       时间  : 2019/5/8
#       主页  : http://qiiing.com 
#       功能  :
# ---------------------------------------------------
import qazse


def upload_qiniu(qiniu_config, file_config):
    """
    上传文件到七牛
    :param access_key:
        qiniu = {
        "access_key":'xxx',
        "secret_key":'xxx',
        "bucket_name":'xxx',
        }
    :param secret_key:
    :param bucket_name:
    :return:
    """

    from qiniu import Auth, put_file, etag
    import requests
    qazse.file.mkdir('data')
    # 需要填写你的 Access Key 和 Secret Key
    access_key = qiniu_config.get('access_key')
    secret_key = qiniu_config.get('secret_key')
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = qiniu_config.get('bucket_name')
    # 上传后保存的文件名
    key = file_config.get('classify', '') + file_config.get('key', '')
    # 生成上传 Token，可以指定过期时间等

    # 要上传文件的本地路径
    file_path = file_config.get('file_path')
    if 'http://' in file_path or 'https://' in file_path:
        reps = requests.get(file_path)
        if reps.status_code == 200:
            md5 = qazse.file.get_md5(reps.content)
            if not file_config.get('key', ''):
                key = file_config.get('classify', '') + str(md5)
            qazse.file.write_file(reps.content, 'data.dat',mode='wb+')
            file_path = 'data.dat'
    token = q.upload_token(bucket_name, key, 3600)
    ret, info = put_file(token, key, file_path)
    return ret

