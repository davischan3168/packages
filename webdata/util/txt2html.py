#!/usr/bin/env python3
# -*-coding:utf-8-*-

import sys,os,time
import re

cstr=['，','。','？','！','；','：']
#temp = "想做/ 兼_职/学生_/ 的 、加,我Q：  1 5.  8 0. ！！？？  8 6 。0.  2。 3     有,惊,喜,哦"  
#temp = temp.decode("utf8")  
#string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),temp)

div_style=r'<div style="word-spacing:5px;line-height:1.5">'
htmlcode='''<html>
<meta http-equiv="Content-Type" content="text/html"; charset="utf8" />
<body bgcolor="#C7EDF0">
<title> My Html File</title>'''

if sys.platform.startswith('win'):
    htmlcode1=htmlcode%'utf8'
elif sys.platform in ['linux']:
    htmlcode1=htmlcode%'utf8'
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
    
def txt2htmlv1(txtName,index=True):
    """
    txtName:文件的名称（含所在的文件夹）
    index：  True,将第四节的列入目录
             False,不含第四节的目录
    ---------------
    在python运行目录下生产一份html文件。
    """
    files=[]
    
    if isinstance(txtName,str):
        files.append(txtName)
    elif isinstance(txtName,list):
        files.extend(txtName)

    htmlName="output.html"
    
    table='table.txt'
    content="output.txt"    
    if os.path.exists(htmlName):
        os.remove(htmlName)

    tb=open(table,'w',encoding='utf8')
    ctt=open(content,"w",encoding='utf8')

    tb.write('''<div id="table-of-contents">
    <h2>Table of Contents</h2>
    <div id="text-table-of-contents">
    <ul>\n''')

    #ctt.write('<div id="content">\n')
    mt1=re.compile(r'^第\w{1,3}编')
    #mtI=re.compile(r'^第\w{1,3}篇')
    muI=1

    
    mt2=re.compile(r'^第\w{1,3}章')
    muII=1

    mt3=re.compile(r'^第\w{1,3}节')
    muIII=1
    
    mt4=re.compile(r'^\w{1,3}、')
    muIV=1
    
    for i,txtName in enumerate(files):
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

        ntitle=os.path.splitext(os.path.basename(txtName))[0]#[2:]
        tb.write('<li><a href="#sec-%s-%s">%s</a></li>\n'%(i,txtName,ntitle))
        titles='''<h1 id="sec-%s-%s">%s</h1> \n'''%(i,txtName,ntitle)
        ctt.write(titles)

        for line in text:
            line=line.strip()
            #print(line)
            if mt1.match(line) is not None:
                if muI>1:
                    ctt.write('</div>\n')
                    tb.write('</ul>\n')
                    tb.write('</li>\n')
                tb.write('<li><a href="#sec-%s-%s">%s</a>\n'%(muI,txtName,line))
                tb.write('\n')
                titles='''<div id="outline-container-%s" class="outline-%s">
                <h2 id="sec-%s-%s">%s</h2>\n'''%(muI,muI+1,muI,txtName,line)
                ctt.write(titles)
                #ctt.write('\n')
                muI=muI+1
            elif mt2.match(line) is not None:
                if muII>1:
                    ctt.write('</div>\n')
                    tb.write('</ul>\n')
                    #tb.write('</li>\n')
                tb.write('<ul><li><a href="#sec-%s-%s-%s">%s</a></li>\n'%(muI,muII,txtName,line))
                #tb.write('\n')
                titles='<div id="outline-container-%s-%s"><h3 id="sec-%s-%s-%s">%s</h4>\n'%(muI,muII,muI,muII,txtName,line)
                ctt.write(titles)
                #ctt.write('\n')
                muII=muII+1
            elif mt3.match(line) is not None:
                if muIII>1:
                    ctt.write('</div>\n')
                    #tb.write('</ul>\n')
                if index:
                    tb.write('<ul><li><a  href="#sec-%s-%s-%s-%s">%s</a></li></ul>\n'%(muI,muII,muIII,txtName,line))
                    #tb.write('\n')
                    titles='<div id="outline-container-%s-%s-%s"><h4 id="sec-%s-%s-%s-%s">%s</h4>\n '%(muI,muII,muIII,muI,muII,muIII,txtName,line)
                    ctt.write(titles)            
                    #tb.write('\n')
                    muIII=muIII+1
            #elif (muI==1) and (muII == 1) and (muIII ==1):
            #        ctt.write('<div>')

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
                line='<p>&emsp;&emsp;%s</p>\n'%line
                ctt.write(line)
            else:
                pass

    ctt.write('</div>')
    #tb.write(r'</ul></div>')
    tb.write(r'</ul></div></div>')    
    ctt.close()
    tb.close()

    tb=open(table,'r',encoding='utf8')
    ctt=open(content,'r',encoding='utf8')
    if os.path.exists(htmlName):
        os.remove(htmlName)    
    try:
        html=open(htmlName,'a',encoding='utf8')
        html.write(htmlcode)
        html.write(tb.read())
        html.write(ctt.read())
    except:
        html=open(htmlName,'a',encoding='gbk')
        html.write(htmlcode)
        html.write(tb.read())
        html.write(ctt.read())
        
    tb.close()
    ctt.close()
    html.write('</body></html>')
    html.close()
    print("\n转换成功,保存在%s"%htmlName)
    os.remove(table)
    os.remove(content)
    return

    

