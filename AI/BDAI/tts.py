#!/usr/bin/env python3
# -*-coding:utf-8-*-

import base64
from aip import AipSpeech
import requests
import json
import os
import datetime as dt
from AI.util.textsplit import BD_text_split
from pydub import AudioSegment
from pydub.playback import play
from AI.util.audiopy import audio2list
import time
try:
    from .util import ReadinChunks_file,audio_play,ReadInChunks
except:
    from util import ReadinChunks_file,audio_play,ReadInChunks

""" 你的 APPID AK SK """
APP_ID = '10947352'
API_KEY = 'gELihIXKQxswEye4Wb3gCdsb'
SECRET_KEY = '2krKB6kQxfCdeuIDjGzXOfmqis7c1ByH'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
"""
tex	String	合成的文本，使用UTF-8编码，请注意文本长度必须小于1024字节	是
lang	String	语言选择,填写zh	是
ctp	String	客户端类型选择，web端填写1	是
cuid	String	用户唯一标识，用来区分用户，填写机器 MAC 地址或 IMEI 码，长度为60以内	否
spd	String	语速，取值0-9，默认为5中语速	否
pit	String	音调，取值0-9，默认为5中语调	否
vol	String	音量，取值0-15，默认为5中音量	否
per	String	发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女	否
"""

def get_token():
    url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'
    r=requests.get(url%(API_KEY, SECRET_KEY))
    data=json.loads(r.text)
    return data['access_token']

def BD_text2audio(text,vol=15,per=1,spd=4,pit=5,aue=6,path=''):
    """
    tex:        合成的文本，使用UTF-8编码。小于512个中文字或者英文数字。
               （文本在百度服务器内转换为GBK后，长度必须小于1024字节）
    lan:        固定值zh。语言选择,目前只有中英文混合模式，填写固定值zh
    spd:	选填	语速，取值0-9，默认为5中语速
    pit:	选填	音调，取值0-9，默认为5中语调
    vol:        选填	音量，取值0-15，默认为5中音量
    per:	选填	发音人选择, 0为普通女声，1为普通男生，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女声
    
    """
    text=BD_text_split(text)
    for i in text:
        txt2mp3='http://tsn.baidu.com/text2audio?lan=zh&ctp=1&cuid=abcdxxx&tok=%s&tex=%s&vol=%s&per=%s&spd=%s&pit=%s&aue=%s'
        uurl=txt2mp3%(get_token(),i,vol,per,spd,pit,aue)
        rr=requests.get(uurl)
        if path=='':
            if aue==3:
                path='audio/auido_%s.mp3'%str(int(time.time()*10000))
            elif aue==6:
                path='audio/auido_%s.wav'%str(int(time.time()*10000))
            elif aue in [4,5]:
                path='audio/auido_%s.pcm'%str(int(time.time()*10000))
            
        if not isinstance(rr.content, dict):
            with open(path, 'wb') as f:
                f.write(rr.content)    
    return
            

#http://ai.baidu.com/docs#/ASR-Online-Python-SDK/top
# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
    
def BD_audio2text(filePath):
    #要对段保存有一段语音的语音文件进行识别
    # 识别本地文件
    
    d=client.asr(get_file_content(filePath), 'pcm', 16000, {
        'dev_pid': '1536',
        })

    # 从URL获取文件识别
    """client.asr('', 'pcm', 16000, {
        'url': 'http://121.40.195.233/res/16k_test.pcm',
        'callback': 'http://xxx.com/receive',
    })"""
    
    return d

def BD_audio2textAll(filePath):
    """
    将一个音频文件的长度大于1分钟的文件，将其分割为一个不超过1分钟
    文件，然后在进行语音识别。
    filePath:为音频文件的 地址。str
    """
    files=audio2list(filePath,duration=59,pcm=True)
    dicts={}
    #import json
    for i,f in enumerate(files):
        dicts[i]=BD_audio2text(f)
        os.remove(f)

    return dicts

def BD_textTaudio(text,vol=15,per=1,spd=3,pit=5,aue=6,path=''):
    """
    tex:        合成的文本，使用UTF-8编码。小于512个中文字或者英文数字。
                （文本在百度服务器内转换为GBK后，长度必须小于1024字节）
    lan:        固定值zh。语言选择,目前只有中英文混合模式，填写固定值zh
    spd:	选填	语速，取值0-9，默认为5中语速
    pit:	选填	音调，取值0-9，默认为5中语调
    vol:        选填	音量，取值0-15，默认为5中音量
    per:	选填	发音人选择, 0为普通女声，1为普通男生，
                        3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女声
    aue	        选填	3为mp3格式(默认)； 4为pcm-16k；5为pcm-8k；6为wav（内容同
                        pcm-16k）; 
                        注意aue=4或者6是语音识别要求的格式，但是音频内容不是语音识别要求的自然人发音，所以识别效果会受影响。
    
    """
    textlist=BD_text_split(text)
    for text in textlist:
        result  = client.synthesis(text, 'zh', 1, {
            'vol': vol,
            'spd':spd,
            'pit':pit,
            'per':per,
            'aue':aue
        
        })

        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
        if path=='':
            if aue==3:
                path='audio/auido_%s.mp3'%(dt.datetime.strftime(dt.datetime.now(),'%Y-%m-%d-%H:%M:%S'))
            elif aue==6:
                path='audio/auido_%s.wav'%(dt.datetime.strftime(dt.datetime.now(),'%Y-%m-%d-%H:%M:%S'))

        if not isinstance(result, dict):
            #data=base64.b64decode(result)
            if aue==6:
                audiof=AudioSegment(result)
                play(audiof)
            with open(path, 'wb') as f:
                f.write(result)

    return result

if __name__=="__main__":
    uu='''天接云涛连晓雾，星河欲转千朝舞。仿佛梦魂归帝所。闻天语，殷勤问我归何处。
我报路长嗟日暮，学诗漫有惊人句。九万里风鹏正举。风休住，蓬舟吹取三山去！'''
    yu=BD_textTaudio(uu)
    #os.system('mplayer auido.mp3')
