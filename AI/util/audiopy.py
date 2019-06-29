#!/usr/bin/env python3
# -*-coding:utf-8-*-
import os
import sys
import time
from pydub import AudioSegment
from pydub.silence import split_on_silence
import pydub
audiolist=['.mp3','.wav','.flv','.ogg','.raw','.m4a']
##########################################
def audiosn_to_one(paths,sln=3.5,ntotal='max',repeat=1):
    """
    将文件夹下面的音频文件整合成，每个文件含有ntotal个音频的文件，重复
    次数为repeat次
    -----------------------------------------------------
    paths:  files to be combine together;paths or file.
    sln:   产生一个持续时间为sln seconds的无声AudioSegment对象
    ntotal:合成的音频文件中所含有的音频个数，max表示将目录下所有的音频
           文件合成在一个文件之中。
    repeat:表示重复的
    """
    sounds=[]
    if isinstance(paths,list):
        for path in paths:
            if os.path.isfile(path):
                dp=os.path.splitext(path)
                if dp[1] in audiolist:
                    sounds.append(AudioSegment.from_file(root+'/'+f,format=dp[1].replace('.','')))

    elif os.path.isdir(paths):
        for root,dirs,files in os.walk(paths):
            for f in files:
                dp=os.path.splitext(f)
                if dp[1] in audiolist:
                    print(f)
                    sounds.append(AudioSegment.from_file(root+'/'+f,format=dp[1].replace('.','')))

    elif os.path.isfile(paths):
        if os.path.splitext(path)[1] in audiolist:
            sounds.append(AudioSegment.from_file(root+'/'+f,format=dp[1].replace('.','')))

    else:
        sys.exit()

    mysilence = AudioSegment.silent(duration=sln*1000)
    if ntotal=='max':
        ntotal=len(sounds)
        
    if len(sounds)<=ntotal:
        if repeat==1:
            playlist=AudioSegment.empty() 
            for sound in sounds:
                playlist += sound
                playlist += mysilence
        elif repeat>1:
            for sound in sounds:
                playlist=AudioSegment.empty() 
                for _ in range(repeat):
                    playlist += sound
                    playlist += mysilence
        
        playlist.export('output_%s.wav'%str(int(time.time())),format='wav')
    elif len(sounds)>ntotal:
        msounds=[sounds[i:i+ntotal] for i in range(0,len(sounds),ntotal)]
        if repeat==1:
            playlist=AudioSegment.empty()
            for ss in msounds:
                for s in ss:
                    playlist += s
                    playlist += mysilence
            playlist.export('output_%s.wav'%str(int(time.time())),format='wav')  
        elif repeat>1:
            for ss in msounds:
                playlist=AudioSegment.empty() 
                for s in ss:
                    for _ in range(repeat):
                        playlist += s
                        playlist += mysilence
                playlist.export('output_%s.wav'%str(int(time.time())),format='wav')  
    else:
        print("Only one file,not to be combine the files")
    return
##########################################
def audios_to_one(paths,sln=3.5,repeat=1):
    """
    将文件夹下面的音频文件整合成一个文件，每个文件重复
    次数为repeat次
    paths:files to be combine together;paths or file.
    sln:产生一个持续时间为sln seconds的无声AudioSegment对象
    """
    sounds=[]
    if isinstance(paths,list):
        for path in paths:
            if os.path.isfile(path):
                dp=os.path.splitext(path)
                if dp[1] in audiolist:
                    sounds.append(AudioSegment.from_file(root+'/'+f,format=dp[1].replace('.','')))

    elif os.path.isdir(paths):
        for root,dirs,files in os.walk(paths):
            for f in files:
                dp=os.path.splitext(f)
                if dp[1] in audiolist:
                    print(f)
                    sounds.append(AudioSegment.from_file(root+'/'+f,format=dp[1].replace('.','')))

    elif os.path.isfile(paths):
        if os.path.splitext(path)[1] in audiolist:
            sounds.append(AudioSegment.from_file(root+'/'+f,format=dp[1].replace('.','')))

    else:
        sys.exit()

    if len(sounds)>1:
        mysilence = AudioSegment.silent(duration=sln*1000)
        playlist=AudioSegment.empty()
        if repeat==1:
            for sound in sounds:
                playlist += sound
                playlist += mysilence
        elif repeat>1:
            for sound in sounds:
                for _ in range(repeat):
                    #print(_)
                    playlist += sound
                    playlist += mysilence

    
        #mtype=os.path.splitext(output)
        
        playlist.export('output_%s.wav'%str(int(time.time())),format='wav')
    else:
        print("Only one file,not to be combine the files")
    return
