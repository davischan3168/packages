#!/usr/bin/env python3
# -*-coding:utf-8-*-

import sys,os,time
import MySQLdb
#import webdata as wd
from AI.TSAI import tts
import requests
import hashlib, base64
import json
import string  
from urllib.parse import quote
import AI as ai

conn = MySQLdb.connect(host="localhost", port=3306, user='root', passwd='801019', db='SDD', charset="utf8")
cur = conn.cursor()

def get_ChengYu():
    """
    Parameters:
        author:按作者
        mtype:分为article,kindle
        pyin: 主体部分是否要标拼音
        ywT:是否要翻译部分
    """        
    
    sqll="select name,means from Chengyu"
    #sqll="select * from gushiwen"
    cur.execute(sqll)
    c=[]
    text=cur.fetchall()
    """
    for i in dd:
        c.append(','.join(i))
        
    d=set(c)
    text=list(d)
    """
    return text

def _getAudio(plus_item):
    url = "https://api.ai.qq.com/fcgi-bin/aai/aai_tts"

    plus_item = plus_item.encode('utf-8')
    payload = tts.get_params(plus_item,appid='1106853711',app_key= 'xuGdBlFP7DRyEx4h',spk='1',fmt='2',vlm='0',spd='80')
    #print(payload)
    r = requests.post(url,data=payload)
    #print(r.text)
    ad=r.json()['data']['speech']
    data=base64.b64decode(ad)
    return data


def ToAudio(text):
    if isinstance(text,tuple):
        for i in text:
            path='/mnt/f/Chengyu/'+i[0]+'.wav'
            if not os.path.exists(path):
                cnt=_getAudio(','.join(i))
                if len(cnt)>0:
                    with open(path,'wb') as f:
                        f.write(cnt)
                else:
                    #cnt=ai.BD_text2audio(','.join(i),path=path)
                    cnt=ai.KDXF_tts(','.join(i),path=path)
                time.sleep(0.2)
                    
                

    return

            
    
if __name__=="__main__":
    
    for root,ds,fs in os.walk('/mnt/f/Chengyu'):
        for f in fs:
            path=os.path.abspath(root+'/'+f)
            if os.path.getsize(path) == 0:
                os.remove(path)
                print('Delected file : %s.'%path)


    dd=get_ChengYu()
    ToAudio(dd)
    
