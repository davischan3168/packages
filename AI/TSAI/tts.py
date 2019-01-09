#!/usr/bin/env python3
# -*-coding:utf-8-*-
import requests
import time
import random
import hashlib, base64
import json
import string  
from urllib.parse import quote
from AI.BDAI.util import audio_play
import os
import re
import sys
from pydub import AudioSegment
from pydub.playback import play


def curlmd5(src):  
    m = hashlib.md5(src.encode('UTF-8'))  
    # 将得到的MD5值所有字符转换成大写
    return m.hexdigest().upper()

def get_params(plus_item,appid,app_key,spk,fmt,vlm,spd):
    #appid = '1106853711'
    #secret_id = '1106853711'
    #app_key = 'xuGdBlFP7DRyEx4h'
    #t = time.time()
    #time_stamp=str(int(t))
    """
    speaker 	是 	int 	正整数 	1 	语音发音人编码，定义见下文描述
    format 	是 	int 	正整数 	2 	合成语音格式编码，定义见下文描述
    volume 	是 	int 	[-10, 10] 	0 	合成语音音量，
                取值范围[-10, 10]，如-10表示音量相对默认值小10dB，0表  示默认音量，10表示音量相对默认值大10dB
    speed 	是 	int 	[50, 200] 	100 	合成语音语速，默认100
    text 	是 	string 	UTF-8编码，非空且长度上限150字节 	腾讯，你好！ 	待合成文本
    aht 	是 	int 	[-24, 24] 	0 	合成语音降低/升高半音个数，即改变音高，默认0
    apc 	是 	int 	[0, 100] 	58 	控制频谱翘曲的程度，改变说话人的音色，默认58
    -----------------------------
    发音人 	编码
    普通话男声 	1
    静琪女声 	5
    欢馨女声 	6
    碧萱女声 	7
    ---------------------------
    格式名称 	编码
    PCM 	1
    WAV 	2
    MP3 	3
    """

    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 17))  
    args = {
        'app_id': appid,
        'time_stamp': str(int(time.time())),
        'nonce_str':nonce_str,
        'speaker':spk,#发音人
        'format':fmt,#格式
        'volume':vlm,#音量
        'speed':spd,#语音速度
        'aht':'0',#音高
        'apc':'58',#音色
        'text':plus_item#需要合成语音的文字
        }

    sign_before = ''
    for key in sorted(args):
         sign_before += '{}={}&'.format(key,quote(args[key], safe=''))

    sign_before += 'app_key={}'.format(app_key)
    sign = curlmd5(sign_before)
    args['sign']=sign
    return args

def writeFile(fs, content):
    with open(fs, 'wb') as f:
        f.write(content)
    f.close()
    return

def getAudio(plus_item,appid='1106853711',app_key= 'xuGdBlFP7DRyEx4h',spk='1',fmt='2',vlm='0',spd='80',path=''):
    """
    将文字转为语音
    spk,#发音人    发音人 	编码
        普通话男声 	1
        静琪女声 	5
        欢馨女声 	6
        碧萱女声 	7
    'format':fmt,#格式
            PCM 	1(path:/../..pcm,../..wav,..mp3)
            WAV 	2
            MP3 	3
    'volume':vlm,#音量
    'speed':spd,#语音速度
    'aht':'0',#音高
    'apc':'58',#音色
    'text':plus_item#需要合成语音的文字
    """
    url = "https://api.ai.qq.com/fcgi-bin/aai/aai_tts"

    plus_item = plus_item.encode('utf-8')
    payload = get_params(plus_item,appid,app_key,spk,fmt,vlm,spd)
    #print(payload)
    r = requests.post(url,data=payload)
    #print(r.text)
    ad=r.json()['data']['speech']
    data=base64.b64decode(ad)
    if path!='':
        with open(path,'wb') as f:
            f.write(data)
        return
    else:
        return data


    
