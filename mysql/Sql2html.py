#!/usr/bin/env python3
# -*-coding:utf-8-*-

import sys,os,time
import re
from pypinyin import pinyin, lazy_pinyin, Style
import MySQLdb
#import webdata as wd

ssx='译赏内容整理自网络（或由匿名网友上传），原作者已无法考证，版权归原作者所有。本站免费发布仅供学习参考，其观点不代表本站立场。站务邮箱：service@gushiwen.org'

div_style=r'<div style="word-spacing:5px;line-height:1.5">'
span_style=r'<span style="word-spacing:5px;line-height:1.5">%s</span>'
#text-indent设置抬头距离css缩进
#letter-spacing来设置字与字间距_字符间距离，字体间距css样式

def htmlWrapper(content,tag,attr):
    return "<"+tag+" "+attr+">"+content+""

def fontColorWrapper(content,color):
    return htmlWrapper(content,'font','color="#'+color+'"')

def b_pinyin(line):
    #py=pinyin(line, errors='ignore')
    py=pinyin(line)
    x=[]
    for i in py:
        x.extend(i)
    p=' '.join(x)
    nl='<ruby style="font-size:110%%;letter-spacing:1px"> %s <rt style="font-size:70%%;color:blue;letter-spacing:2px"> %s </rt> </ruby>'%(line,p)
    return nl
                    

def htmHighLight(line):
        keywords=["if","then","else","def","for","in","return","import","print","unsigned","long","int","short","include","class","void","while","const","template"]        
        for i in keywords:
                keywordMatcher=re.compile(r'\b'+i+r'\b')
                line = keywordMatcher.sub(fontColorWrapper(i,'cf0000'), line)

        return line

conn = MySQLdb.connect(host="localhost", port=3306, user='root', passwd='801019', db='SDD', charset="utf8")
cur = conn.cursor()

