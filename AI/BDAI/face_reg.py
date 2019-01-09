#!/usr/bin/env python3
# -*-coding:utf-8-*-

from aip import AipFace
from urllib import request
import sys

""" 你的 APPID AK SK """
#https://ai.baidu.com/docs#/Face-Python-SDK/top
APP_ID = '10969993'
API_KEY = 'PwYwEP8QpFctd7zE6uhmfdXL'
SECRET_KEY = 'sOBZWPrNL3W5cZMTkkLeOVxZPFzUzp9G'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_token(key,secrect):
    host ='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'%(key,secrect)
    req = request.Request(host)
    req.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = request.urlopen(req)
    content=response.read()
    if content:
        data=json(content)
        return data['access_token']
    else:
        sys.exit()


    """ 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def BD_detect(filePath):    
    image = get_file_content(filePath)

    """ 调用通用文字识别, 图片参数为本地图片 """
    #client.basicGeneral(image);

    """ 如果有可选参数 """
    options = {}
    options["max_face_num"] = 2
    options["face_fields"] = "age"

    """ 带参数调用通用文字识别, 图片参数为本地图片 """
    d=client.detect(image, options)

    return d
