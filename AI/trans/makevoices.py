#!/usr/bin/env python3
# -*-coding:utf-8-*-
from AI.trans import download_audio
from AI.util.audiopy import audios_to_one
import os
import sys

def makevoice_English(text):
    if os.path.isfile(text):
        if os.path.splitext(1)=='.txt':
            with open(text,'r',encoding='utf8') as f:
                contents=f.readlines()
        for lines in contents:
            words=lines.split(',')
            download_audio(words)
        audios_to_one('audio',repeat=2)

    elif isinstance(text,str):
        contents=text.split(',')
        download_audio(contents)
        audios_to_one('audio',repeat=2)        

    else:
        sys.exit()


    return



if __name__ == '__main__':
    pass
