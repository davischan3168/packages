#!/usr/bin/env python3
# -*-coding:utf-8-*-

import sys,os,time
import MySQLdb
#import webdata as wd

conn = MySQLdb.connect(host="localhost", port=3306, user='root', passwd='801019', db='SDD', charset="utf8")
cur = conn.cursor()

title=r"""
\documentclass[myxecjk,msize]{gdhsarticle}%{kindle}
\iffalse
\geometry{paperheight=297mm,%
paperwidth=210mm,
left=2.3cm,%
right=2.3cm,%
top=2.1cm,%
bottom=2.1cm,%
headheight=0cm,%
headsep=0cm,
footskip=0cm
}%
\fi
\linespacing{1.52}%
\pagestyle{empty}
\usepackage{xpinyin}
\setmainfont{CMU Serif}
\setCJKmainfont{SimSun}
%\include{setting}
%\include{pagesign}
\setlength{\unitlength}{1cm}
\parindent=2em
\definecolor{defaultbgcolor-0}{RGB}{199,237,204}%for eye
\pagecolor{defaultbgcolor-0}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%以下正文%%%%%%%%%%%%
\begin{document}
"""

kindle=r"""
\documentclass[myxecjk,msize]{gdhsarticle}%{kindle}
\geometry{paperwidth=9.2cm,% 
paperheight=12.4cm, width=9cm, 
height=12cm,top=0.2cm,bottom=0.4cm,
left=0.2cm,right=0.2cm,foot=0cm, nohead,nofoot}%
\linespacing{1.52}%
\pagestyle{empty}
\usepackage{xpinyin}
\setmainfont{CMU Serif}
\setCJKmainfont{SimSun}
%\include{setting}
%\include{pagesign}
\setlength{\unitlength}{1cm}
\parindent=2em
\definecolor{defaultbgcolor-0}{RGB}{199,237,204}%for eye
%\pagecolor{defaultbgcolor-0}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%以下正文%%%%%%%%%%%%
\begin{document}
\setlength{\parindent}{0em}
%\begin{pinyinscope}
"""

end=r"""
%\end{pinyinscope}
\end{document}"""
latexs={'article':title,'kindle':kindle}
section='\section{%s}'

def div_list(ls,n):  
    if not isinstance(ls,list) or not isinstance(n,int):  
        return []  
    ls_len = len(ls)  
    if n<=0 or 0==ls_len:  
        return []  
    if n > ls_len:  
        return []  
    elif n == ls_len:  
        return [[i] for i in ls]  
    else:  
        j = int(ls_len/n)
        k = ls_len%n  
        ### j,j,j,...(前面有n-1个j),j+k  
        #步长j,次数n-1  
        ls_return = []  
        for i in range(0,(n-1)*j,j):  
            ls_return.append(ls[i:i+j])  
        #算上末尾的j+k  
        ls_return.append(ls[(n-1)*j:])  
        return ls_return  

def _write_file(path,r):
    f=open(path,'a',encoding='utf8')
    f.write(r)
    f.flush()
    return

def _removef(outpath):
    lsd=['.aux','.log','.out','.xdv','.tex']
    base=os.path.split(outpath)
    basename=os.path.splitext(base[1])[0]
    for ex in lsd:
        try:
            mybsn=basename+ex
            path=os.path.join(base[0],mybsn)
            print(path)
            os.remove(path)
        except Exception as e:
            pass
    return

