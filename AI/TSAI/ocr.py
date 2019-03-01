#!/usr/bin/env python3
# -*-coding:utf-8-*-
import requests  
import hashlib  
import time  
import random
import base64
import json
import string  
from urllib.parse import quote
import os
import sys

def curlmd5(src):  
    m = hashlib.md5(src.encode('UTF-8'))  
    # 将得到的MD5值所有字符转换成大写
    return m.hexdigest().upper()

def get_file(fpath):
    #print(fpath)
    f=open(fpath,'rb')
    fbs=base64.b64encode(f.read())
    f.close()
    return fbs

def get_params(plus_item):
    # 请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效）  
    t = time.time()
    time_stamp=str(int(t))
    # 请求随机字符串，用于保证签名不可预测  
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))  
    # 应用标志，这里修改成自己的id和key  
    app_id = '1106853711'  
    app_key = 'xuGdBlFP7DRyEx4h'
    plus=get_file(plus_item)
    params = {'app_id':app_id,  
              'image':plus,
              'time_stamp':time_stamp,
              'nonce_str':nonce_str,
              #'sign':''
             }
    sign_before = ''
    # 要对key排序再拼接  
    for key in sorted(params):
        # 键值拼接过程value部分需要URL编码，URL编码算法用大写字母，例如%E8。quote默认大写。  
        sign_before += '{}={}&'.format(key,quote(params[key], safe=''))  
    # 将应用密钥以app_key为键名，拼接到字符串sign_before末尾  
    sign_before += 'app_key={}'.format(app_key)
    # 对字符串sign_before进行MD5运算，得到接口请求签名  
    sign = curlmd5(sign_before) 
    params['sign'] = sign
    return params


def TS_ocr(plus_item):    
    # 聊天的API地址    
    url = "https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr"      
    # 获取请求参数
    #if os.path.isfile(plus_item):
    #    plus_item=get_file(plus_item)
        
    #else:
    #plus_item = plus_item.encode('utf-8')  
    payload = get_params(plus_item)    
    # r = requests.get(url,params=payload)    
    r = requests.post(url,data=payload)    
    return r.json()

def TS_ocrTtext(plus_item):
    text=[]
    dd=TS_ocr(plus_item)
    if dd['msg'] == 'ok':
        for i in dd['data']['item_list']:
            text.append(i['itemstring'])
    else:
        print(dd['msg'])
    T='\n'.join(text)
    return T

def TS_ocr_text_dir(fpath):
    #dtext=[]
    
    #ff=open(textp,'a',encoding='utf8')
    for root,dirs,files in os.walk(fpath):
        for f in files:
            #print(f)
            if os.path.splitext(f)[1] in ['.jpg','.png''.jpeg']:
                f=os.path.abspath(root+'/'+f)
                #f=str(root+'/'+f)
                try:
                    #ddtext='\n'.join(TS_ocr_text(f))
                    #ff.write(ddtext)
                    #ff.flush()
                    print(f)
                    d=TS_ocr1By1(f)
                    if len(d.strip())>0:
                        os.remove(f)
                        print('remove file %s ...'%f)
                    #dtext.append('\n'.join(TS_ocr_text(f)))
                    time.sleep(0.5)
                except Exception as e:
                    pass
    return #dtext
                
def TS_ocr1By1(path):
    text='\n'.join(TS_ocrTtext(path))
    #print(text)
    fpath=os.path.abspath(path)
    name=os.path.splitext(path)[0]+'.txt'
    with open(name,'w',encoding='utf8') as f:
        f.write(text)
    return text

def TS_ocr1By1dir(dirname):
    for root,dirs,files in os.walk(dirname):
            if os.path.splitext(f)[1] in ['.jpg','.png''.jpeg']:
                f=os.path.abspath(root+'/'+f)
                try:
                    print(f)
                    d=TS_ocr1By1(f)
                    if len(d.strip())>0:
                        os.remove(f)
                        print('remove file %s ...'%f)
                    time.sleep(0.5)
                except Exception as e:
                    pass
    return
def TS_ocrAllInOnedir(dirname):
    Al='output_allinone.txt'
    ff=open(Al,'a',encoding='utf8')
    for root,dirs,files in os.walk(dirname):
        for f in files:
            if os.path.splitext(f)[1] in ['.jpg','.png''.jpeg']:
                f=os.path.abspath(root+'/'+f)
                try:
                    ddtext='\n'.join(TS_ocr_text(f))
                    print(f)
                    d=TS_ocr1By1(f)
                    if len(d.strip())>0:
                        ff.write(ddtext+'\n\n')
                        ff.write('-------------------- %s ----------------\n\n'%f)
                        ff.flush()                        
                        os.remove(f)
                        print('remove file %s ...'%f)
                    time.sleep(0.5)
                except Exception as e:
                    pass
    return
    
  
  
if __name__ == '__main__':    
    import sys
    #d=trans(sys.argv[1])
    #text=[]
    #dd=ocr(sys.argv[1])
    #for i in dd['data']['item_list']:
    #    text.append(i['itemstring'])
    text=TS_ocr_text_dir(sys.argv[1])
    #print(text)        
