#!/usr/bin/env python3
# -*-coding:utf-8-*-
import os
import sys
import re

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
   tb,ct= make_Mulu_content(sys.argv[1])