def sqlTolatex(text,oupf,mtype='kindle',pyin=True):
    title=set()
    #outpath='/home/chen/public/shiwen/'+oupf+'.tex'
    outpath=oupf+'.tex'
    if os.path.exists(outpath):
        os.remove(outpath)

    with open(outpath,'a') as f:
        f.writelines(latexs[mtype])
        f.flush()

    try:
        for li in text[0]:
            if li[1]+li[2] not in title:
                title.add(li[1]+li[2])
                sct=section%li[1]+'\n\n'
                _write_file(outpath,sct)
                
                conn=li[2]+'\n\n'
                _write_file(outpath,conn)
                content=li[3].strip().replace('\n','\n\n')+'\n\n'
                if pyin:
                    #_write_file(outpath,'\begin{pinyinscope}'+'\n')
                    _write_file(outpath,"\\begin{pinyinscope}"+"\n")
                    #_write_file(outpath,'\saohao'+'\n')
                    _write_file(outpath,content)
                    #_write_file(outpath,'\xiaosaohao'+'\n')
                    #_write_file(outpath,'\xiaosaohao'+'\n')
                    _write_file(outpath,'\end{pinyinscope}'+'\n')
                else:
                    _write_file(outpath,content)
                yw=li[4].strip()
                if len(yw)>0:
                    yw=yw.replace('\n','\n\n')+'\n\n'
                    _write_file(outpath,r'\subsection{译文}')
                    _write_file(outpath,yw)
                zx=li[5].strip()
                if len(zx)>0:
                    zx=zx.replace('\n','\n\n')+'\n\n'
                    _write_file(outpath,r'\subsection{注释}')
                    _write_file(outpath,zx)
                sx=li[6].strip()
                if len(sx) > 0:
                    sx=sx.replace('、\n','、')
                    sx=sx.replace('\n','\n\n')+'\n\n'
                    _write_file(outpath,r'\subsection{赏析}')
                    _write_file(outpath,sx)
                
        _write_file(outpath,end)
        os.system('xelatex -no-pdf -interaction=nonstopmode %s' %outpath)
        os.system('xelatex -interaction=nonstopmode %s' %outpath)
        _removef(outpath)
    except Exception as e:
        print(e)
        pass

    

def Gushi2Pdf_author(author,mtype='article',pyin=True):
    """
    Parameters:
        author:按作者
        mtype:分为article,kindle
        pyin: 主体部分是否要标拼音
        ywT:是否要翻译部分
    """        
    
    sqll="select * from gushiwenI where author like '%%%s%%'"%author
    #sqll="select * from gushiwen"
    cur.execute(sqll)
    c=[]
    c.append(cur.fetchall())
    d=set(c)
    text=list(d)
    sqlTolatex(text,author,mtype,pyin)
    os.system('mv %s.pdf /home/chen/public/shiwen/' %author)
    return

def Gushi2Pdf_note(note,mtype='article',pyin=True,ywT=True):
    """
    Parameters:
        note:按分类
        mtype:分为article,kindle
        pyin: 主体部分是否要标拼音
        ywT:是否要翻译部分
    """    
    
    sqll="select * from gushiwenI where note like '%%%s%%'"%note
    #sqll="select * from gushiwen"
    cur.execute(sqll)
    c=[]
    c.append(cur.fetchall())
    d=set(c)
    text=list(d)
    sqlTolatex(text,author,mtype,pyin)
    os.system('mv %s.pdf /home/chen/public/shiwen/' %note)
    return

