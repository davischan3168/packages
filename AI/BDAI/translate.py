#/usr/bin/env python3
#coding=utf8
 
#import httplib
import http.client as httplib
#import md5
import hashlib
import urllib
import random
import json
import sys



def BD_trans(text='apple',fromLang='auto',toLang='zh'):
    """
    auto 	自动检测
    zh 	中文
    en 	英语
    yue 	粤语
    wyw 	文言文
    jp 	日语
    kor 	韩语
    fra 	法语
    spa 	西班牙语
    th 	泰语
    ara 	阿拉伯语
    ru 	俄语
    pt 	葡萄牙语
    de 	德语
    it 	意大利语
    el 	希腊语
    nl 	荷兰语
    pl 	波兰语
    bul 	保加利亚语
    est 	爱沙尼亚语
    dan 	丹麦语
    fin 	芬兰语
    cs 	捷克语
    rom 	罗马尼亚语
    slo 	斯洛文尼亚语
    swe 	瑞典语
    hu 	匈牙利语
    cht 	繁体中文
    vie 	越南语
    """
    
    appid = '20170419000045174' 
    secretKey = 'X7AscyijNyhxLBW29yzz' 
    httpClient = None
    myurl = '/api/trans/vip/translate'
    #text=text.replace(' ','\n')
    #text = 'apple'
    #fromLang = 'en'
    #toLang = 'zh'
    #print(text)
    salt = random.randint(32768, 65536)

    sign = appid+text+str(salt)+secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode('utf8'))
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(text)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

    #print(myurl)
    try:
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
 
        #response
        response = httpClient.getresponse()
        content=response.read().decode("unicode_escape")
        ds=json.loads(content)['trans_result']
        #print(content)
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()

    return ds

if __name__=="__main__":
    ddd=BD_trans(text=sys.argv[1])
    pass
