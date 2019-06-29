#!/usr/bin/env python3
# -*-coding:utf-8-*-

# pyrec.py 文件内容
import pyaudio
import wave
from pyaudio import paInt16,PyAudio
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import pydub
import time

def audio_split(path,min_sl=300,sth=-40):
    """
    sgm:AudioSegment 对象
    silence_thresh=-70 # 小于-70dBFS以下的为静默 
    min_silence_len=700 # 静默超过700毫秒则拆分 
    length_limit=60*1000 # 拆分后每段不得超过1分钟 
    abandon_chunk_len=500 # 放弃小于500毫秒的段 
    joint_silence_len=1300 # 段拼接时加入1300毫秒间隔用于断句
    """
    if os.path.isfile(path):
        dp=os.path.splitext(path)
        if os.path.splitext(path)[1] in ['.mp3','.wav','.flv','.ogg','.raw','.m4a']:
            sgm=AudioSegment.from_file(path,format=dp[1].replace('.',''))
            chunks=split_on_silence(sgm,min_silence_len=min_sl,silence_thresh=sth)
            return chunks
        else:
            print('%s is not audio file,Please input audio file....'%path)
            sys.exit()

    elif isinstance(path,pydub.audio_segment.AudioSegment):
        #sgm=path
        chunks=split_on_silence(path,min_silence_len=min_sl,silence_thresh=sth)
        return chunks
    else:
        print('Input is not audio file or AudioSegment')
        sys.exit()
        return


def Topcm(wav_file,min_sl=300,sth=-40,duration=60):
    chunks=audio_split(wav_file,min_sl=min_sl,sth=sth)
    pf=[]
    if (chunks is not None) and (len(chunks)>0):
        ofile=os.path.splitext(wav_file)[0]
        if not os.path.exists(ofile):
            try:
                os.mkdir(ofile)
            except:
                os.makedirs(ofile)
        for i,wav in enumerate(chunks):
            if len(wav)/1000>60:
                sounds=[wav[i:i+duration*1000] for i in range(0,len(wav),duration*1000)]
                for w in sounds:
                    path=ofile+'/%s_%s.wav'%(str(i).zfill(3),int(time.time()*1000000))
                    w.export(path,format='wav')
                    pf.append(wav2pcm(path))
                    #pf.append(path)
            else:
                path=ofile+'/%s.wav'%str(i).zfill(3)
                wav.export(path,format='wav')
                pf.append(wav2pcm(path))
                #pf.append(path)
    return pf

def pyrec(file_name,CHUNK = 1024,FORMAT = paInt16,CHANNELS = 2,RATE = 16000,RECORD_SECONDS = 2):
    p = PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("开始录音,请说话......")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("录音结束,请闭嘴!")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return

def wav2pcm(wav_file):
    # 假设 wav_file = "音频文件.wav"
    # wav_file.split(".") 得到["音频文件","wav"] 拿出第一个结果"音频文件"  与 ".pcm" 拼接 等到结果 "音频文件.pcm"
    pcm_file = os.path.splitext(wav_file)[0]+'.pcm'
    #pcm_file = "%s.pcm" %(wav_file.split(".")[0])

    # 就是此前我们在cmd窗口中输入命令,这里面就是在让Python帮我们在cmd中执行命令
    os.system("ffmpeg -y  -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s"%(wav_file,pcm_file))

    return pcm_file
