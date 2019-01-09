#!/usr/bin/env python3
# -*-coding:utf-8-*-

import os
import sys
import wave
import numpy as np 
from datetime import datetime
from pyaudio import PyAudio, paInt16
from pydub import AudioSegment
from AI.KDXF.XF import audio2str,str2audio
from AI.BDAI.tts import BD_text2audio,BD_audio2text

    
class GenAudio(object):
    def __init__(self,duration=8,chunk=1024):
        self.num_samples = 2000    #pyaudio内置缓冲大小
        self.sampling_rate = 8000  #取样频率
        self.level = 1500          #声音保存的阈值
        self.count_num = 20        #count_num个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音
        self.save_length = 8       #声音记录的最小长度：save_length * num_samples 个取样
        self.time_count = duration        #录音时间，单位s
        self.voice_string = []
        self.chunk=chunk


    def asr_xf(self,fpath):
        """
        语音转化为文字，利用科大讯飞的接口
        """
        extend=os.path.splitext(fpath)
        Tem=AudioSegment.from_file(fpath,format=extend[1].replace('.',''))
        for i,chunk in enumerate(Tem[::10*1000]):
            path='audio/sound_%s.wav'%i
            with open(path,'wb') as f:
                chunk.export(f,format='wav')
            audio2str(path)
            os.remove(path)
        
    def asr_bd(self,fpath):
        """
        语音转化为文字，利用百度的接口
        """        
        extend=os.path.splitext(fpath)
        Tem=AudioSegment.from_file(fpath,format=extend[1].replace('.',''))
        for i,chunk in enumerate(Tem[::10*1000]):
            path='audio/sound_%s.wav'%i
            with open(path,'wb') as f:
                chunk.export(f,format='wav')
            d=audioTtext(path)
            print(d['result'])
            os.remove(path)        
        
    #保存文件
    def save_wav(self, filename):
        wf = wave.open(filename, 'wb') 
        wf.setnchannels(1) 
        wf.setsampwidth(2) 
        wf.setframerate(self.sampling_rate) 
        wf.writeframes(np.array(self.voice_string).tostring())
        wf.close()

    def Towav(self,fpath):
        extend=os.path.splitext(fpath)
        Tem=AudioSegment.from_file(fpath,format=extend[1].replace('.',''))
        Tem.export(extend[0]+'.wav',format='wav')

    def play(self,fpath):

        flag=False
        extend=os.path.splitext(fpath)
        if extend[0] != '.wav':
            self.Towav(fpath)
            fpath=extend[0]+'.wav'
            flag=True
        
        #define stream chunk 
        #chunk = 1024

        #open a wav format music
        f = wave.open(fpath,"rb")
        #instantiate PyAudio
        p = PyAudio()
        #open stream
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                    channels = f.getnchannels(),
                    rate = f.getframerate(),
                    output = True)
        #read data
        data = f.readframes(self.chunk)

        #paly stream
        while data:
            stream.write(data)
            data = f.readframes(self.chunk)

        #stop stream
        stream.stop_stream()
        stream.close()

        #close PyAudio
        p.terminate()
        if flag:
            os.remove(fpath)

    
    
    def record(self):
        pa = PyAudio() 
        stream = pa.open(format=paInt16, channels=1, rate=self.sampling_rate, input=True, frames_per_buffer=self.num_samples) 
        
        save_count = 0
        save_buffer = [] 
        time_count = self.time_count

        while True:
            time_count -= 1
            
            # 读入num_samples个取样
            string_audio_data = stream.read(self.num_samples)     
            # 将读入的数据转换为数组
            audio_data = np.fromstring(string_audio_data, dtype = np.short)
            #计算大于 level 的取样的个数
            large_sample_count = np.sum(audio_data > self.level)
            
            print(np.max(audio_data)),  "large_sample_count=>", large_sample_count

            # 如果个数大于COUNT_NUM，则至少保存SAVE_LENGTH个块
            if large_sample_count > self.count_num:
                save_count = self.save_length
            else: 
                save_count -= 1
            if save_count < 0:
                save_count = 0
            
            if save_count > 0:
                save_buffer.append(string_audio_data)
            else:
                if len(save_buffer) > 0:
                    self.voice_string = save_buffer
                    save_buffer = [] 
                    print("Recode a piece of  voice successfully!")
                    return True
            
            if time_count == 0: 
                if len(save_buffer) > 0:
                    self.voice_string = save_buffer
                    save_buffer = []
                    print("Recode a piece of  voice successfully!")
                    return True
                else:
                    return False
        return True


if __name__ == "__main__":
    r = GenAudio()
    r.record()
    r.save_wav("./test.wav")
