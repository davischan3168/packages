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

def TS_asr_echo(fpath):
    """
    将语音转为中文
    """
    url = "https://api.ai.qq.com/fcgi-bin/aai/aai_asr"

    #plus_item = plus_item.encode('utf-8')
    data=get_file(fpath)

    appid = '1106853711'
    app_key = 'xuGdBlFP7DRyEx4h'

    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 17))  
    args = {
        'app_id': appid,
        'time_stamp': str(int(time.time())),
        'nonce_str':nonce_str,
        'format':'3',
        'speech':data,
        'rate':'16000',
        }

    sign_before = ''
    for key in sorted(args):
         sign_before += '{}={}&'.format(key,quote(args[key], safe=''))

    sign_before += 'app_key={}'.format(app_key)
    sign = curlmd5(sign_before)
    args['sign']=sign    
    
    r = requests.post(url,data=args)
    ad=r.json()['data']['text']
    #data=base64.b64decode(ad)
    
    return ad
    
  
"""
query_str = "&".join(["%s=%s"%(k,args[k]) for k in sorted(args.keys())])
calc_str = "POSTaai.qcloud.com/tts/v1/%(appid)s?%(query_str)s"%vars()
hashed = hmac.new(secret_key.encode('utf8'), calc_str.encode('utf8'), hashlib.sha1)
headers = {"Authorization": base64.b64encode(hashed.digest())}

url = "http://aai.qcloud.com/tts/v1/%(appid)s?%(query_str)s"%vars()
upload_file = "test.txt"
files = {"file": open(upload_file, "rb")}
resp = requests.post(url=url, files=files, headers=headers)
resp = json.loads(resp.text)
data = base64.b64decode(resp["speech"])

f = open("hello.mp3", "w")
f.write(data)
f.close()"""

if __name__ == '__main__':
    import sys
    dd=asr_echo(sys.argv[1])
