# -*- coding: utf-8 -*-
import requests
import time
import hashlib
import base64
import sys
from AI.util.audiopy import audio2list

URL = "http://api.xfyun.cn/v1/service/v1/iat"
APPID = "5ae94345"
API_KEY = "a8b94ef76fda8f87b990f24c660213d9"


def getHeader(aue, engineType):
    curTime = str(int(time.time()))
    # curTime = '1526542623'
    param = "{\"aue\":\"" + aue + "\"" + ",\"engine_type\":\"" + engineType + "\"}"
    #print("param:{}".format(param))
    paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
    #print("x_param:{}".format(paramBase64))

    m2 = hashlib.md5()
    m2.update((API_KEY + curTime + paramBase64).encode('utf-8'))
    checkSum = m2.hexdigest()
    #print('checkSum:{}'.format(checkSum))
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    #print(header)
    return header


def getBody(filepath):
    #if os.path.isfile(filepath):
    binfile = open(filepath, 'rb')
    data = {'audio': base64.b64encode(binfile.read())}
    #print(data)
    #print('data:{}'.format(type(data['audio'])))
    #print("type(data['audio']):{}".format(type(data['audio'])))
    return data


#aue 
#engineType 
#audioFilePath =
#r"D:\webapidemo\iat_1130\webiat_demo\webiat_demo\resource\12.pcm"
    
    

def KDXF_aitFpcm(audioFilePath,aue= "raw",engineType= "sms16k"):
    """
    将音频文件转为文字。
    audioFilePath:音频文件,为pcm格式。
    """
    r = requests.post(URL, headers=getHeader(aue, engineType), data=getBody(audioFilePath))
    content=r.content.decode('utf-8')
    #print(r.content.decode('utf-8'))
    return content

def KDXF_aitFall(audioFilePath):
    """
    将一MP3、WAV 文件转为文字文件，即实施语音识别。
    """

    files=audio2list(audioFilePath,duration=15,pcm=True)
    dicts={}
    import json
    for i,path in enumerate(files):
        dicts[i]=json.loads(KDXF_aitFpcm(path))['data']
        os.remove(path)

    return dicts
    
    

if __name__=="__main__":
    ds=KDXF_aitFall(sys.argv[1])
