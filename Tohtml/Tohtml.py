#!/usr/bin/env python3
# -*-coding:utf-8-*-

import sys,os,time
import re
from packages.Tohtml.cfg import title,endd,title1

def C2html(txtpath,output='output.html',index=True):
    """
    txtpath:为单独的文件、一系列文件或一段字符
    并将这些文件中的内容输出到一份html 文件中
    """
    files=[]
    if os.path.isfile(txtpath):
        if os.path.splitext(txtpath)[1] in ['.txt']:
            files.append(txtpath)
            #tname=os.path.splitext(os.path.basename(txtpath))[0]
    elif isinstance(txtpath,list):
        for f in txtpath:
            if os.path.isfile(txtpath) and (os.path.splitext(txtpath)[1] in ['.txt']):
                files.append(txtpath)
                
    elif isinstance(txtpath,str):
        path123='tempsdfsf.txt'
        fff=open(path123,'w',encoding='utf8')
        fff.write(txtpath)
        fff.close()
        files.append(path123)
                
    else:
        sys.exit()
        

    table='table.txt'#文件目录
    content="output.txt"#文件内容
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
        #txtName=ntitle
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
                #line=""+htmHighLight(line)
                #line='<span style="font-size:90%%;letter-spacing:1px"> %s </span>\n'%line
                line='<p>%s</p>\n'%line
                ctt.write(line)
            else:
                #line='</br> <br/>'
                #print(line)
                #ctt.write(line)
                pass

    ctt.write('</div>')
    #tb.write(r'</ul></div>')
    tb.write(r'</ul></div></div>')    
    ctt.close()
    tb.close()
    if os.path.exists(output):
       os.remove(output)

    if os.path.exists(path123):
        os.remove(path123)
        
    tb=open(table,'r',encoding='utf8')
    ctt=open(content,'r',encoding='utf8')

    try:
        html=open(output,'a',encoding='utf8')
        html.write(title+'\n'+title1+'\n')
        html.write('<div id="content">\n')
        html.write(tb.read())
        html.write(ctt.read())
    except:
        html=open(output,'a',encoding='gbk')
        #html.write(title+'\n')
        html.write(title+'\n'+title1+'\n')
        html.write('<div id="content">\n')
        html.write(tb.read())
        html.write(ctt.read())

        
    tb.close()
    ctt.close()
    html.write(endd)
    html.close()
    print("\n转换成功,保存在%s"%output)
    os.remove(table)
    os.remove(content)
    return
################################################
def C2htmlBase(txtpath,index=True):
    """
    txtpath:为单独的文件或一段字符
    
    """
    files=[]
    if os.path.isfile(txtpath):
        if os.path.splitext(txtpath)[1] in ['.txt']:
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
        

    table='table.txt'#文件目录
    content="output.txt"#文件内容
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
        path=os.path.splitext(os.path.abspath(txtName))[0]+'.html'
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
        #txtName=ntitle
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
                #line=""+htmHighLight(line)
                #line='<span style="font-size:90%%;letter-spacing:1px"> %s </span>\n'%line
                line='<p>%s</p>\n'%line
                ctt.write(line)
            else:
                #line='</br> <br/>'
                #print(line)
                #ctt.write(line)
                pass

    ctt.write('</div>')
    #tb.write(r'</ul></div>')
    tb.write(r'</ul></div></div>')    
    ctt.close()
    tb.close()
    if os.path.exists(output):
       os.remove(output)

    if os.path.exists(path123):
        os.remove(path123)
        
    tb=open(table,'r',encoding='utf8')
    ctt=open(content,'r',encoding='utf8')

    output=

    try:
        html=open(output,'a',encoding='utf8')
        html.write(title+'\n'+title1+'\n')
        html.write('<div id="content">\n')
        html.write(tb.read())
        html.write(ctt.read())
    except:
        html=open(output,'a',encoding='gbk')
        #html.write(title+'\n')
        html.write(title+'\n'+title1+'\n')
        html.write('<div id="content">\n')
        html.write(tb.read())
        html.write(ctt.read())

        
    tb.close()
    ctt.close()
    html.write(endd)
    html.close()
    print("\n转换成功,保存在%s"%output)
    os.remove(table)
    os.remove(content)
    return
##########################################################
def C2html_inOne(txtpath,output='output.html',index=True):
    """
    将目录txtpath下的txt文件内容全部转到output.html文件中
    """
    files=[]
    if os.path.isdir(txtpath)
        for root,ds,fs in os.walk(txtpath):
            for f in fs:
                if os.path.splitext(txtpath)[1] in ['.txt']:
                    files.append(root+'/'+f)

    if len(files)>0:
        C2html(files,output=output,index=index)
    return
######################################################
def C2html_OnebyOne(txtpath,index=True):
    """
    将目录txtpath下的txt文件内容逐一转到相应的html文件中
    """
    files=[]
    if os.path.isdir(txtpath)
        for root,ds,fs in os.walk(txtpath):
            for f in fs:
                if os.path.splitext(txtpath)[1] in ['.txt']:
                    C2htmlBase(txtpath=root+'/'+f,index=index)
    else:
        print("txtpath is not dir or the dir has no txt files")
    return

    
if __name__=="__main__":
    C2html(sys.argv[1])
            