def txt2html_inonefile(txtName,index=True):
    """
    txtName:文件的名称（含所在的文件夹）
    index：  True,将第四节的列入目录
             False,不含第四节的目录
    ---------------
    在txtName文件目录下生产一html文件。
    """
    files=[]
    if os.path.isfile(txtName):
        path=os.path.abspath(txtName)
        files.append(path)
        htmlName=os.path.splitext(path)[0]+'.html'
    else:
        print("%s is not file...."%txtName)
        sys.exit()
    
    if os.path.exists(htmlName):
        os.remove(htmlName)

    table='table.txt'
    #设置保存目录的暂时文件
    content="output.txt"
    #设置保存内容的暂时文件

    tb=open(table,'w',encoding='utf8')
    ctt=open(content,"w",encoding='utf8')

    tb.write('''<div id="table-of-contents">
    <h2>Table of Contents</h2>
    <div id="text-table-of-contents">
    <ul>\n''')

    #ctt.write('<div id="content">\n')
    mt1=re.compile(r'^第\w{1,3}编')
    #mtI=re.compile(r'^第\w{1,3}篇')
    muI=1

    
    mt2=re.compile(r'^第\w{1,3}章')
    muII=1

    mt3=re.compile(r'^第\w{1,3}节')
    muIII=1
    
    mt4=re.compile(r'^\w{1,3}、')
    muIV=1
    
    for i,txtName in enumerate(files):
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

        ntitle=os.path.splitext(os.path.basename(txtName))[0]#[2:]
        tb.write('<li><a href="#sec-%s-%s">%s</a></li>\n'%(i,txtName,ntitle))
        titles='''<h1 id="sec-%s-%s">%s</h1> \n'''%(i,txtName,ntitle)
        ctt.write(titles)

        for line in text:
            line=line.strip()
            #print(line)
            if mt1.match(line) is not None:
                if muI>1:
                    ctt.write('</div>\n')
                    tb.write('</ul>\n')
                    tb.write('</li>\n')
                tb.write('<li><a href="#sec-%s-%s">%s</a>\n'%(muI,txtName,line))
                tb.write('\n')
                titles='''<div id="outline-container-%s" class="outline-%s">
                <h2 id="sec-%s-%s">%s</h2>\n'''%(muI,muI+1,muI,txtName,line)
                ctt.write(titles)
                #ctt.write('\n')
                muI=muI+1
            elif mt2.match(line) is not None:
                if muII>1:
                    ctt.write('</div>\n')
                    tb.write('</ul>\n')
                    #tb.write('</li>\n')
                tb.write('<ul><li><a href="#sec-%s-%s-%s">%s</a></li>\n'%(muI,muII,txtName,line))
                #tb.write('\n')
                titles='<div id="outline-container-%s-%s"><h3 id="sec-%s-%s-%s">%s</h4>\n'%(muI,muII,muI,muII,txtName,line)
                ctt.write(titles)
                #ctt.write('\n')
                muII=muII+1
            elif mt3.match(line) is not None:
                if muIII>1:
                    ctt.write('</div>\n')
                    #tb.write('</ul>\n')
                if index:
                    tb.write('<ul><li><a  href="#sec-%s-%s-%s-%s">%s</a></li></ul>\n'%(muI,muII,muIII,txtName,line))
                    #tb.write('\n')
                    titles='<div id="outline-container-%s-%s-%s"><h4 id="sec-%s-%s-%s-%s">%s</h4>\n '%(muI,muII,muIII,muI,muII,muIII,txtName,line)
                    ctt.write(titles)            
                    #tb.write('\n')
                    muIII=muIII+1
            #elif (muI==1) and (muII == 1) and (muIII ==1):
            #        ctt.write('<div>')

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
                line='<p>&emsp;&emsp;%s</p>\n'%line
                ctt.write(line)
            else:
                pass

    ctt.write('</div>')
    #tb.write(r'</ul></div>')
    tb.write(r'</ul></div></div>')    
    ctt.close()
    tb.close()    

    tb=open(table,'r',encoding='utf8')
    ctt=open(content,'r',encoding='utf8')

    if os.path.exists(htmlName):
        os.remove(htmlName)
    try:
        html=open(htmlName,'w',encoding='utf8')
        html.write(htmlcode)
        html.write(tb.read())
        html.write(ctt.read())
    except:
        html=open(htmlName,'w',encoding='gbk')
        html.write(htmlcode)
        html.write(tb.read())
        html.write(ctt.read())

    tb.close()
    ctt.close()
    html.write('</body></html>')
    html.close()
    print("\n转换成功,保存在%s"%htmlName)
    os.remove(table)
    os.remove(content)
    return

def txt2html_odir(txtName,index=False):
    """
    txtName:文件的名称（含所在的文件夹）,或是文件名的list
    index：  True,将第四节的列入目录
             False,不含第四节的目录
    ---------------
    在txtName文件目录下生产一份html文件。
    """    
    if isinstance(txtName,list):
        for f in txtName:
            print(f)
            txt2html_inonefile(f,index=index)
    else:
        txt2html_inonefile(txtName,index=index)
    return

def txt2htmldir(path=None,func=txt2html_odir,index=False):
    """
    path:文件夹的名称,若没有输入参数，则默认为None，即当前目录。
    func:txt2html_odir,形成一个个单独的文件，并保存在源文件的目录下。
        :txt2htmlv1，合并成一个文件，文件保存在当前工作目录下。
    path:所选择的文件夹
    """
    if path == None:
        path=os.getcwd()
    dirset=[]
    for root,dirs,files in os.walk(path):
        for f in files:
            if os.path.splitext(f)[1] == '.txt':
                fpath=os.path.join(root,f)
                dirset.append(fpath)
    func(dirset,index=index)
    return



if __name__=="__main__":
    #txt2htmlv1(sys.argv[1])
    txt2htm(sys.argv[1])
    #txt2htmldir(sys.argv[1],func=txt2html_odir,index=False)
    #txt2html_inonefile(sys.argv[1])
    #txt2html_odir(sys.argv[1])
