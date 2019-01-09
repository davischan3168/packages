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
    auto 	�Զ����
    zh 	����
    en 	Ӣ��
    yue 	����
    wyw 	������
    jp 	����
    kor 	����
    fra 	����
    spa 	��������
    th 	̩��
    ara 	��������
    ru 	����
    pt 	��������
    de 	����
    it 	�������
    el 	ϣ����
    nl 	������
    pl 	������
    bul 	����������
    est 	��ɳ������
    dan 	������
    fin 	������
    cs 	�ݿ���
    rom 	����������
    slo 	˹����������
    swe 	�����
    hu 	��������
    cht 	��������
    vie 	Խ����
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
