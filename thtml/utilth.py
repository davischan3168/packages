#!/usr/bin/env python3
# -*-coding:utf-8-*-
import os
import sys
import re
import util.ch2num as ut


cc=re.compile('[，、:-》.《—_;；〈〉<>【】（）()\s]')
def GFlist(path,regrex1=None,research=None,startw=None):
    """
    regrex1:为re.compile 的类型
    startw:re.compile类型
    research: str or list
    """
    rs=[]
    if isinstance(research ,list):
        rs.extend(research)
    elif isinstance(research ,str):
        rs.append(research)
        
    ss={}
    for root,ds,fs in os.walk(path):
        for f in fs:
            #print(f)
            if regrex1 is not None:
                #print('ok....1')
                if os.path.splitext(f)[1] in ['.txt']:
                    i1=[i for i in regrex1.findall(f) if len(i)>0]
                    i2=[i for i in regrex1.findall(ut.ChNumToArab(f)) if len(i)>0]
                    if len(i1)>0:
                        num=int(i1[0])
                        ss[num]=os.path.abspath(os.path.join(root,f))
                    elif len(i2)>0:
                        num= int(i2[0])
                        ss[num]=os.path.abspath(root+'/'+f)
                    
                    dd=sorted(ss.items(),key=lambda item:item[0])
            else:
                #print('ok ......2')
                num=cc.sub('',f).replace('&nbsp','')
                ss[num]=os.path.abspath(root+'/'+f)
                dd=sorted(ss.items(),key=lambda item:item[0])

    if (regrex1 is None) and (research is not None):
        ddf={}
        for k,v in dd:
            for rsch in rs:
                if rsch in k:
                    ddf[k]=v

        if len(ddf)>0:
            dd=sorted(ddf.items(),key=lambda item:item[0])
        else:
            print('没有关于 "%s" 的文件'%research)

    if (regrex1 is None) and (startw is not None):
        dff={}
        for k,v in dd:
            if startw.match(k) is not None:
                dff[k]=v
                
        if len(dff)>0:
            dd=sorted(dff.items(),key=lambda item:item[0])
        else:
            print('没有关于 "%s" 的文件'%research)                
                
    return dd

def make_Mulu_content(files,m1=re.compile(r'^第\w{1,3}[编|篇]'),m2=re.compile(r'^第\w{1,3}章'),m3=re.compile(r'^第\w{1,3}节'),index=True):
    """
    files:为纯文本文件的列表。否则会出现错误。
    """
    table='table.txt'
    content="output.txt"

    if os.path.exists(table):
        os.remove(table)

    if os.path.exists(content):
        os.remove(content)

    tb=open(table,'w',encoding='utf8')
    ctt=open(content,"w",encoding='utf8')

    tb.write('''<div id="table-of-contents">
    <h2>Table of Contents</h2>
    <div id="text-table-of-contents">
    \n''')
    
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
        if i>0:
            tb.write('</li></ul>\n')
            pass
        tb.write('<ul><li><a href="#sec-%s-%s">%s</a>\n'%(i,txtName,ntitle))
        titles='''<h1 id="sec-%s-%s">%s</h1> \n'''%(i,txtName,ntitle)
        ctt.write(titles)

        muI=1
        mu1o=muI
        muII=1
        mu2o=muII
        muIII=1
        mu3o=muIII
        muIV=1
        for line in text:
            line=line.strip()
            #print(line)
            if m1.match(line) is not None:
                if muI>mu1o:
                    tb.write('</li></ul>\n')
                    #print('ok......1')
                    mu1o=muI
                ctt.write('</div>\n')
                tb.write('<ul><li><a href="#sec-%s-%s">%s</a>\n'%(muI,txtName,line))
                tb.write('\n')
                titles='''<div id="outline-container-%s" class="outline-%s">
                <h2 id="sec-%s-%s">%s</h2>\n'''%(muI,muI+1,muI,txtName,line)
                ctt.write(titles)
                muI=muI+1
            elif m2.match(line) is not None:
                if muII>mu2o:
                    tb.write('</li></ul>\n')
                    #print('ok...........2')
                    mu20=muII
                tb.write('<ul><li><a href="#sec-%s-%s-%s">%s</a>\n'%(muI,muII,txtName,line))
                titles='<div id="outline-container-%s-%s"><h3 id="sec-%s-%s-%s">%s</h4>\n'%(muI,muII,muI,muII,txtName,line)
                ctt.write(titles)
                #print(titles)
                muII=muII+1
            elif m3.match(line) is not None:
                if index:
                    tb.write('<ul><li><a  href="#sec-%s-%s-%s-%s">%s</a></li></ul>\n'%(muI,muII,muIII,txtName,line))
                    tb.write('\n')
                    titles='<div id="outline-container-%s-%s-%s"><h4 id="sec-%s-%s-%s-%s">%s</h4>\n '%(muI,muII,muIII,muI,muII,muIII,txtName,line)
                    ctt.write(titles)            
                    muIII=muIII+1
                    #print('ok.......3')

                else:
                    ctt.write(titles)


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
                #print(line)
                ctt.write(line)
            else:
                pass

        
        tb.write(r'</li></ul>')

    ctt.write('</div>')
    tb.write(r'</div></div>')    
    ctt.close()
    tb.close()
    tb=open(table,'r',encoding='utf8').read()
    ctt=open(content,'r',encoding='utf8').read()
    os.remove(table)
    os.remove(content)
    
    return tb,ctt

if __name__=="__main__":
   #tb,ct= make_Mulu_content(sys.argv[1])
   pass
