#/usr/bin/env python3
#coding=utf8
""" 
有道翻译API
API key：1308315335
keyfrom：translatedavischan
http://fanyi.youdao.com/openapi.do?keyfrom=translatedavischan&key=1308315335&type=data&doctype=<doctype>&version=1.1&q=要翻译的文本 

参数说明：
　type - 返回结果的类型，固定为data
　doctype - 返回结果的数据格式，xml或json或jsonp
　version - 版本，当前最新版本为1.1
　q - 要翻译的文本，必须是UTF-8编码，字符长度不能超过200个字符，需要进行urlencode编码
　only - 可选参数，dict表示只获取词典数据，translate表示只获取翻译数据，默认为都获取
　注： 词典结果只支持中英互译，翻译结果支持英日韩法俄西到中文的翻译以及中文到英语的翻译
errorCode：
　0 - 正常
　20 - 要翻译的文本过长
　30 - 无法进行有效的翻译
　40 - 不支持的语言类型
　50 - 无效的key
　60 - 无词典结果，仅在获取词典结果生效
"""
import urllib
import urllib.request
import hashlib
import json
import random
import operator


def auTot(q):
    """
    可以实现中英文互译。
    """
    #appid = '1308315335'
    #keyfrom = 'translatedavischan'

    qcode=q.encode('utf8')
    qcode=urllib.parse.quote(qcode)

    url='http://fanyi.youdao.com/openapi.do?keyfrom=translatedavischan&key=1308315335&type=data&doctype=json&version=1.1&q=%s'%qcode
    

    TransRequest = urllib.request.Request(url)
    TransResponse = urllib.request.urlopen(TransRequest)
    TransResult = TransResponse.read().decode('utf8')
    #print(TransResult)
    data = json.loads(TransResult)
    

    try:
        print(data['translation'][0],'\n')
        #return data['translation'][0]
    except:
        pass
    try:
        print(data['basic']['explains'],'\n')
    except:
        pass
    try:
        print(data['web'])
    except:
        pass
    return data['translation'][0]


if __name__=="__main__":
    d=auTot("我爱你，老婆")
