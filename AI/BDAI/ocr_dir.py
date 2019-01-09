#!/usr/bin/env python3
# -*-coding:utf-8-*-

from aip import AipOcr
from urllib import request
import sys
import os

""" 你的 APPID AK SK """
#http://ai.baidu.com/docs#/OCR-Python-SDK/top
APP_ID = '10947557'
API_KEY = 'KxCS71VeSUFLk00pUvk641Xz'
SECRET_KEY = 'R8cnb80t6CmYXefE7aYzhro1goMLCjyZ'

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

def picTword(filePath):    
    image = get_file_content(filePath)

    """ 调用通用文字识别, 图片参数为本地图片 """
    #client.basicGeneral(image);

    """ 如果有可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"

    """ 带参数调用通用文字识别, 图片参数为本地图片 """
    d=client.basicGeneral(image, options)#用完500次后可改respon = client.basicAccurate(image)

    #url = "https//www.x.com/sample.jpg"

    """ 调用通用文字识别, 图片参数为远程url图片 """
    #client.basicGeneralUrl(url);

    """ 如果有可选参数 """
    #options = {}
    #options["language_type"] = "CHN_ENG"
    #options["detect_direction"] = "true"
    #options["detect_language"] = "true"
    #options["probability"] = "true"

    """ 带参数调用通用文字识别, 图片参数为远程url图片 """
    #client.basicGeneralUrl(url, options)
    return d

def jsonTtext(filePath):
    d=picTword(filePath)
    dd=[]
    for i in d['words_result']:
        dd.append(i['words'])

    text='\n'.join(dd)
    return text

def Pic_Text(filepath):
    text=[]
    for root,dirs,files in os.walk(filepath):
        for f in files:
            paf=os.path.join(root,f)
            try:
                txt=jsonTtext(paf)
                text.append(txt)
                print('page %s is ok'%f)
            except Exception as e:
                print(e)

    dd='\n\n'+'--'*30+'\n\n'
    ds=dd.join(text)
    f=open('test.txt','w',encoding='utf8')
    f.write(ds)
    f.close()
    return text

if __name__=="__main__":
    #text=jsonTtext(sys.argv[1])
    text=[]
    for root,dirs,files in os.walk(sys.argv[1]):
        for f in files:
            paf=os.path.join(root,f)
            try:
                txt=jsonTtext(paf)
                text.append(txt)
                print('page %s is ok'%f)
            except Exception as e:
                print(e)

    dd='\n\n'+'--'*30+'\n\n'
    ds=dd.join(text)
    f=open('test.txt','w',encoding='utf8')
    f.write(ds)
    f.close()
                
            
