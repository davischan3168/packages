#!/usr/bin/env python3
# -*-coding:utf-8-*-
import sys,os,time
import re


div_style=r'<div style="word-spacing:5px;line-height:1.5">'
def htmlWrapper(content,tag,attr):
    return "<"+tag+" "+attr+">"+content+""

def fontColorWrapper(content,color):
    return htmlWrapper(content,'font','color="#'+color+'"')

def htmHighLight(line):
        keywords=["if","then","else","def","for","in","return","import","print","unsigned","long","int","short","include","class","void","while","const","template"]        
        for i in keywords:
                keywordMatcher=re.compile(r'\b'+i+r'\b')
                line = keywordMatcher.sub(fontColorWrapper(i,'cf0000'), line)
        return line

def txt2htmlv2(txtName,index=True):
    """
    txtName:文件的名称（含所在的文件夹）
    index：  True,将第四节的列入目录
             False,不含第四节的目录
    ---------------
    在txtName文件目录下生产一份html文件。
    """    
    if os.path.isfile(txtName):
        path=os.path.abspath(txtName)
        htmlName=os.path.splitext(path)[0]+'.html'
    else:
        sys.exit()
        
    if os.path.exists(htmlName):
        os.remove(htmlName)

    table='table.txt'
    #设置保存目录的暂时文件
    content="output.txt"
    #设置保存内容的暂时文件
    tb=open(table,'w',encoding='utf8')
    ctt=open(content,"w",encoding='utf8')
    
    tb.write('<div id="table-of-contents"> <h2>目录</h2><div id="text-table-of-contents"><ul>')
    try:
        txt=open(txtName,'r',encoding='utf8')
        text=txt.readlines()
    except:
        txt=open(txtName,'r',encoding='gbk')
        text=txt.readlines()
    txt.close()

    text=[x.strip() for x in text]
    s='\n'.join(text)
    ss=re.sub(r'\n{1,}',r'\n\n',s)
    text=ss.splitlines()

    mt=re.compile(r'^第\w{1,3}编')
    j=1

    mtrec=re.compile(r'^第\w{1,3}篇')
    mtrec1=re.compile(r'^第\w{1,3}章')
    i=1

    mt3=re.compile(r'^第\w{1,3}节')
    k=1
    mt4=re.compile(r'^\w{1,3}、')
    l=1    
    ctt.write(div_style)

    for line in text:
        line=line.strip()
        if mt.match(line) is not None:
            tb.write(r'<li><a href="#sec-%s">%s</a></li>'%(j,line))
            title=r'<h2 id="sec-%s">%s</h2> '%(j,line)
            ctt.write(title)
            j=j+1
        elif mt3.match(line) is not None:
            tb.write(r'<li><a href="#sec-%s">%s</a></li>'%(k,line))
            title=r'<h4 id="sec-%s">%s</h4> '%(k,line)
            ctt.write(title)            
            k=k+1
        
        elif (mt4.match(line) is not None) and index:
            #if index:
            tb.write(r'<li><a href="#sec-%s">%s</a></li>'%(l,line))
            title=r'<h5 id="sec-%s">%s</h5> '%(l,line)
            ctt.write(title)            
            l=l+1
            """else:
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
                line='<span style="font-size:90%%;letter-spacing:1px"> %s </span>\n'%line
                ctt.write(line)"""
                
        elif mtrec.match(line) is not None:
            tb.write(r'<li><a href="#sec-%s">%s</a></li>'%(i,line))
            title=r'<h3 id="sec-%s">%s</h3> '%(i,line)
            #print(title)
            ctt.write(title)
            i=i+1
        elif mtrec1.match(line) is not None:
            tb.write(r'<li><a href="#sec-%s">%s</a></li>'%(i,line))
            title=r'<h3 id="sec-%s">%s</h3> '%(i,line)
            #print(title)
            ctt.write(title)
            i=i+1            
            
        elif len(line)>0:
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
            #line=r"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"+htmHighLight(line)
            line=""+htmHighLight(line)
            line='<span style="font-size:90%%;letter-spacing:1px"> %s </span>\n'%line
            ctt.write(line)
            #print(line)
            #time.sleep(1)
        else:
            line='</br> <br/>'
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
    print("\n转换成功,保存在%s"%htmlName)
    os.remove(table)
    os.remove(content)
    return
if __name__=="__main__":
    txt2htmlv2(sys.argv[1])
