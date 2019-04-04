#!/usr/bin/env python3
# -*-coding:utf-8-*-
import pyaudio
import wave
import sys
from pydub import AudioSegment
from pydub.playback import play
from pydub.silence import split_on_silence

def audio_split(sgm,min_sl=300,sth=-40):
    """
    sgm:AudioSegment 对象
    silence_thresh=-70 # 小于-70dBFS以下的为静默 
    min_silence_len=700 # 静默超过700毫秒则拆分 
    length_limit=60*1000 # 拆分后每段不得超过1分钟 
    abandon_chunk_len=500 # 放弃小于500毫秒的段 
    joint_silence_len=1300 # 段拼接时加入1300毫秒间隔用于断句
    """
    chunks=split_on_silence(sgm,min_silence_len=min_sl,silence_thresh=sth)
    return chunks



def ReadInChunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""

    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def ReadinChunks_file(fpath,chunk_size=1024):
    #with open(fpath,'r',encoding='utf8') as file_object:
    #    wts=ReadInChunks(file_object, chunk_size)
    file_object=open(fpath,'r',encoding='utf8')
    wts=ReadInChunks(file_object, chunk_size)
    return wts

p = pyaudio.PyAudio()
def audio_play(fpath):
    #define stream chunk 
    chunk = 1024

    #open a wav format music
    f = wave.open(fpath,"rb")
    #instantiate PyAudio
    #p = pyaudio.PyAudio()
    #open stream
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
				channels = f.getnchannels(),
				rate = f.getframerate(),
				output = True)
    #read data
    data = f.readframes(chunk)

    #paly stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)

    #stop stream
    stream.stop_stream()
    stream.close()

    #close PyAudio
    p.terminate()
    return

def record_audio(filename,DurationT=5):
    """
    filename:输出的文件名称,
    DurationT: 录音时间，单位s
    """
    chunk = 1024
    FORMAT=pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = DurationT
    filename = filename + '.wav'
    WAVE_OUPUT_FILENAME = filename

    #p = pyaudio.PyAudio()

    stream = p.open(format = FORMAT,
                        channels = CHANNELS,
                        rate = RATE,
                        input = True,
                        frames_per_buffer = chunk)

    print("* recording ......")
    alls=[]
    for i in range(0,int(RATE/chunk*RECORD_SECONDS)):
        data = stream.read(chunk)
        alls.append(data)

    print("* done recording")

    stream.close()
    p.terminate()


    #write data to Wave file
    data=b''.join(alls)
    wf=wave.open(WAVE_OUPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()
    return


        
        

if __name__=="__main__":
    record_audio(sys.argv[1])
    #pass
