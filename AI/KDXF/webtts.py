
#-*- coding: utf-8 -*-
import requests
import time
import hashlib
import base64
import os
import sys
import json

URL = "http://api.xfyun.cn/v1/service/v1/tts"
AUE = "raw"
APPID = "5ae94345"
API_KEY = "718ea4c61466265e4e88b1e6ecae2cd0"

def getHeader(AUE,voice,engine,speed,volume,rate,pitch):
        """
        auf 	string 	是 	音频采样率，可选值：audio/L16;rate=8000，
                            audio/L16;rate=16000 	
        aue 	string 	是 	音频编码，可选值：raw（未压缩的pcm或wav格式），lame（mp3格式）
        voice_name 	string 	是 	发音人，可选值：详见发音人列表 	xiaoyan
        speed 	string 	否 	语速，可选值：[0-100]，默认为50 	50
        volume 	string 	否 	音量，可选值：[0-100]，默认为50 	50
        pitch 	string 	否 	音高，可选值：[0-100]，默认为50 	50
        engine_type 	string 	否 	引擎类型，可选值：aisound（普通效果），
                                    intp65（中文），intp65_en（英文），
                                    mtts（小语种，需配合小语种发音人使用），
                                    x（优化效果），
                                    默认为intp65 	intp65
        text_type 	string 	否 	文本类型，可选值：text（普通格式文本），
                           待合成文本，使用utf-8编码，需urlencode，长度小于1000字节,默认为text
        """
        curTime = str(int(time.time()))
        #ttp=ssml
        #param = "{\"aue\":\""+AUE+"\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\"xiaoyan\",\"engine_type\":\"intp65\"}"
        #print("param:{}".format(param))
        #paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
        
        param ={
        "aue":AUE,
        "auf":"audio/L16;rate=%s"%rate,
        "voice_name":voice,
        "engine_type":engine,
        "speed":speed,
        "pitch":pitch,
        "volume":volume
        }
        
        paramBase64= base64.b64encode(json.dumps(param).replace(' ', '').encode('utf8'))
        #print("x_param:{}".format(paramBase64))
        
        m2 = hashlib.md5()
        m2.update((API_KEY.encode('utf8') + curTime.encode('utf8') + paramBase64))
        
        checkSum = m2.hexdigest()
        #print('checkSum:{}'.format(checkSum))
        
        header ={
                'X-CurTime':curTime,
                'X-Param':paramBase64,
                'X-Appid':APPID,
                'X-CheckSum':checkSum,
                'X-Real-Ip':'127.0.0.1',
                'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
        }
        #print(header)
        return header

def getBody(text):
        data = {'text':text}
        #print(data)
        return data

def writeFile(fs, content):
    with open(fs, 'wb') as f:
        f.write(content)
    f.close()
    return

def KDXF_tts(text,AUE='raw',voice="xiaoyan",engine="intp65",speed="100",volume="70",rate="16000",pitch="50",path=''):
        """
        text:为str，需要合成语音的内容。字节不超过1000个字符，对汉字而
             言不超过500个字
        """
        r = requests.post(URL,headers=getHeader(AUE,voice,engine,speed,volume,rate,pitch),data=getBody(text))

        contentType = r.headers['Content-Type']
        if contentType == "audio/mpeg":
                if path=='':
                #sid = r.headers['sid']
                        if AUE == "raw":
                                #print(r.content)
                                path="audio/audio_%s.wav"%str(int(time.time()*10000))
                                #writeFile("audio/audio_%s.wav"%str(int(time.time()*10000)),r.content)
                                #writeFile("audio/"+str(int(time.time()))+sid+str(int(time.time()))+".wav", r.content)
                        else :
                                #print(r.content)
                                path="audio/audio_%s.mp3"%str(int(time.time()*10000))
                                #writeFile("audio/audio_%s.wav"%str(int(time.time()*10000)),r.content)
                                #writeFile("audio/"+str(int(time.time()))+"xiaoyan"+".mp3", r.content)
                writeFile(path,r.content)
                print ("success, sid = " + sid)
        else :
                print (r.text)
                #pass
        return 
def KDXF_ttsFile(path):
        """
        将一个文件或者一大段的文字转为
        """
        if isinstance(path,str):
                if os.path.isfile(path):
                        f=open(path,'r',encoding='utf8')
                        con=f.read().replace('\n','').replace('-','').replace('.','').replace(' ','').replace('|','')
                        f.close()
                else:
                        con=path.replace('\n','').replace('-','').replace('.','').replace(' ','')

                text=[]
                ilen=350
                if len(con)>ilen:
                        text=[con[i:i+ilen] for i in  range(0,len(con),ilen)]

                for i,co in enumerate(text):
                        d=KDXF_tts(co)

        return 
                        
if __name__=="__main__":
        #KDXF_ttsV(sys.argv[1])
        pass
