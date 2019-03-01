#!/usr/bin/env python3
# -*-coding:utf-8-*-

import requests
import time
import hashlib
import base64
import json
import sys
#from urllib import parse

URL = "http://webapi.xfyun.cn/v1/service/v1/ocr/general"
APPID = "5ae94345"
API_KEY = "069d8996e03e644d08458625df894f53"
def getHeader():
    curTime = str(int(time.time()))
    param = {"language": "cn|en", "location": "false"}
    param = json.dumps(param)
    #x_param = base64.b64encode(param.encode('utf-8'))
    #param = "{\"auto_rotate\":\"true\"}"
    paramBase64 = base64.b64encode(param.encode('utf-8'))

    m2 = hashlib.md5()
    str1 = API_KEY + curTime + str(paramBase64,'utf-8')
    m2.update(str1.encode('utf-8'))
    checkSum = m2.hexdigest()

    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header

def KDXF_ocr_general(path):
    """
    path: image file path,jpeg,
    """
    with open(path, 'rb') as f:
        f1 = f.read()

    f1_base64 = str(base64.b64encode(f1), 'utf-8')

    data = {
        'image': f1_base64
    }

    #headers=getHeader(language, location)
    r = requests.post(URL, data=data, headers=getHeader())
    result = str(r.content, 'utf-8')
    return result

def KDXF_OcrTtext(path):
    d=KDXF_ocr_general(path)
    ds=json.loads(d)
    text=[]
    if ds['code']=='0':
        df=ds['data']['block'][0]['line']
        #print(df)
        for i in df:
            text.append(i['word'][0]['content'])
        T='\n'.join(text)
        return T
    
if __name__=="__main__":
    d=KDXF_ocr_general(sys.argv[1])
    #print(result)
    #input("Entry the any key to exit")
