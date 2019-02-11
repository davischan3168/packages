#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# uzip.py
"""
解决在linux下解压的乱码问题
""" 
import os
import sys
import zipfile
from unrar import rarfile
import tarfile  
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

def _rewrite(fpath):
    """
    解压缩的根目录
    """
    ad=[]
    for rs,ds,fs in os.walk(fpath):
        for f in fs:
            ad.append(rs+'/'+f)
    for i in ad:
        try:
            ii=i.encode('cp437')
            ii=ii.decode('gbk')
            print('decode %s \n to %s ....\n\n'%(i,ii))
            pathname = os.path.dirname(ii)
            if not os.path.exists(pathname) and pathname!= "":
                os.makedirs(pathname)                    
            if not os.path.exists(ii):
                fo = open(ii, "wb")
                fo.write(open(i,'rb').read())
                fo.close
                
            os.remove(i)
            print("Remove file %s completed..."%i)
        except Exception as e:
            print(e)
            pass
    return

def _renamefile(dirname):
    """
    将dirname目录下文件的名称
    """
    #dirs=os.listdir(dirname)
    for root,dirs,fs in os.walk(dirname):

        for f in fs:
            try:
                newf=f.encode('cp437')
                newf=newf.decode('gbk')
                print("convert oldfile: %s to newfile: %s "%(f,newf))
                old=os.path.join(root,f)
                newf=os.path.join(root,newf)
                os.rename(old,newf)
            except Exception as e:
                #print(e)
                pass        

    return

def _renamedir(dirname):
    listdir=[]
    for root,dirs,fs in os.walk(dirname):
        for d in dirs:
            old=os.path.join(root,d)
            listdir.append(old)
    

    listdir.reverse()
    for i in listdir:
        try:
            dr=os.path.split(i)
            new=dr[-1].encode('cp437').decode('gbk')
            newdir=os.path.join(dr[0],new)
            os.rename(i,newdir)
            print(newdir)
        except Exception as e:
            pass
    
    return

    
def decompress(mfile,dpr=True,*GSfs):
    """
    mfile:压缩文件，待解压的文件。
    GSfs：是需要解压出来的文件。
    Return：
          压缩文件中所包含的文件列表。
    """
    if isinstance(GSfs,str):
        lis=[]
        lis.append(GSfs)
        GSfs=lis
        print(GSfs)
        del lis

    mfile=os.path.abspath(mfile)
    if os.path.splitext(mfile)[1].lower()=='.rar':
        rf=rarfile.RarFile(mfile,'r')
        listf=rf.namelist()
        namelist=[rf.filename+'//'+i for i in listf]
        if len(GSfs)>0:
            if not os.path.exists('extract'):
                os.mkdir('extract')
            for i in GSfs:
                if i in listf:
                    rf.extract(i,'extract/')
                else:
                    print('File %s is not in the Compress File'%i)
        #rf.close()
        elif dpr:
            if not os.path.exists('extract'):
                os.mkdir('extract')
            for i in listf:
                rf.extract(i,'extract')
                #pass
     
        return namelist
    ####################################################
    elif os.path.splitext(mfile)[1].lower()=='.zip':
        rf=zipfile.ZipFile(mfile,'r')
        listff= rf.namelist()
        listf=[]
        for i in listff:
            if sys.version[0] == '2':
                ii=i.decode('gbk')
                listf.append(i)
            elif sys.version[0] == '3':
                ii=i.encode('cp437')
                ii=ii.decode('gbk')#gb2312\gb1803
                listf.append(ii)
        
        if len(GSfs)>0:
            if not os.path.exists('extract'):
                os.mkdir('extract')
            for i in GSfs:
                if i in listff:
                    rf.extract(i,'extract')
                    _renamefile('extract')
                    _renamedir('extract')

        elif dpr:
            if not os.path.exists('extract'):
                os.mkdir('extract')
            for i in listff:
                rf.extract(i,'extract')
        rf.close()
        
        if os.path.exists('extract'):
            #_rewrite('extract')
            _renamefile('extract')
            _renamedir('extract')
            pass
        namelist=[rf.filename+'//'+i for i in listf]
        return namelist
    #############################################################
    elif os.path.splitext(mfile)[1].lower() in ['.tar','.gz']:
        rf=tarfile.open(mfile,'r')
        listf=rf.getnames()
        namelist=[rf.name+'//'+i for i in listf]
        if len(GSfs)>0:
            if not os.path.exists('extract'):
                os.mkdir('extract')
            for i in GSfs:
                if i in listf:
                    rf.extract(i,'extract')
        elif dpr:
            if not os.path.exists('extract'):
                os.mkdir('extract')
            for i in listf:
               rf.extract(i,'extract')                     
        rf.close()        
        return namelist        
    else:
        return False

if __name__=="__main__":
    #f=sys.argv[1]
    #d=decompress(f,dpr=False)
    pass
