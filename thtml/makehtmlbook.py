#!/usr/bin/env python3
# -*-coding:utf-8-*-

import os
import sys
import re
from util.ch2num import ChNumToArab
import thtml as th
def getfilelist(path,regrex1=re.compile('\d{1,3}')):
    """
    regrex1:为re.compile 的类型    
    """
    ss={}
    for root,ds,fs in os.walk(path):
        for f in fs:
            print(f)
            if isinstance(regrex1,re.Pattern):
                print('ok....1')
                if os.path.splitext(f)[1] in ['.txt']:
                    
                    if len(re.findall(regrex1,f))>0:
                        num=int((regrex1.findall(f)[0]))
                        ss[num]=os.path.abspath(os.path.join(root,f))
                    elif len([i for i in regrex1.findall(ChNumToArab(f)) if len(i)>0])>0:
                        num= int(regrex1.findall(ChNumToArab(f))[0])
                        ss[num]=os.path.abspath(root+'/'+f)
                    
                    dd=sorted(ss.items(),key=lambda item:item[0])
            else:
                print('ok ......2')
                ss[f]=os.path.abspath(root+'/'+f)
                dd=sorted(ss.items(),key=lambda item:item[0])

    return dd
    
def MyHtmlSplit(path,output='',regrex1=re.compile('\d{1,3}'),func=th.txt2htmlv1,span=48,split=True,index=False,revs=True):
    """
    path:文件夹的名称
    output:输出文件的名称
    regrex1:正则表达式，按其进行排序
    func:th.C2html,th.txt2htmlv1 合并成一个文件
    span:在分割的情况下，每个文件所包含的文章数量
    split=True，是否分割
    revs：按倒叙排列
    index：第三次目录是否需要。
    """
    dd=getfilelist(path,regrex1)
    df=[]
    
    
    for i in dd:
        df.append(i[1])

    if revs:
        df.sort(reverse=revs)
    

    if output=='':
        output='myhtml'
    if len(df)>span:
        dff=[df[i:i+span] for i in range(0,len(df),span)]
        if split:
            out=output+'%s.html'
            for i,df in enumerate(dff):
                if os.path.exists(out%str(i).zfill(2)):
                    os.remove(out%str(i).zfill(2))                
                func(df,index=index)
                if func.__name__=="txt2htmlv1":
                    os.rename('outputtxt.html',out%str(i).zfill(2))
                else:
                    os.rename('output.html',out%str(i).zfill(2))
        else:
            out=output+'.html'
            if os.path.eixsts(out):
                os.remove(out)
            func(df,index=index)
            if os.path.exists(out%str(i)):
                os.remove(out%str(i))             
            if func.__name__=="txt2htmlv1":
                os.rename('outputtxt.html',out)
            else:
                os.rename('output.html',out)
    else:
        func(df,index=index)
        out=output+'.html'
        if os.path.exists(out):
            os.remove(out)
        if func.__name__=="txt2htmlv1":
            os.rename('outputtxt.html',out)
        else:
            os.rename('output.html',out)            

    return 
if __name__=="__main__":
    #DXtohtml(sys.argv[1])
    #ddd=getfilelist(sys.argv[1],regrex1=None)
    #MyHtmlSplit(sys.argv[1],'最高法指导性案例',func=wd.txt2htmlv1,span=48,split=True,index=False,revs=False)
    MyHtmlSplit(sys.argv[1],'最高法指导性案例',regrex1=None,func=th.C2html,span=48,split=False,index=False,revs=False)
    pass
