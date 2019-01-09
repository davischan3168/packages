#!/usr/bin/env python3
# -*-coding:utf-8-*-
import requests
import time
import random
import hashlib, base64
import json
import string  
from urllib.parse import quote


def curlmd5(src):  
    m = hashlib.md5(src.encode('UTF-8'))  
    # 将得到的MD5值所有字符转换成大写
    return m.hexdigest().upper()

def get_file(fpath):
    f=open(fpath,'rb')
    fbs=base64.b64encode(f.read())
    f.close()
    return fbs

def get_params(plus_item):
    appid = '1106853711'
    #secret_id = '1106853711'
    app_key = 'xuGdBlFP7DRyEx4h'
    #t = time.time()
    #time_stamp=str(int(t))

    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 17))  
    args = {
        'app_id': appid,
        'time_stamp': str(int(time.time())),
        'nonce_str':nonce_str,
        #'speaker':'1',#
        #'format':'2',
        #'volume':'0',
        #'speed':'100',
        #'aht':'0',
        'type':'0',
        'text':plus_item
        }

    sign_before = ''
    for key in sorted(args):
         sign_before += '{}={}&'.format(key,quote(args[key], safe=''))

    sign_before += 'app_key={}'.format(app_key)
    sign = curlmd5(sign_before)
    args['sign']=sign
    return args

def TS_trans(plus_item):
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_texttrans"

    plus_item = plus_item.encode('utf-8')
    payload = get_params(plus_item)
    #print(payload)
    r = requests.post(url,data=payload)
    #print(r.text)
    ad=r.json()['data']['trans_text']
    #data=base64.b64decode(d)
    
    return ad

def TS_speechtranslate(fpath,fr='zh',to='en'):
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_speechtranslate"

    dt=get_file(fpath)

    appid = '1106853711'
    app_key = 'xuGdBlFP7DRyEx4h'

    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 17))  
    args = {
        'app_id': appid,
        'time_stamp': str(int(time.time())),
        'nonce_str':nonce_str,
        'format':'8',
        'seq':'0',
        'end':'1',
        'session_id':'test1',
        'speech_chunk':dt,
        'source':fr,
        'target':to,
        }

    sign_before = ''
    for key in sorted(args):
         sign_before += '{}={}&'.format(key,quote(args[key], safe=''))

    sign_before += 'app_key={}'.format(app_key)
    sign = curlmd5(sign_before)
    args['sign']=sign
    
    #print(payload)
    r = requests.post(url,data=args)
    #ad=r.json()['data']['source_text']
    #ad1=r.json()['data']['target_text']
    #data=base64.b64decode(d)
    
    return r.json()
    
def TS_imagetranslate(fpath,fr='zh',to='en'):
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_imagetranslate"

    dt=get_file(fpath)

    appid = '1106853711'
    app_key = 'xuGdBlFP7DRyEx4h'

    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 17))  
    args = {
        'app_id': appid,
        'time_stamp': str(int(time.time())),
        'nonce_str':nonce_str,
        'scene':'doc',
        'session_id':'test2093',
        'image':dt,
        'source':fr,
        'target':to,
        }

    sign_before = ''
    for key in sorted(args):
         sign_before += '{}={}&'.format(key,quote(args[key], safe=''))

    sign_before += 'app_key={}'.format(app_key)
    sign = curlmd5(sign_before)
    args['sign']=sign
    
    #print(payload)
    r = requests.post(url,data=args)
    #ad=r.json()['data']['source_text']
    #ad1=r.json()['data']['target_text']
    #data=base64.b64decode(d)
    
    return r.json()

def TS_img_trans_text(fpath):
    source=[]
    target=[]
    dd=imagetranslate(fpath)
    for i in dd['data']['image_records']:
        source.append(i['source_text'])
        target.append(i['target_text'])
    return source,target


if __name__ == '__main__':
    import sys
    #d=trans(sys.argv[1])
    dd=imagetranslate(sys.argv[1])
    for i in dd['data']['image_records']:
        print(i['source_text'])
        print(i['target_text'])

    print(dd)
