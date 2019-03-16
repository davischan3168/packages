#!/usr/bin/env python3
# -*-coding:utf-8-*-
import os
import sys
import re

def Gongbao(path):
    """
    将最高院提供的公报案例的ocr文本文件进行编辑
    一满足段落的要求
    """
    if os.path.splitext(path)[1] == '.txt':
        path=os.path.abspath(path)
        op=os.path.splitext(path)[0]+'_new.txt'
        #print(op)
    else:
        print('Something is wrong....')
        sys.exit()
    
    f=open(path,'r',encoding='utf8')
    text=f.readlines()
    f.close()
    cnts=''
    for i in text:
        if re.search('^\w例索引:',i):
            cnts +='\n\n'+i
        elif re.search('^裁判\w{2}:',i):
            cnts +='\n\n'+i.strip()
        elif re.search('^本期关键词:',i):
            cnts +='\n\n'+i.strip()
        elif re.search("^\w例\d*争点:",i):
            print(i)
            cnts +='\n\n'+i.strip()            
        elif re.search('。\n$',i):
            cnts +=i
        elif re.search('\?\n$',i):
            cnts +=i
        else:
            cnts +=i.rstrip()


    f=open(op,'w',encoding='utf8')
    f.write(cnts)
    #print(cnts)
    f.close()
    return cnts

def Gongbaov1(path):
    """
    将最高院提供的公报案例的ocr文本文件进行编辑
    一满足段落的要求
    """
    if os.path.splitext(path)[1] == '.txt':
        path=os.path.abspath(path)
        op=os.path.splitext(path)[0]+'_new.txt'
    else:
        print('Something is wrong....')
        sys.exit()
    
    f=open(path,'r',encoding='utf8')
    text=f.readlines()
    f.close()
    cnts=''
    for i in text:
        if re.search('^\w例索引:',i):
            cnts +='\n\n'+i
        elif re.search('^\w{4,5}:',i):
            cnts +='\n\n'+i.strip()
        elif re.search("^\w例\d*争点:",i):
            print(i)
            cnts +='\n\n'+i.strip()            
        elif re.search('。\n$',i):
            cnts +=i
        elif re.search('\?\n$',i):
            cnts +=i
        else:
            cnts +=i.rstrip()
    with open(op,'w',encoding='utf8') as f:
        f.write(cnts)
    return cnts

def Luoji(path):
    """
    将最高院提供的公报案例的ocr文本文件进行编辑
    一满足段落的要求
    """
    if os.path.splitext(path)[1] == '.txt':
        path=os.path.abspath(path)
        op=os.path.splitext(path)[0]+'_new.txt'
    else:
        print('Something is wrong....')
        sys.exit()
    
    f=open(path,'r',encoding='utf8')
    text=f.readlines()
    f.close()
    cnts=''
    for i in text:
        if re.search('^第\w*章',i):
            cnts +='\n\n'+i+'\n'
        elif re.search('^第\w*节',i):
            cnts +='\n\n'+i+'\n'
        elif re.search('^\(\d*\)',i):
            cnts +='\n\n'+i            
        elif re.search('。\n$',i):
            cnts +=i
        elif re.search('\?\n$',i):
            cnts +=i
        elif re.search('[;|；|\)]\n$',i):
            cnts +=i
        elif re.search('-\d*-',i):
            pass
        else:
            cnts +=i.rstrip()
    with open(op,'w',encoding='utf8') as f:
        f.write(cnts)
    return cnts

def XingF(path):
    """
    将最高院提供的公报案例的ocr文本文件进行编辑
    一满足段落的要求
    """
    if os.path.splitext(path)[1] == '.txt':
        path=os.path.abspath(path)
        op=os.path.splitext(path)[0]+'_new.txt'
    else:
        print('Something is wrong....')
        sys.exit()
    
    f=open(path,'r',encoding='utf8')
    text=f.readlines()
    f.close()
    cnts=''
    for i in text:
        if re.search('^第\w*章',i):
            cnts +='\n\n'+i+'\n'
        elif re.search('^第\w*节',i):
            cnts +='\n\n'+i+'\n'
        elif re.search('^法条必读',i):
            cnts +='\n\n'+i+'\n'
        elif re.search('^复习提要',i):
            cnts +='\n\n'+i+'\n'            
        #elif re.search('^\(\w*\)',i):
        #    cnts +='\n\n'+i
        elif re.search('^第\w{1,}条',i):
            cnts +='\n\n'+i            
        elif re.search('^\w{1,}、',i):
            cnts +='\n\n'+i             
        elif re.search('。\n$',i):
            cnts +=i
        elif re.search('\?\n$',i):
            cnts +=i
        elif re.search('[;|；|\)]\n$',i):
            cnts +=i
        elif re.search('-\d*-',i):
            pass
        else:
            cnts +=i.rstrip()
    with open(op,'w',encoding='utf8') as f:
        f.write(cnts)
    return# cnts

def txtcombine(path1,start,end):
    f=open('new.txt','w',encoding='utf8')
    #path1='2019年瑞达法考精讲班刑法-刘凤科讲义_页面_{}.txt'
    for i in range(start,end,1):
        #path=path%str(i).zfill(3)
        print(i)
        path=path1.format(str(i).zfill(3))
        print(path)
        try:
            with open(path,encoding='utf8') as ff:
                dd=ff.readlines()
                f.write(''.join(dd))
                #f.write(ff.read())
        except Exception as e:
            print(e)
    f.close()
    return

def Gongbaodir(pathdir):
    for root,ds,files in os.walk(pathdir):
        for f in files:
            path=os.path.join(root,f)
            try:
                Gongbao(path)
            except:
                pass

    return
    
if __name__=="__main__":
    #ct=Gongbao(sys.argv[1])
    pass