def TS_tts(plus_item,appid='1106853711',app_key= 'xuGdBlFP7DRyEx4h',spk='1',fmt='2',vlm='0',spd='80'):
    """
    将文字转为语音
    spk,#发音人    发音人 	编码
        普通话男声 	1
        静琪女声 	5
        欢馨女声 	6
        碧萱女声 	7
    'format':fmt,#格式
            PCM 	1
            WAV 	2
            MP3 	3
    'volume':vlm,#音量
    'speed':spd,#语音速度
    'aht':'0',#音高
    'apc':'58',#音色
    'text':plus_item#需要合成语音的文字
    """
    url = "https://api.ai.qq.com/fcgi-bin/aai/aai_tts"

    plus_item = plus_item.encode('utf-8')
    payload = get_params(plus_item,appid,app_key,spk,fmt,vlm,spd)
    #print(payload)
    r = requests.post(url,data=payload)
    #print(r.text)
    ad=r.json()['data']['speech']
    data=base64.b64decode(ad)
    if fmt == "2" and len(data)>0:
        #print(r.content)
        writeFile('audio/auido_%s.wav'%str(int(time.time()*10000)), data)
    elif fmt == '3' and len(data)>0:
        #print(r.content)
        writeFile('audio/auido_%s.mp3'%str(int(time.time()*10000)), data)
    elif fmt == '1' and len(data)>0:
        #print(r.content)
        writeFile('audio/auido_%s.pcm'%str(int(time.time()*10000)), data)
    else:
        print("The len(text) is too long and the lenghth of audio is %s."%len(data))
    return


def TS_ttsTplay(plus_item,appid='1106853711',app_key= 'xuGdBlFP7DRyEx4h',spk='1',fmt='2',vlm='0',spd='100'):
    df=tts(plus_item,appid=appid,app_key=app_key,spk=spk,fmt=fmt,vlm=vlm,spd=spd)
    """
    if fmt=='2':
        fp='tempsdfre.wav'
        with open(fp,'wb') as f:
            f.write(df)
        audio_play(fp)
        os.remove(fp)
    """
    audio=AudioSegment(df)
    play(audio)

    return

def TS_ttsList(text,appid='1106853711',app_key='xuGdBlFP7DRyEx4h',spk='1',fmt='2',vlm='0',spd='100'):
    tems=[]
    if isinstance(text,str):
        text=re.sub('\n*','',text)
        #text=re.sub('\s*','',text)
        tems.append(text)
    elif isinstance(text,list):
        text=''.join(text)
        text=re.sub('\n*','',text)
        #text=re.sub('\s*','',text)
        tems.append(text)
        
        #tems.extend(text)
    else:
        sys.exit()

    #print(text)
    txt=''.join(tems)
    txtl=txt.replace('-','').replace(' ','')
    td=txtl.split('。')
    for i in td:
        if len(i)>0:
            print(i)
            try:
                ttsTplay(i,appid=appid,app_key=app_key,spk=spk,fmt=fmt,vlm=vlm,spd=spd)
            except:
                tem=[]
                tem.extend(i.split(','))
                #print(tem)
                for ii in tem:
                    try:
                        #print(ii)
                        TS_tts(i,appid=appid,app_key=app_key,spk=spk,fmt=fmt,vlm=vlm,spd=spd)
                        #ttsTplay(ii,appid=appid,app_key=app_key,spk=spk,fmt=fmt,vlm=vlm,spd=spd)
                    except:
                        pass
    return        
        

def TS_ttsFile(pfile,appid='1106853711',app_key= 'xuGdBlFP7DRyEx4h',spk='1',fmt='2',vlm='0',spd='100'):
    tl=open(pfile,'r')
    tx=tl.readlines()
    txt=''.join(tx)
    txtl=txt.replace('-','').replace(' ','')
    td=txtl.split('。')
    for i in td:
        if len(i)>0:
            print(i)
            try:
                TS_tts(i,appid=appid,app_key=app_key,spk=spk,fmt=fmt,vlm=vlm,spd=spd)
                #ttsTplay(i,appid=appid,app_key=app_key,spk=spk,fmt=fmt,vlm=vlm,spd=spd)
            except:
                tem=[]
                tem.extend(i.split(','))
                for ii in i:
                    try:
                        TS_tts(i,appid=appid,app_key=app_key,spk=spk,fmt=fmt,vlm=vlm,spd=spd)
                        #ttsTplay(ii,appid=appid,app_key=app_key,spk=spk,fmt=fmt,vlm=vlm,spd=spd)
                    except:
                        pass
    return
    


if __name__ == '__main__':
    #import sys
    pass
    #d=ttsTplay(sys.argv[1])