#################################################
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
        if os.path.splitext(path)[1] in audiolist:
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
        
            
####################################################
def audio_split_combine(fpath,start='00:00:00',end='00:00:02',min_sl=300,sth=-40,duration=4):
    """
    先对语音进行分割，然后再将分割后语言按一定的时间间隔进行重新拼接，
    产生新的语音文件。
    fpath:语音文件
    start，end: 分别为从语音文件中提取的开始时间和截止时间，like 00:00:00
    sth:silence_thresh=-70 # 小于-70dBFS以下的为静默 
    min_sl:min_silence_len=700 # 静默超过700毫秒则拆分
    duration:持续无声的时间，单位为秒
    """
    if isinstance(fpath,str) and os.path.isfile(fpath):
        mf=os.path.splitext(fpath)
        if mf[1] in audiolist:
            Ag=AudioSegment.from_file(fpath,format=mf[1].replace('.',''))
    elif isinstance(fpath,pydub.audio_segment.AudioSegment):
        Ag=fpath
    else:
        sys.exit()

    if start=='':
        start=0
    else:
        st=start.split(':')
        if len(st)==3:
            start=(int(st[0])*3600+int(st[1])*60+int(st[2]))*1000
        elif len(st)==2:
            start=(int(st[0])*60+int(st[1]))*1000
        elif len(st)==1 and int(st[0])<60:
            start=int(st[0])*1000
        else:
            print("开始时间的格式错误，应为00：00：00样式")
            sys.exit()

    if end=='':
        end=len(Ag)
    else:
        ed=end.split(':')
        if len(ed)==3:
            end=(int(ed[0])*3600+int(ed[1])*60+int(ed[2]))*1000
        elif len(ed)==2:
            start=(int(ed[0])*60+int(ed[1]))*1000
        elif len(ed)==1 and int(ed[0])<60:
            start=int(ed[0])*1000
        else:
            print("结束时间的格式错误，应为00：00：00样式")
            sys.exit()
            
    audio=Ag[start:end]

    chunks=audio_split(audio,min_sl,sth)
    
    '间隔时间'
    ms = AudioSegment.silent(duration=duration*1000)
    pl=AudioSegment.empty()
    
    for sound in chunks:
        pl +=sound
        pl += ms
        #pl +=sound
        #pl += ms          
    pl.export('audio_split_%s.wav'%str(int(time.time())),format='wav')
          
    return
##################################################
def new_from_audio(fpath,start='00:00:00',end='00:00:20'):
    """
    fpath:is audio file or AudioSegment file.
    start:the start time like '00:00:00'
    end:  the end time like 00:00:10

    """
    if isinstance(fpath,str):
        if os.path.isfile(fpath):
            mf=os.path.splitext(fpath)
            if mf[1] in audiolist:
                Ag=AudioSegment.from_file(fpath,format=mf[1].replace('.',''))

    elif isinstance(fpath,pydub.audio_segment.AudioSegment):
        Ag=fpath
    else:
        sys.exit()

    if start=='':
        start=0

    else:
        st=start.split(':')
        if len(st)==3:
            start=(int(st[0])*3600+int(st[1])*60+int(st[2]))*1000
        elif len(st)==2:
            start=(int(st[0])*60+int(st[1]))*1000
        elif len(st)==1 and int(st[0])<60:
            start=int(st[0])*1000
        else:
            print("开始时间的格式错误，应为00：00：00样式")
            sys.exit()

    if end=='':
        end=len(Ag)
    else:
        ed=end.split(':')
        if len(ed)==3:
            end=(int(ed[0])*3600+int(ed[1])*60+int(ed[2]))*1000
        
        elif len(ed)==2:
            start=(int(ed[0])*60+int(ed[1]))*1000
        elif len(ed)==1 and int(ed[0])<60:
            start=int(ed[0])*1000
        else:
            print("结束时间的格式错误，应为00：00：00样式")
            sys.exit()
            
    audio=Ag[start:end]
    audio.export('audio_split_%s.wav'%str(int(time.time())),format='wav')
    return
