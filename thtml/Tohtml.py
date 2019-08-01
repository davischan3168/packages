#!/usr/bin/env python3
# -*-coding:utf-8-*-

import sys,os,time
import re
from thtml.cfg import title,endd,title1,title2
from thtml.utilth import (GFlist,make_Mulu_content)
from util.ch2num import ChNumToArab
from urllib.request import pathname2url
#from mswdoc.docx2txt import msdoc2text

pp='<p style="word-spacing:10px;line-height:1.5">&emsp;&emsp;%s</p>\n'

def getfilelist(path,regrex1=None,Research=None):
    """
    regrex1:为re.compile 的类型    
    """
    ss={}
    for root,ds,fs in os.walk(path):
        for f in fs:
            #print(f)
            if regrex1 is not None:
                #print('ok....1')
                if os.path.splitext(f)[1].lower() in ['.txt','.doc','.docx']:
                    
                    if len(re.findall(regrex1,f))>0:
                        num=int((regrex1.findall(f)[0]))
                        ss[num]=os.path.abspath(os.path.join(root,f))
                    elif len([i for i in regrex1.findall(ChNumToArab(f)) if len(i)>0])>0:
                        num= int(regrex1.findall(ChNumToArab(f))[0])
                        ss[num]=os.path.abspath(root+'/'+f)
                    
                    dd=sorted(ss.items(),key=lambda item:item[0])
            else:
                #print('ok ......2')
                
                ss[f]=os.path.abspath(root+'/'+f)
                dd=sorted(ss.items(),key=lambda item:item[0])
    if (regrex1 is None) and (Research is not None):
        d=[i[1] for i[0] in dd if Research in i[0]]
        dd=d

    return dd

def C2html(txtpath,output='output.html',m1=re.compile(r'^第\w{1,3}[编|篇]'),m2=re.compile(r'^第\w{1,3}章'),m3=re.compile(r'^第\w{1,3}节'),m4=re.compile(r'^\w{1,3}、'),index=True):
    """
    txtpath:为单独的文件、一系列文件或一段字符
    并将这些文件中的内容输出到一份html 文件中
    """
    p=getcsspath()
    ft='''\n<link rel="stylesheet" type="text/css" href="%s" />'''
    ll=title+'\n'+title1+ft%p+title2+'\n'
    #print(ll)
    
    files=[]

    if isinstance(txtpath,list):
        for f in txtpath:
            if os.path.isfile(f) and (os.path.splitext(f)[1].lower() in ['.txt','.doc','.docx']):
                files.append(f)    
    elif os.path.isfile(txtpath):
        if os.path.splitext(txtpath)[1].lower() in ['.txt','.doc','.docx']:
            files.append(txtpath)

                
    elif isinstance(txtpath,str):
        path123='tempsdfsf.txt'
        fff=open(path123,'w',encoding='utf8')
        fff.write(txtpath)
        fff.close()
        files.append(path123)
                
    else:
        sys.exit()
        


    if os.path.exists(output):
       os.remove(output)

    
    tb,ctt=make_Mulu_content(files,m1=m1,m2=m2,m3=m3,index=index)
    try:
        html=open(output,'a',encoding='utf8')
        html.write(ll)
        #html.write('<div id="content">\n')
        html.write('<div id="content",style="background-color:#C7EDF0">\n')
        html.write(tb)
        html.write(ctt)
    except:
        html=open(output,'a',encoding='gbk')
        html.write(ll)
        #html.write('<div id="content">\n')
        html.write('<div id="content",style="background-color:#C7EDF0">\n')
        html.write(tb)
        html.write(ctt)

        

    html.write(endd)
    html.close()
    print("\n转换成功,保存在%s"%output)
    try:
        if os.path.exists(path123):
            os.remove(path123)
    except:
        pass
    return
######################################
def getcsspath():
    if sys.platform.startswith('win'):
        if os.getcwd() in ['J:\\python']:
            p='packages/thtml/css/worg.css'
        else:
            p=os.path.abspath('J:/python/packages/thtml/css/worg.css')
    elif sys.platform in ['linux']:
        if os.getcwd() in ['/media/chen/Davis/python']:
            p='packages/thtml/css/worg.css'
        else:
            p=os.path.abspath('/media/chen/Davis/python/packages/thtml/css/worg.css')
    return pathname2url(p)
