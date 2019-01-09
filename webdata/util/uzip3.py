#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# uzip.py
"""
解决在linux下解压的乱码问题
""" 
import os
import sys
import zipfile
#import codecs

def uzipall(fpath):
    """
    解压缩zip类型的文件,可以自动识别是在py2或py3的环境
    """
 
    print("Processing File %s" %fpath)
    file=zipfile.ZipFile(fpath,"r")

    for name in file.namelist():
        if sys.version[0] == '2':
            uname=name.decode('gbk')
        elif sys.version[0] == '3':
            uname=name.encode('cp437')
            uname=uname.decode('gbk')
            
        print("Extracting %s"  %uname)
        pathname = os.path.dirname(uname)
        if not os.path.exists(pathname) and pathname!= "":
            os.makedirs(pathname)
            
        data = file.read(name)
        if not os.path.exists(uname):
            try:
                fo = open(uname, "w")
                fo.write(data)
            except:
                fo = open(uname, "wb")
                fo.write(data)
            fo.close
            
    file.close()
    return

if __name__=="__main__":
    f=sys.argv[1]
    uzipall(f)
