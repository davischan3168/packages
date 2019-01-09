#!/usr/bin/env python3
# -*-coding:utf-8-*-

import re
import os
import sys

def BD_text_split(fpath):
    if os.path.isfile(fpath):
        try:
            f=open(fpath,'r')
            tl=f.read()
        except:
            f=open(fpath,'r',encoding='gbk')
            tl=f.read()
    elif isinstance(fpath,str):
        tl=fpath

    else:
        sys.exit()
        
    text=re.sub('\n*','',tl)
    text=re.sub('-','',text)
    text_list = [text[i:i+500] for i in range(0, len(text), 500)]
    return text_list


def TS_text_split(fpath):
    if os.path.isfile(fpath):
        try:
            f=open(fpath,'r')
            tl=f.read()
        except:
            f=open(fpath,'r',encoding='gbk')
            tl=f.read()
    elif isinstance(fpath,str):
        tl=fpath

    else:
        sys.exit()    
        
    text=re.sub('\n*','',tl)
    text=re.sub('-','',text)
    text_list = [text[i:i+50] for i in range(0, len(text), 50)]
    return text_list