def sqlTolatex_guwen(text,oupf,mtype='article',pyin=True,ywT=True,cnT=True):
    title=set()
    #outpath='/home/chen/public/shiwen/'+oupf+'.tex'
    outpath=oupf+'.tex'
    if os.path.exists(outpath):
        os.remove(outpath)

    with open(outpath,'a') as f:
        f.writelines(latexs[mtype])
        f.flush()
        
    try:
        for li in text[0]:
            if li[0] not in title:
                title.add(li[0])
                sct=section%li[0]+'\n\n'
                _write_file(outpath,sct)
                
                content=li[1].strip().replace('\n','\n\n')+'\n\n'
                if cnT:
                    _write_file(outpath,r'\subsection{%s}'%li)
                    if pyin:
                        #_write_file(outpath,'\begin{pinyinscope}'+'\n')
                        _write_file(outpath,"\\begin{pinyinscope}"+"\n")
                        #_write_file(outpath,'\saohao'+'\n')
                        _write_file(outpath,content)
                        #_write_file(outpath,'\xiaosaohao'+'\n')
                        #_write_file(outpath,'\xiaosaohao'+'\n')
                        _write_file(outpath,'\end{pinyinscope}'+'\n')
                    else:
                        _write_file(outpath,content)
                        
                yw=li[2].strip().replace('译文及注释','').replace('译文','').replace('全屏','')
                if len(yw)>0 and ywT:
                    yw=yw.replace('\n','\n\n')+'\n\n'
                    _write_file(outpath,r'\subsection{译文}')
                    _write_file(outpath,yw)
                
        _write_file(outpath,end)
        os.system('xelatex -no-pdf -interaction=nonstopmode %s' %outpath)
        os.system('xelatex -interaction=nonstopmode %s' %outpath)
        _removef(outpath)
    except Exception as e:
        print(e)
        pass
    
def Guwen2Pdf_book(book,mtype='article',pyin=True,ywT=True,cnT=True):
    """
    Parameters:
        book:书名
        mtype:分为article,kindle
        pyin: 主体部分是否要标拼音
        cnT:是否要主体章节部分内容
        ywT:是否要翻译部分
    """
    
    sqll="select charpter,content,zhushi from Guwen where book like '%%%s%%'"%book
    #sqll="select * from gushiwen"
    cur.execute(sqll)
    c=[]
    c.append(cur.fetchall())
    d=set(c)
    text=list(d)
    sqlTolatex_guwen(text,book,mtype,pyin,ywT,cnT)
    os.system('mv %s.pdf /home/chen/public/shiwen/' %book)
    return


def sqlTolatex_split(text,oupf,mtype='kindle',pyin=True,ywT=True,zxT=True,sxT=True):
    outpath=oupf+'.tex'
    if os.path.exists(outpath):
        os.remove(outpath)

    with open(outpath,'a') as f:
        f.writelines(latexs[mtype])
        f.flush()

    try:
        for li in text:
            sct=section%li[0]+'\n\n'
            _write_file(outpath,sct)
                
            conn=li[1]+'\n\n'
            _write_file(outpath,conn)
            content=li[2].strip().replace('\n','\n\n')+'\n\n'
            if pyin:
                _write_file(outpath,"\\begin{pinyinscope}"+"\n")
                _write_file(outpath,content)
                _write_file(outpath,'\end{pinyinscope}'+'\n')
            else:
                _write_file(outpath,content)
            yw=li[3].strip()
            if (len(yw)>0)&ywT:
                yw=yw.replace('\n','\n\n')+'\n\n'
                _write_file(outpath,r'\subsection{译文}')
                _write_file(outpath,yw)
            zx=li[4].strip()
            if (len(zx)>0)&zxT:
                zx=zx.replace('\n','\n\n')+'\n\n'
                _write_file(outpath,r'\subsection{注释}')
                _write_file(outpath,zx)
            sx=li[5].strip()
            if (len(sx) > 0)&sxT:
                sx=sx.replace('、\n','、')
                sx=sx.replace('\n','\n\n')+'\n\n'
                _write_file(outpath,r'\subsection{赏析}')
                _write_file(outpath,sx)
                
        _write_file(outpath,end)
        os.system('xelatex -no-pdf -interaction=nonstopmode %s' %outpath)
        os.system('xelatex -interaction=nonstopmode %s' %outpath)
        _removef(outpath)
    except Exception as e:
        print(e)
        pass

