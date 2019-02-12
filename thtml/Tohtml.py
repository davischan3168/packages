#!/usr/bin/env python3
# -*-coding:utf-8-*-

import sys,os,time
import re
from thtml.cfg import title,endd,title1,title2

pp='<p style="word-spacing:10px;line-height:1.5">&emsp;&emsp;%s</p>\n'
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
            if os.path.isfile(f) and (os.path.splitext(f)[1] in ['.txt']):
                files.append(f)    
    elif os.path.isfile(txtpath):
        if os.path.splitext(txtpath)[1] in ['.txt']:
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

    mt1=m1
    muI=1
    
    mt2=m2
    muII=1

    mt3=m3
    muIII=1
    
    mt4=m4
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
                line=pp%line
                ctt.write(line)
            else:
                pass

    ctt.write('</div>')
    #tb.write(r'</ul></div>')
    tb.write(r'</ul></div></div>')    
    ctt.close()
    tb.close()
    if os.path.exists(output):
       os.remove(output)

    
    tb=open(table,'r',encoding='utf8')
    ctt=open(content,'r',encoding='utf8')

    try:
        html=open(output,'a',encoding='utf8')
        html.write(ll)
        #html.write('<div id="content">\n')
        html.write('<div id="content",style="background-color:#C7EDF0">\n')
        html.write(tb.read())
        html.write(ctt.read())
    except:
        html=open(output,'a',encoding='gbk')
        html.write(ll)
        #html.write('<div id="content">\n')
        html.write('<div id="content",style="background-color:#C7EDF0">\n')
        html.write(tb.read())
        html.write(ctt.read())

        
    tb.close()
    ctt.close()
    html.write(endd)
    html.close()
    print("\n转换成功,保存在%s"%output)
    os.remove(table)
    os.remove(content)
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
    return p
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

    mt1=m1
    muI=1
    
    mt2=m2
    muII=1

    mt3=m3
    muIII=1
    
    mt4=m4
    muIV=1
    
    for i,txtName in enumerate(files):
        output=os.path.splitext(os.path.abspath(txtName))[0]+'.html'
        
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
                line=pp%line
                ctt.write(line)
            else:
                pass

    ctt.write('</div>')
    #tb.write(r'</ul></div>')
    tb.write(r'</ul></div></div>')    
    ctt.close()
    tb.close()
    if os.path.exists(output):
       os.remove(output)

    try:
        if os.path.exists(path123):
            os.remove(path123)
    except:
        pass
    tb=open(table,'r',encoding='utf8')
    ctt=open(content,'r',encoding='utf8')
    
    try:        
        html=open(output,'a',encoding='utf8')
        html.write(ll)
        #html.write('<div id="content">\n')
        html.write('<div id="content",style="background-color:#C7EDF0">\n')
        html.write(tb.read())
        html.write(ctt.read())
    except:
        html=open(output,'a',encoding='gbk')
        html.write(ll)
        #html.write('<div id="content">\n')
        html.write('<div id="content",style="background-color:#C7EDF0">\n')
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
def C2html_inOne(txtpath=None,output='output.html',px='\d{1,3}',index=True):
    """
    将目录txtpath下的txt文件内容全部转到output.html文件中
    px:文中排序的基准。
    """
    files=[]
    if txtpath is None:
        txtpath=os.getcwd()
            
    elif not os.path.isdir(txtpath):
        raise("txtpath is not dir")
    
    for root,ds,fs in os.walk(txtpath):
        for f in fs:
            if os.path.splitext(f)[1] in ['.txt']:
                #print(f)
                files.append(root+'/'+f)

    if len(files)>0:
        ss={}
        try:
            for i in files:
                dd=re.findall(px,i)
                num=int([j for j in dd if len(j)>0][0])
                ss[num]=i
            dds=sorted(ss.items(),key=lambda item:item[0])
            files=[]
            for i in dds:
                files.append(i[1])
        except Exception as e:
            print(e)
                
        C2html(txtpath=files,output=output,index=index)
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
    C2html_inOne(sys.argv[1])
    pass
            
