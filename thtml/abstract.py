#!/usr/bin/env python3
# -*-coding:utf-8-*-

import re
from thtml.utilth import (GFlist,make_Mulu_content)
from thtml.txt2html import _hh
import shutil
import os

def getTt(path,rc=re.compile('(.*?案\s*（检例第\d*号）)'),p1=re.compile('【要旨】'),p2=re.compile('\【\w*】')):
    """
    
    """
    with open(path,encoding='utf8') as f:
        text=f.read()

    tt=rc.findall(text)
    #print(tt)
    ftxt=[]
    yzs=[]
    for i in tt:
        text=re.split(i,text)
        ftxt.append(text[0])

        try:
            text=text[1]
        except:
            pass
    #print(len(yzs))
    ftxt.append(text)
    fftxt=ftxt[1:]
    #print(len(fftxt))
    for ii in fftxt:
        try:
            yz=p1.split(ii)[1]
            yz=p2.split(yz)[0]
            #print(yz)
            yzs.append(yz)
        except:
            pass
        
    return list(zip(tt,fftxt,yzs))

def absSPP(path,tdir='itempdit',rc=re.compile('(.*?案\s*（检例第\d*号）)'),p1=re.compile('【要旨】'),p2=re.compile('\【\w*】'),yz=True):

    tt=re.compile('\s*')

    if not os.path.exists(tdir):
        os.mkdir(tdir)
        
    for root,dirs,files in os.walk(path):
        for f in files:
            if f.endswith('.txt'):
                pf=root+'/'+f
                df=getTt(pf)
                for i in df:
                    #print(i)
                    ttl=tt.sub('',i[0])
                    with open(tdir+'/%s.txt'%ttl,'w',encoding='utf8') as fl:
                        #fl.write('【要旨】:\n\n')
                        if yz:
                            fl.write(i[2])
                        else:
                            fl.write(i[1])

    return

def absAPPhtml(path,outdir='',regrex1=re.compile('检例第(\d*)号'),rc=re.compile('(.*?案\s*（检例第\d*号）)'),p1=re.compile('【要旨】'),p2=re.compile('\【\w*】'),yz=True):                           
    if outdir=='':
        outdir='itempdit'
    absSPP(path=path,tdir=outdir,rc=rc,p1=p1,p2=p2,yz=yz)
    ss=GFlist(outdir,regrex1=regrex1)
    Tfile=[i[1] for i in ss]
    htmlcode=_hh(outdir)
    tb,ctt=make_Mulu_content(Tfile)
    htmlName='outputabsSPP.html'
    try:
        html=open(htmlName,'w',encoding='utf8')
        html.write(htmlcode)
        html.write(tb)
        html.write(ctt)
    except:
        html=open(htmlName,'w',encoding='gbk')
        html.write(htmlcode)
        html.write(tb)
        html.write(ctt)

    html.write('</body></html>')
    html.close()
    shutil.rmtree(outdir)    
    return
            


    return 
def abstract(path,rc=re.compile('裁判要点\W*(.*?\s*.*?)\W*相关法条')):
    with open(path,encoding='utf8') as f:
        text=f.read()

    if rc is not None:
        cmmt='裁判要点:\n\n'+''.join(rc.findall(text))+'\n\n'
    else:
        cmmt=text
    return cmmt

def abssplit(path,p1=re.compile('裁判要点'),p2=re.compile('相关法条')):
    with open(path,encoding='utf8') as f:
        text=f.read()

    cc=p1.split(text)
    if len(cc)==2:
        c1=p2.split(cc[1])
        if len(c1)==2:
            return c1[0]
        else:
            print('No content for p2')
            return
    else:
        print('No content for p1')
        return
    
def absfile(path,func=abssplit,p1=re.compile('裁判要点'),p2=re.compile('相关法条'),rc=re.compile('裁判要点\W*(.*?\s*.*?)\W*相关法条')):
    with open(path,encoding='utf8') as f:
        text=f.read()

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
    tdir='temp_dir'
    if not os.path.exists(tdir):
        os.mkdir(tdir)
        
    Tfile=[]
    if func.__name__=='abstract':
        for f in files:
            bn=os.path.basename(f)
            nf=os.path.join(tdir,bn)
            text=func(f,rc=rc)
            try:
                with open(nf,'w',encoding='utf8') as gf:
                    gf.write(text)
                Tfile.append(nf)
            except:
                pass
    elif func.__name__=='abssplit':
        for f in files:
            bn=os.path.basename(f)
            nf=os.path.join(tdir,bn)
            text=func(f,p1=p1,p2=p2)
            #print(text)
            try:
                with open(nf,'w',encoding='utf8') as gf:
                    gf.write(text)
                Tfile.append(nf)
            except:
                pass 
    return Tfile
    

def absTFilehtml(txtpath,func=abssplit,rc=re.compile('裁判要点\W*(.*?\s*.*?)\W*相关法条'),p1=re.compile('裁判要点'),p2=re.compile('相关法条'),regrex1=None,Research=None,index=True,Startw=None,m1=re.compile(r'^第\w{1,3}[编|篇]'),m2=re.compile(r'^第\w{1,3}章'),m3=re.compile(r'^第\w{1,3}节')):
    """
    rc:需要提取的主要内容
    regrex1:
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
    tdir='temp_dir'
    if not os.path.exists(tdir):
        os.mkdir(tdir)
        
    htmlcode=_hh(txtpath)
    Tfile=[]
    if func.__name__=='abstract':
        for f in files:
            bn=os.path.basename(f)
            nf=os.path.join(tdir,bn)
            text=func(f,rc=rc)
            try:
                with open(nf,'w',encoding='utf8') as gf:
                    gf.write(text)
                Tfile.append(nf)
            except:
                pass
    elif func.__name__=='abssplit':
        for f in files:
            bn=os.path.basename(f)
            nf=os.path.join(tdir,bn)
            text=func(f,p1=p1,p2=p2)
            #print(text)
            try:
                with open(nf,'w',encoding='utf8') as gf:
                    gf.write(text)
                Tfile.append(nf)
            except:
                pass
                

    tb,ctt=make_Mulu_content(Tfile,m1=m1,m2=m2,m3=m3,index=index)
    htmlName='outputabs.html'
    try:
        html=open(htmlName,'w',encoding='utf8')
        html.write(htmlcode)
        html.write(tb)
        html.write(ctt)
    except:
        html=open(htmlName,'w',encoding='gbk')
        html.write(htmlcode)
        html.write(tb)
        html.write(ctt)

    html.write('</body></html>')
    html.close()
    shutil.rmtree(tdir)

    return

if __name__=="__main__":
    pass