#########################################
def _wav_pcm(ifile):
    """
    ifile:为输入的wav 文件。
    ofile:为输出的pcm文件
    """
    ofile=os.path.splitext(ifile)[0]+'.pcm'
    cmd='ffmpeg -y  -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s'%(ifile,ofile)
    os.system(cmd)
    return ofile
###################################
def _mp3_pcm(ifile):
    """
    ifile:为输入的wav 文件。
    ofile:为输出的pcm文件
    """
    ofile=os.path.splitext(ifile)[0]+'.pcm'
    cmd='ffmpeg -y  -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s'%(ifile,ofile) 
    os.system(cmd)
    #print(ofile)
    return ofile
####################################
def _wav_44kT16k(ifile):
    """
    ifile:为输入的wav 文件。
    ofile:为输出的pcm文件
    """
    ofile=os.path.splitext(ifile)[0]+'.pcm'
    cmd='ffmpeg -y  -f s16le -ac 1 -ar 44100 -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s'%(ifile,ofile) 
    os.system(cmd)    
    return ofile
#####################################
def audio2pcm(fpath):
    """
    将mp3、wav两种音频文件转化为pcm文件，为使用百度的语音识别做好准备
    """
    tm=os.path.splitext(fpath)[1].replace('.','')
    if tm=='wav':
        ofile=_wav_pcm(fpath)
        return ofile
    if tm == 'mp3':
        ofile=_mp3_pcm(fpath)
        return ofile
######################################################    
def audio2list(fpath,duration=59,pcm=False):
    """
    http://ai.baidu.com/docs#/ASR-Tool-convert/top
    fpath:is audio file or AudioSegment file.
    duration:分割语音的长度，单位为秒,默认是59s。
    cv:False表示不转为pcm文件，仅仅对文件分割为duration秒长的音频文件，
       否则，转为pcm
    """
    if isinstance(fpath,str):
        if os.path.isfile(fpath):
            paths=os.path.splitext(fpath)
            if paths[1] in audiolist:
                Ag=AudioSegment.from_file(fpath,format=paths[1].replace('.',''))
                path=paths[0]

    elif isinstance(fpath,pydub.audio_segment.AudioSegment):
        Ag=fpath
        path=os.getcwd()
    else:
        sys.exit()

    sounds=[Ag[i:i+duration*1000] for i in range(0,len(Ag),duration*1000)]

    #path=path[0]
    if not os.path.exists(path):
        os.mkdir(path)

    files=[]
    for i,sound in enumerate(sounds):
        tms=str(i).zfill(2)
        path1=path+'/audio_%s.wav'%tms
        sound.export(path1,format='wav')
        if pcm:
            ff=audio2pcm(path1)
            os.remove(path1)
            files.append(ff)
        else:
            files.append(path1)
    return files
##################################################
def chunks_n(sgm,duration=3,ntotal=40,repeat=2):
    """
    将一段音频先进行分割，然后再进行合并
    """    
    chunks=audio_split(sgm)
    s1=AudioSegment.silent(duration*1000)
    sounds=[chunks[i:i+ntotal] for i in range(0,len(chunks),ntotal)]
    
    for i,sound in enumerate(sounds):
        pls=AudioSegment.empty()
        for sd in sound:
            p=sd+s1
            pls +=pls*repeat
        pls.export("audio_split_%s.wav"%str(i).zfill(2))

    return
            
            
    
    
if __name__=="__main__":
    #audio_file_operation(paths=sys.argv[1])
    pass