def Gushi2Pdf_AuthorSplit(author,mtype='article',pyin=True,ywT=True,zxT=True,sxT=True,split=2):

    sqll="select title,author,content,yiwen,zhus,shangxi from gushiwenI where author like '%%%s%%'"%author
    cur.execute(sqll)
    df=cur.fetchall()
    df=set(df)
    text=list(df)
    title=set()
    allt=[]#最终的文本
    for li in text:
        if li[1]+li[2] not in title:
            title.add(li[1]+li[2])
            allt.append(li)

    allsplit=div_list(allt,split)

    for i,twx in enumerate(allsplit):
        out=author+str(i+1).zfill(2)
        sqlTolatex_split(twx,out,mtype,pyin,ywT,zxT,sxT)
        os.system('mv %s.pdf /home/chen/public/shiwen/' %out)
    return

def Gushi2Pdf_NoteSplit(note,mtype='article',pyin=True,ywT=True,zxT=True,sxT=True,split=2):

    #kk={'note':'','author':''}
    sqll="select title,author,content,yiwen,zhus,shangxi from gushiwenI where note like '%%%s%%'"%note
    cur.execute(sqll)
    df=cur.fetchall()
    df=set(df)
    text=list(df)
    title=set()
    allt=[]#最终的文本
    for li in text:
        if li[1]+li[2] not in title:
            title.add(li[1]+li[2])
            allt.append(li)

    allsplit=div_list(allt,split)

    for i,twx in enumerate(allsplit):
        out=note+str(i+1).zfill(2)
        sqlTolatex_split(twx,out,mtype,pyin,ywT,zxT,sxT)
        os.system('mv %s.pdf /home/chen/public/shiwen/' %out)
    return

def sqlTolatex_guwensplit(text,oupf,mtype='article',pyin=True,ywT=True,cnT=True):
    outpath=oupf+'.tex'
    if os.path.exists(outpath):
        os.remove(outpath)

    with open(outpath,'a') as f:
        f.writelines(latexs[mtype])
        f.flush()
        
    try:
        for li in text:
            sct=section%li[0]+'\n\n'
            _write_file(outpath,sct)
                
            content=li[1].strip().replace('\n','\n\n')+'\n\n'
            if cnT:
                _write_file(outpath,r'\subsection{%s}'%li)
                if pyin:
                    _write_file(outpath,"\\begin{pinyinscope}"+"\n")
                    _write_file(outpath,content)
                    _write_file(outpath,'\end{pinyinscope}'+'\n')
                else:
                    _write_file(outpath,content)
                        
            yw=li[2].strip().replace('译文及注释','').replace('译文','').replace('全屏','')
            if len(yw)>0 and ywT:
                yw=yw.replace('\n','\n\n')+'\n\n'
                _write_file(outpath,r'\subsection{译文}')
                _write_file(outpath,yw)
                
        _write_file(outpath,end)
        os.system('xelatex -no-pdf -interaction=nonstopmode %s' %outpath)
        os.system('xelatex -interaction=nonstopmode %s' %outpath)
        _removef(outpath)
    except Exception as e:
        print(e)
        pass    
    
def Guwen2Pdf_bookSplit(book,mtype='article',pyin=True,ywT=True,cnT=True,split=1):

    #kk={'note':'','author':''}
    sqll="select charpter,content,zhushi from Guwen where book like '%%%s%%'"%book
    cur.execute(sqll)
    df=cur.fetchall()
    df=set(df)
    text=list(df)
    title=set()
    allt=[]#最终的文本
    for li in text:
        if li[1]+li[2] not in title:
            title.add(li[1]+li[2])
            allt.append(li)

    allsplit=div_list(allt,split)

    for i,twx in enumerate(allsplit):
        if len(allsplit)==1:
            out=book
        else:
            out=book+str(i+1).zfill(2)
        sqlTolatex_guwensplit(twx,out,mtype,pyin,ywT,zxT,sxT)
        os.system('mv %s.pdf /home/chen/public/shiwen/' %out)
    return    
    
    
if __name__=="__main__":
    #Sql2Pdf(sys.argv[1])
    #Guwen2Pdf_book(sys.argv[1])
    Gushi2Pdf_AuthorSplit(sys.argv[1])

    
    
