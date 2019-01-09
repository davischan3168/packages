#!/usr/bin/env python3
# -*-coding:utf-8-*-
import sys

def tonum(f,befor='第',after='批指导性案例.txt'):
    """
    留下汉字序号,
    
    """
    num=f.replace(befor,'').replace(after,'')
    if num == '一':
        numI = 1
    elif num == '二': 
        numI =2
    elif num == '三':
        numI=3
    elif num == '四':
        numI=4
    elif num == '五':
        numI=5        
    elif num == '六':
        numI=6
    elif num == '七':
        numI=7
    elif num == '八':
        numI=8
    elif num == '九':
        numI=9
    elif num == '十':
        numI=10
    elif num == '十一':
        numI=11
    elif num == '十二':
        numI=12
    elif num == '十三':
        numI=13
    elif num == '十四':
        numI=14
    elif num == '十五':
        numI=15        
    elif num == '十六':
        numI=16
    elif num == '十七':
        numI=17
    elif num == '十八':
        numI=18
    elif num == '十九':
        numI=19
    elif num == '二十':
        numI=20
    elif num == '二十一':
        numI=21
    else:
        sys.exit()
    return numI

if __name__=="__main__":
    tonum(sys.argv[1])
