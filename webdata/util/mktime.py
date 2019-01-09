#!/usr/bin/env python3
# -*-coding:utf-8-*-

import time
import datetime
import sys

def str2timestamp(a):
    """
    a must like %Y-%m-%d %H:%M:%S or %Y-%m-%d
    """
    try:
        timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
        return int(time.mktime(timeArray))
    except:
        timeArray = time.strptime(a, "%Y-%m-%d")
        return int(time.mktime(timeArray))
def str2timestamp_dt(a):
    """
    a must like %Y-%m-%d %H:%M:%S or %Y-%m-%d
    """    
    try:
        dateArray=datetime.datetime.strptime(a,'%Y-%m-%d').timetuple()
    except:
        dateArray=datetime.datetime.strptime(a,'%Y-%m-%d %H:%M:%S').timetuple()
    return int(time.mktime(dateArray))

    
def timestamp2str(timeStamp,mtype='L'):
    """
    timeStamp: must be 10 int
    mtype: L,输出格式为%Y-%m-%d %H:%M:%S
           其他,输出格式为%Y-%m-%d
    """
    if not isinstance(timeStamp,int):
        timeStamp=int(timeStamp)
    if len(str(timeStamp))!=10:
        i=len(str(timeStamp))-10
        timeStamp=int(timeStamp/(10**i))
    timeArray = time.localtime(timeStamp)
    if mtype=='L':
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    else:
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime
    
    
def timestamp2str_dt(timeStamp,mtype='L'):
    """
    timeStamp: must be 10 int
    mtype: L,输出格式为%Y-%m-%d %H:%M:%S
           其他,输出格式为%Y-%m-%d
    """
    if not isinstance(timeStamp,int):
        timeStamp=int(timeStamp)    
    if len(str(timeStamp))!=10:
        i=len(str(timeStamp))-10
        timeStamp=int(timeStamp/(10**i))
    timeArray = datetime.datetime.utcfromtimestamp(timeStamp)
    if mtype=='L':
        otherStyleTime = timeArray.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    else:
        otherStyleTime = timeArray.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime

def now2str(mtype='L'):
    now=int(time.time())
    timeArray = time.localtime(timeStamp)
    if mtype=='L':
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    else:
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime

def now2str_dt(mtype='L'):
    now=datetime.datetime.now()
    if mtype=='L':
        otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
    else:
        otherStyleTime = now.strftime("%Y-%m-%d")
    return otherStyleTime

    
if __name__=="__main__":
    timestamp2str(sys.argv[1])