################################################
def C2htmlBase(txtpath,m1=re.compile(r'^第\w{1,3}[编|篇]'),m2=re.compile(r'^第\w{1,3}章'),m3=re.compile(r'^第\w{1,3}节'),m4=re.compile(r'^\w{1,3}、'),index=True):
    """
    txtpath:为单独的文件或一段字符
    
    """
    p=getcsspath()
    ft='''\n<link rel="stylesheet" type="text/css" href="%s" />'''
    ll=title+'\n'+title1+ft%p+title2+'\n'
    #print(ll)
    
    files=[]
    if os.path.isfile(txtpath):
        if os.path.splitext(txtpath)[1].lower() in ['.txt','.doc','.docx']:
            files.append(txtpath)
            #tname=os.path.splitext(os.path.basename(txtpath))[0]
                
    elif isinstance(txtpath,str):
        path123='tempsdfsf.txt'
        fff=open(path123,'w',encoding='utf8')
        fff.write(txtpath)
        fff.close()
        files.append(path123)
                
    else:
        sys.exit()
        

    tb,ctt=make_Mulu_content(files,m1=m1,m2=m2,m3=m3,index=index)
    if os.path.exists(output):
       os.remove(output)

    try:
        if os.path.exists(path123):
            os.remove(path123)
    except:
        pass
    
    try:        
        html=open(output,'a',encoding='utf8')
        html.write(ll)
        #html.write('<div id="content">\n')
        html.write('<div id="content",style="background-color:#C7EDF0">\n')
        html.write(tb)
        html.write(ctt)
    except:
        html=open(output,'a',encoding='gbk')
        html.write(ll)
        #html.write('<div id="content">\n')
        html.write('<div id="content",style="background-color:#C7EDF0">\n')
        html.write(tb)
        html.write(ctt)
    html.write(endd)
    html.close()
    print("\n转换成功,保存在%s"%output)
    return
##########################################################
def C2html_AllinOnev1(txtpath=None,output='output.html',regrex1=re.compile('\d{1,3}'),span=48,split=False,index=False,revs=True):
    """
    将目录txtpath下的txt文件内容全部转到output.html文件中
    px:文中排序的基准。
    """
    files=[]
    if isinstance(txtpath,list):
        files.extend(txtpath)
    elif txtpath is None:
        txtpath=os.getcwd()
        ss=getfilelist(txtpath,regrex1)
        files=[i[1] for i in ss]
    elif os.path.isdir(txtpath):
        ss=getfilelist(txtpath,regrex1)
        files=[i[1] for i in ss]

    if output=='':
        output='myhtml'
    if revs:
        files.sort(reverse=revs)
    if len(files)>span:
        dff=[files[i:i+span] for i in range(0,len(files),span)]
        if split:
            out=output+'%s.html'
            for i,df in enumerate(dff):
                if os.path.exists(out%str(i)):
                    os.remove(out%str(i))                
                C2html(df,index=index)
                os.rename('output.html',out%str(i))
        else:
            out=output+'.html'
            C2html(files,index=index)
            if os.path.exists(out):
                os.remove(out)            
            os.rename('output.html',out)
    else:
        C2html(files,index=index)
        out=output+'.html'
        if os.path.exists(out):
            os.remove(out)         
        os.rename('output.html',out)
    return
####################################################
def C2html_AllinOne(txtpath=None,regrex1=re.compile('\d{1,3}'),index=True):
    """
    将目录txtpath下的txt文件内容全部转到output.html文件中
    px:文中排序的基准。
    """
    files=[]
    if isinstance(txtpath,list):
        files.extend(txtpath)
    elif txtpath is None:
        txtpath=os.getcwd()
        ss=getfilelist(txtpath,regrex1)
        files=[i[1] for i in ss]
    elif os.path.isdir(txtpath):
        ss=getfilelist(txtpath,regrex1)
        files=[i[1] for i in ss]

    C2html(files,index=index)
    return
####################################################
def C2html_AllinOneGF(txtpath=None,regrex1=None,Research=None,index=True,Startw=None):
    """
    将目录txtpath下的txt文件内容全部转到output.html文件中
    px:文中排序的基准。
    """
    files=[]
    if isinstance(txtpath,list):
        files.extend(txtpath)
    elif txtpath is None:
        txtpath=os.getcwd()
        ss=GFlist(txtpath,regrex1=regrex1,research=Research,startw=Startw)
        files=[i[1] for i in ss]
    elif os.path.isdir(txtpath):
        ss=GFlist(txtpath,regrex1=regrex1,research=Research,startw=Startw)
        files=[i[1] for i in ss]

    C2html(files,index=index)
    return
######################################################
def C2html_OnebyOne(txtpath,index=True):
    """
    将目录txtpath下的txt文件内容逐一转到相应的html文件中
    """
    files=[]
    if txtpath is None:
        txtpath=os.getcwd()
            
    elif not os.path.isdir(txtpath):
        raise("txtpath is not dir")

    txtpath='/'.join([i for i in txtpath.split('/') if len(i)>0])
    for root,ds,fs in os.walk(txtpath):
        for f in fs:
            #print(f,txtpath)
            if os.path.splitext(f)[1] in ['.txt']:
                #print(root+'/'+f)
                C2htmlBase(txtpath=root+'/'+f,index=index)
    return

    
if __name__=="__main__":
    #C2html_AllinOne(sys.argv[1],regrex1=None)
    pass
            
