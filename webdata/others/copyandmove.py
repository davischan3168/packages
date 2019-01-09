#!/usr/bin/env python3
# -*-coding:utf-8-*-

import os,sys,shutil

def copyfiles(srcpath,dstpath,mtype=['.mp4']):
    if not os.path.exists(dstpath):
        os.mkdir(dstpath)
    #allfiles=[]
    for root,dirs,files in os.walk(srcpath):
        for k,f in enumerate(files):
            if os.path.splitext(f)[1] in mtype:
                du=os.path.join(root,f)
                print(du)
                dstdu=os.path.join(dstpath,f)
                print(dstdu)
                shutil.copyfile(du,dstdu)
                print("copy %s ---> %s" %(du,dstdu))

    return

def movefile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%srcfile)
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.move(srcfile,dstfile)          #移动文件
        print ("move %s -> %s"%( srcfile,dstfile))
    return

def copyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%srcfile)
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        print ("copy %s -> %s"%( srcfile,dstfile))
    return

if __name__=="__main__":
    copyfiles(sys.argv[1],sys.argv[2])