def Sql2html_Guwen(book,cnT=True,ywT=True):
    
    sqll="select charpter,content,zhushi from Guwen where book like '%%%s%%'"%book
    cur.execute(sqll)
    c=[]
    c.append(cur.fetchall())
    d=set(c)
    text1=list(d)        

    table='table.txt'
    htmlName="epub/%s.html"%book
    if os.path.exists(htmlName):
        os.remove(htmlName)
    content="output.txt"
    tb=open(table,'w',encoding='utf8')#临时文件，生产目录文件
    ctt=open(content,"w",encoding='utf8')#临时文件，生产正文
    
    tb.write('<div id="table-of-contents"> <h2>目录</h2><div id="text-table-of-contents"><ul>')

    ctt.write(div_style) 
    for i,dd in enumerate(text1[0]):

        if cnT:
            ss=re.sub(r'\n{1,}',r'\n\n',dd[1])
            text=ss.splitlines()
        
            tb.write(r'<li><a href="#sec-%s%s">%s</a></li>'%(i,dd[0],dd[0]))
            title=r'<h2 id="sec-%s%s">%s</h2> '%(i,dd[0],dd[0])
            ctt.write(title)

            for line in text:
                line=line.strip()

                if len(line)>0:
                    line=line\
                          .replace('&','&')\
                          .replace('<','<')\
                          .replace('® ','® ')\
                          .replace('"','"')\
                          .replace('©','©')\
                          .replace('™','™')\
                          .replace('<','<')\
                          .replace('\t',"    ").\
                          replace(' ',' ')
                    line=""+htmHighLight(line)
                    ctt.write(line)
                else:
                    line='</br> <br/> \n'
                    ctt.write(line)

        if (len(dd[2])>0) & ywT & (dd[2] != 'Null'):
            tt=dd[2].replace('1、\n','1、').replace('2、\n','2、').replace('3、\n','3、').replace('4、\n','4、').replace('5、\n','5、').replace('译文及注释\n','').replace('译文\n','').replace('全屏\n','').replace(ssx,'')
            sss=re.sub(r'\n{1,}',r'\n\n',tt)
            textyw=sss.splitlines()

            tb.write(r'<li><a href="#sec-%s%s译文">%s译文</a></li>'%(i,dd[0],dd[0]))

            title=r'<h2 id="sec-%s%s译文">%s译文</h2> '%(i,dd[0],dd[0])
            ctt.write(title)                
            for line in textyw:
                line=line.strip()

                if len(line)>0:
                    line=line\
                          .replace('&','&')\
                          .replace('<','<')\
                          .replace('® ','® ')\
                          .replace('"','"')\
                          .replace('©','©')\
                          .replace('™','™')\
                          .replace('<','<')\
                          .replace('\t',"    ").\
                          replace(' ',' ')
                    line=""+htmHighLight(line)
                    ctt.write(line)
                else:
                    line='</br> <br/> \n'
                    #print(line)
                    ctt.write(line)                
                
    ctt.write(r'</div>')
    tb.write(r'</ul></div></div>')    
    ctt.close()
    tb.close()

    tb=open(table,'r',encoding='utf8')
    ctt=open(content,'r',encoding='utf8')
    if os.path.exists(htmlName):
        os.remove(htmlName)    
    try:
        html=open(htmlName,'a',encoding='utf8')
        html.write(r'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
        html.write(tb.read())
    except:
        html=open(htmlName,'a',encoding='gbk')
        html.write(r'<meta http-equiv="Content-Type" content="text/html; charset=gbk" />')
        html.write(tb.read())

    try:
        html=open(htmlName,'a',encoding='utf8')        
        html.write(ctt.read())
    except:
        html=open(htmlName,'a',encoding='gbk')        
        html.write(ctt.read())
        
    tb.close()
    ctt.close()
    html.close()
    print("\n转换成功,保存在 ----> %s"%htmlName)
    os.remove(table)
    os.remove(content)
    return

def Sql2html_GushiByNote(note,ywT=True,zhusT=True,shangxT=True):
    
    sqll="select title,author,content,yiwen,zhus,shangxi from gushiwenI where note like '%%%s%%'"%note
    cur.execute(sqll)
    c=[]
    c.append(cur.fetchall())
    d=set(c)
    text1=list(d)
    _settle(text1,note,ywT,zhusT,shangxT)
    return

def Sql2html_GushiByAuthor(author,ywT=True,zhusT=True,shangxT=True):
    
    sqll="select title,author,content,yiwen,zhus,shangxi from gushiwenI where author like '%%%s%%'"%author
    cur.execute(sqll)
    c=[]
    c.append(cur.fetchall())
    d=set(c)
    text1=list(d)        
    _settle(text1,author,ywT,zhusT,shangxT)
    return

def _settle(text1,author,ywT=True,zhusT=True,shangxT=True):
    table='table.txt'
    htmlName="epub/%s.html"%author
    if os.path.exists(htmlName):
        os.remove(htmlName)
    content="output.txt"
    tb=open(table,'w',encoding='utf8')#临时文件，生产目录文件
    ctt=open(content,"w",encoding='utf8')#临时文件，生产正文
    only=set()
    
    tb.write('<div id="table-of-contents"> <h2>目录</h2><div id="text-table-of-contents"><ul>')

    ctt.write(div_style)
    for i,dd in enumerate(text1[0]):
        if (dd[0],dd[1],dd[2]) not in only:
            only.add((dd[0],dd[1],dd[2]))
            
            ss=re.sub(r'\n{1,}',r'\n\n',dd[2])
            text=ss.splitlines()
        
            tb.write(r'<li><a href="#sec-%s%s">%s</a></li>'%(i,dd[0],dd[0]))
            title=r'<h2 id="sec-%s%s">%s</h2> '%(i,dd[0],dd[0])
            ctt.write(title)

            ctt.write(dd[1]+'</br> <br/>')

            for line in text:
                line=line.strip()

                if len(line)>0:
                    line=line\
                          .replace('&','&')\
                          .replace('<','<')\
                          .replace('® ','® ')\
                          .replace('"','"')\
                          .replace('©','©')\
                          .replace('™','™')\
                          .replace('<','<')\
                          .replace('\t',"    ").\
                          replace(' ',' ')
                    line=""+htmHighLight(line)
                    line=b_pinyin(line)
                    ctt.write(line)
                else:
                    line='</br> <br/>'
                    ctt.write(line)

            if (len(dd[3])>0) & ywT & (dd[3] != 'Null'):
                tt=dd[3].replace('译文及注释\n','').replace('译文\n','').replace('全屏\n','')
                sss=re.sub(r'\n{1,}',r'\n\n',tt)
                textyw=sss.splitlines()

                tb.write(r'<li><a href="#sec-%s%s译文">%s译文</a></li>'%(i,dd[0],dd[0]))

                title=r'<h3 id="sec-%s%s译文">%s译文</h3> '%(i,dd[0],dd[0])
                ctt.write(title)                
                for line in textyw:
                    line=line.strip()

                    if len(line)>0:
                        line=line\
                              .replace('&','&')\
                              .replace('<','<')\
                              .replace('® ','® ')\
                              .replace('"','"')\
                              .replace('©','©')\
                              .replace('™','™')\
                              .replace('<','<')\
                              .replace('\t',"    ").\
                              replace(' ',' ')
                        line=""+htmHighLight(line)
                        line='<p><span style="font-size:90%%;letter-spacing:1px"> %s </span></p>\n'%line
                        ctt.write(line)
                    else:
                        #line='</br> <br/>'
                        #ctt.write(line)
                        pass

            if (len(dd[4])>0) & zhusT & (dd[4] != 'Null'):
                tt=dd[4].replace('译文及注释\n','').replace('译文\n','').replace('全屏\n','')
                sss=re.sub(r'\n{1,}',r'\n\n',tt)
                textyw=sss.splitlines()

                tb.write(r'<li><a href="#sec-%s%s注释">%s注释</a></li>'%(i,dd[0],dd[0]))

                title=r'<h3 id="sec-%s%s注释">%s注释</h3> '%(i,dd[0],dd[0])
                ctt.write(title)                
                for line in textyw:
                    line=line.strip()

                    if len(line)>0:
                        line=line\
                              .replace('&','&')\
                              .replace('<','<')\
                              .replace('® ','® ')\
                              .replace('"','"')\
                              .replace('©','©')\
                              .replace('™','™')\
                              .replace('<','<')\
                              .replace('\t',"    ").\
                              replace(' ',' ')
                        line=""+htmHighLight(line)
                        line='<p><span style="font-size:90%%;letter-spacing:1px"> %s </span></p>\n'%line
                        ctt.write(line)
                    else:
                        #line='</br> <br/>'
                        #ctt.write(line)
                        pass

            if (len(dd[5])>0) & shangxT & (dd[5] != 'Null'):
                tt=dd[5].replace('1、\n','1、').replace('2、\n','2、').replace('3、\n','3、').replace('4、\n','4、').replace('5、\n','5、').replace('6、\n','6、').replace('7、\n','7、').replace(ssx,'').replace('8、\n','8、').replace('9、\n','9、')
                sss=re.sub(r'\n{1,}',r'\n\n',tt)
                textyw=sss.splitlines()

                tb.write(r'<li><a href="#sec-%s%s赏析">%s赏析</a></li>'%(i,dd[0],dd[0]))

                title=r'<h3 id="sec-%s%s赏析">%s赏析</h3> '%(i,dd[0],dd[0])
                ctt.write(title)                
                for line in textyw:
                    line=line.strip()

                    if len(line)>0:
                        line=line\
                              .replace('&','&')\
                              .replace('<','<')\
                              .replace('® ','® ')\
                              .replace('"','"')\
                              .replace('©','©')\
                              .replace('™','™')\
                              .replace('<','<')\
                              .replace('\t',"    ").\
                              replace(' ',' ')
                        line=""+htmHighLight(line)
                        line='<p><span style="font-size:90%%;letter-spacing:1px"> %s </span></p>\n'%line
                        ctt.write(line)
                    else:
                        #line='</br> <br/>'
                        #ctt.write(line)
                        pass
                        
                        
    ctt.write(r'</div>')
    tb.write(r'</ul></div></div>')    
    ctt.close()
    tb.close()

    tb=open(table,'r',encoding='utf8')
    ctt=open(content,'r',encoding='utf8')
    if os.path.exists(htmlName):
        os.remove(htmlName)    
    try:
        html=open(htmlName,'a',encoding='utf8')
        html.write(r'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
        html.write(tb.read())
    except:
        html=open(htmlName,'a',encoding='gbk')
        html.write(r'<meta http-equiv="Content-Type" content="text/html; charset=gbk" />')
        html.write(tb.read())

    try:
        html=open(htmlName,'a',encoding='utf8')        
        html.write(ctt.read())
    except:
        html=open(htmlName,'a',encoding='gbk')        
        html.write(ctt.read())
        
    tb.close()
    ctt.close()
    html.close()
    print("\n转换成功,保存在 ----> %s"%htmlName)
    os.remove(table)
    os.remove(content)
    return

if __name__=="__main__":
    #Sql2Pdf(sys.argv[1])
    #Sql2html_guwen(sys.argv[1])
    Sql2html_GushiByNote(sys.argv[1])
    #Sql2html_GushiByAuthor(sys.argv[1])

