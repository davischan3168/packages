import requests
import urllib
import re
import time
import hashlib
import base64
import json
import struct
import os
import sys
from AI.BDAI.util import ReadinChunks_file,audio_play,ReadInChunks
#from webdata.util.hds import user_agent as hds
#from webdata.util.chrome_cookies import firefox_cookies as gcookies


def _getHeader(AUE,voice,engine,speed,volume,rate,pitch):
    """
    auf 	string 	是 	音频采样率，可选值：audio/L16;rate=8000，audio/L16;rate=16000 	audio/L16;rate=16000
    aue 	string 	是 	音频编码，可选值：raw（未压缩的pcm或wav格式），lame（mp3格式） 	raw
    voice_name 	string 	是 	发音人，可选值：详见发音人列表 	xiaoyan
    speed 	string 	否 	语速，可选值：[0-100]，默认为50 	50
    volume 	string 	否 	音量，可选值：[0-100]，默认为50 	50
    pitch 	string 	否 	音高，可选值：[0-100]，默认为50 	50
    engine_type 	string 	否 	引擎类型，可选值：aisound（普通效果），
                                intp65（中文），intp65_en（英文），
                                mtts（小语种，需配合小语种发音人使用），x（优化效果），默认为inpt65 	intp65
    text_type 	string 	否 	文本类型，可选值：text（普通格式文本），默认为text 	text
"""    
    curTime = str(int(time.time()))
    #curTime='%s'%int(time.time())
    param ={
        "aue":AUE,
        "auf":"audio/L16;rate=%s"%rate,
        "voice_name":voice,
        "engine_type":engine,
        "speed":speed,
        "pitch":pitch,
        "volume":volume
        }
        

                
    #param = "{\"aue\":\""+AUE+"\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\"xiaoyan\",\"engine_type\":\"intp65\",\"speed\":\""+speed+"\",\"volume\":\""+volume+"\"}"


    paramBase64= base64.b64encode(json.dumps(param).replace(' ', '').encode('utf8'))
    m2 = hashlib.md5()
    APPID = "5ae94345"
    API_KEY = "718ea4c61466265e4e88b1e6ecae2cd0"
    m2.update(API_KEY.encode('utf8') + curTime.encode('utf8') + paramBase64)
    checkSum = m2.hexdigest()
    header ={
        'X-CurTime':curTime,
        'X-Param':paramBase64,
        'X-Appid':APPID,
        'X-CheckSum':checkSum,
        #'user_agent':[i for i in hds().values()][0],
        'X-Real-Ip':'127.0.0.1',
        'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
        }
    return header

def _getBody(text):
        """text   待合成文本，使用utf-8编码，需urlencode，长度小于1000字节"""
        data = {'text':text}
        return data

def _writeFile(file, content):
    with open(file, 'wb') as f:
        f.write(content)
    #f.close()
    return

def KDXF_tts(text,AUE='raw',voice="xiaoyan",engine="intp65",speed="100",volume="70",rate="16000",pitch="50"):
        """
        text:为str，需要合成语音的内容。字节不超过1000个字符，对汉字而
             言不超过500个字
        """
        URL = "http://api.xfyun.cn/v1/service/v1/tts"
        #r = requests.post(URL,headers=getHeader(),data=getBody(text))
        r = requests.post(URL,headers=_getHeader(AUE,voice,engine,speed,volume,rate,pitch),data=_getBody(text))
        contentType = r.headers['Content-Type']
        if contentType == "audio/mpeg":
                sid = r.headers['sid']
                if AUE == "raw":
                        #print(r.content)
                        #writeFile("audio1/"+str(int(time.time())*1000)+sid+str(int(time.time()))+".wav",r.content)
                        _writeFile("audio/audio_%s.wav"%str(int(time.time()*10000)),r.content)
                else :
                        #print(r.content)
                        _writeFile("audio/audio_%s.mp3"%str(int(time.time()*10000)),r.content)
                        
                print ("success, sid = " + sid)
        else :
                print (r.text)
                pass
        return
    
def KDXF_str2audio(fpath,chunk=128,AUE='raw',voice="xiaoyan",engine="intp65",speed="35",volume="70",rate="16000",pitch="50",flag=True):
    """
    fpath:文件
    chunk:文件
    engine：为
    flag: 是否播放语音,True为播放,False为不播放
    """
    texts=[]
    if os.path.isfile(fpath):
        f=ReadinChunks_file(fpath,chunk_size=chunk)
        for line in f:
            line=line.strip().replace(' ','').replace('\n','').replace('-','')
            if len(line)>0:
                texts.append(line)
        

    elif isinstance(fpath,str):
        texts.append(fpath)
              
    else:
        sys.exit()

    
    URL = "http://api.xfyun.cn/v1/service/v1/tts"
    audios=[]
    for text in texts:
        text=text.replace('\n','')
        r = requests.post(URL,headers=_getHeader(AUE,voice,engine,speed,volume,rate,pitch),data=_getBody(text))
        contentType = r.headers['Content-Type']
        if contentType == "audio/mpeg":
            sid = r.headers['sid']
            if AUE == "raw":
                _writeFile("audio/"+sid+".wav", r.content)
                if flag:
                    audio_play("audio/"+sid+".wav")
            else :
                _writeFile("audio/"+sid+".mp3", r.content)
                if flag:
                    audio_play("audio/"+sid+".mp3")
            print ("success, sid = " + sid)
            audios.append(r.content)

        else:
            #print(contentType)
            print (r.text )
            pass
    return audios


def KDXF_audio2str(AUDIO_PATH,engine="sms16k",aue="raw"):
    f = open(AUDIO_PATH, 'rb')
    file_content = f.read()
    base64_audio = base64.b64encode(file_content)
    body = urllib.parse.urlencode({'audio': base64_audio}).encode('utf8')
    """音频数据，base64 编码后进行 urlencode，要求 base64 编码和 urlencode 后大小
    不超过2M，原始音频时长不超过60s"""
    
    url = 'http://api.xfyun.cn/v1/service/v1/iat'
    x_appid = "5ae94345"    
    api_key = "a8b94ef76fda8f87b990f24c660213d9"
    param = {"engine_type": engine, "aue":aue }
    
    
    """aue:音频编码，可选值：raw（未压缩的pcm或wav格式）、speex（speex格式）、speex-wb（宽频speex格式）
       speex_size 	string 	否 	speex音频帧率，speex音频必传
       engine_type 	string 	是 	引擎类型，可选值：sms16k（16k采样率普通话音频）、sms8k（8k采样率普通话音频）等，其他参见引擎类型说明
       scene 	string 	否 	情景模式 	main
       vad_eos 	string 	否 	后端点检测（单位：ms），默认1800 	2000
    """

    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf8'))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5(api_key.encode('utf8') + str(x_time).encode('utf8') + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}

    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()
    print(result.decode('utf8'))
    return

if __name__=="__main__":
    
    d=KDFX_str2audio(sys.argv[1])
    #str2audio()
