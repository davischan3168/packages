#!/usr/bin/env python3
# -*-coding:utf-8-*-
import os
import sys
import re
import util.ch2num as ut
from mswdoc.docx2txt import msdoc2text

cc=re.compile('\W*')
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
    pathlist=[]
    if isinstance(path,list):
        pathlist.extend(path)
    elif isinstance(path,str):
        pathlist.append(path)
        
    ss={}
    for path in pathlist:
        for root,ds,fs in os.walk(path):
            for f in fs:
                #print(f)
                if regrex1 is not None:
                    #print('ok....1')
                    if os.path.splitext(f)[1].lower() in ['.txt','.doc','.docx']:
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
#######################################3
def GFlistv1(path,\
                 regrex1=None,\
                 search=None,\
                 startw=None,\
                 exclude=None,\
                 res=False):
    """
    regrex1:为re.compile 的类型，选取相应的关键字作为排序
    startw:re.compile类型，选取以某个字为开头
    search: str or list
    res:True or False,是否倒序
    """
    rs=[]
    if isinstance(search ,list):
        rs.extend(search)
    elif isinstance(search ,str):
        rs.append(search)

    file_list=[]
    path_list=[]        
    if isinstance(path,list):
        for f in path:
            if os.path.isfile(f):
                file_list.append(f)
            elif os.path.isdir(f):
                path_list.append(f)
            
    elif os.path.isfile(path):
        file_list.append(path)
    elif os.path.isdir(path):
        path_list.append(path)
    elif path is None:
        txtpath=os.getcwd()
        
    excl=[]
    if isinstance(exclude ,list):
        excl.extend(exclude)
    elif isinstance(exclude,str):
        excl.append(exclude)          
        
    for path in path_list:
        for root,ds,fs in os.walk(path):
            for f in fs:
                file_list.append(os.path.abspath(os.path.join(root,f)))

    
    only_one=set()
    fls=[]
    word=re.compile(r'[\u4e00-\u9fa5]+')
    for ff in file_list:
        aa=os.path.basename(ff)
        nwd=''.join(word.findall(aa))
        if nwd not in only_one:
            only_one.add(nwd)
            fls.append(ff)

    if len(fls)>0:
        file_list=fls
            
    temff=set()
    if exclude is not None:
        for ff in file_list:
            for ex in excl:
                aa=os.path.basename(ff)
                if ex in aa:
                    temff.add(ff)
    

    File_tmp=[f for f in file_list if f not in temff]

    Final_list={}
    for f in File_tmp:
        ff=os.path.basename(f)
        if regrex1 is not None:
            if splitext(ff)[1].lower() in ['.txt','.doc','.docx']:
                i1=[i for i in regrex1.findall(ff) if len(i)>0]
                i2=[i for i in regrex1.findall(ut.ChNumToArab(ff)) if len(i)>0]
                if len(i1)>0:
                    num1=int(i1[0])
                    Final_list[num1]=f
                elif len(i2)>0:
                    num1= int(i2[0])
                    Final_list[num1]=f
        else:
            num1=cc.sub('',ff).replace('&nbsp','')
            Final_list[num1]=f
        
    if search is not None:
        Tem={}
        for k,v in Final_list.items():
            for rsch in rs:
                if rsch in os.path.basename(v):
                    Tem[k]=v
        if len(Tem)>0:
            Final_list=Tem
        else:
            print('没有关于 "%s" 的文件'%search)
            sys.exit()

    if startw is not None:
        dff={}
        for k,v in Final_list.items():
            if startw.match(basename(v)) is not None:
                #print('start word ...',v)
                dff[k]=v
        if len(dff)>0:
            Final_list=dff
        else:
            print('没有符合的文件')
            sys.exit()
            
    Final_files=[]
    if len(Final_list)>0:
        Final=sorted(Final_list.items(),key=lambda item:item[0],reverse=res)
        Final_files=[i[1] for i in Final]
    return Final_files
#############################################
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
        tem=os.path.splitext(txtName)
        if tem[1].lower() in ['.txt']:
            try:
                txt=open(txtName,'r',encoding='utf8')
                text=txt.readlines()
            except:
                txt=open(txtName,'r',encoding='gbk')
                text=txt.readlines()            
            txt.close()
        elif tem[1].lower() in ['.doc','.docx']:
            text=msdoc2text(txtName)
            tl=text.split('\n')
            text=[i.strip() for i in tl if len(i.strip())>0]
            
        text=[x.strip() for x in text]
        s='\n'.join(text)
        ss=re.sub(r'\n{1,}',r'\n\n',s)
        text=ss.splitlines()

        ntitle=os.path.splitext(os.path.basename(txtName))[0]#[2:]
        ntitle=cc.sub('',ntitle)
        #print('the name for file %s,%s'%(ntitle,txtName))
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
        tmplist=[]
        tem=''
        for line in text:
            line=line.strip()
            
            if m2.match(tem):
                if m2.match(line):
                    #l1='</ul></li>\n'
                    tb.write('</ul></li>\n')
                    ctt.write('</div>\n')
                    #print('2 t0 2 title %s next title %s....'%(tem,line))
                    #print(l1)
                elif m1.match(line):
                    #l2='</ul></li>\n</ul></li>\n'
                    tb.write('</ul></li>\n</ul></li>\n')
                    ctt.write('</div>\n</div>')
                    #print('2 to 1 title %s next title %s....'%(tem,line))
                    #print('title 2 next title 1....')
                    
            elif m1.match(tem):
                if m1.match(line):
                    tb.write('</ul></li>\n')
                    #l3='</ul></li>\n'
                    ctt.write('</div>\n')
                    #print(l3,'1 to 2')
                    pass

            elif m3.match(tem):
                if m1.match(line):
                    tb.write('</ul></li>\n</ul></li>\n')
                    ctt.write('</div>\n</div></div>')
                    #print('3 to 1 title %s next title %s....'%(tem,line))
                    #print('title 3 next title 1....')
                elif m2.match(line):
                    tb.write('</ul></li>\n')
                    ctt.write('</div>\n</div>')
                    #print('3 to 2 title %s next title %s....'%(tem,line))
                    #print('title 3 next title 2....')
                elif m3.match(line):
                    ctt.write('</div>\n')
                    
            if m1.match(line) is not None:
                
                tb.write('<ul><li><a href="#sec-%s-%s">%s</a>\n'%(muI,txtName,line))
                #tb.write('\n')
                titles='''<div id="outline-container-%s" class="outline-%s">
                <h2 id="sec-%s-%s">%s</h2>\n'''%(muI,muI+1,muI,txtName,line)
                ctt.write(titles)
                tem=line
                muI += 1
            elif m2.match(line) is not None:
                tb.write('<ul><li><a href="#sec-%s-%s-%s">%s</a>\n'%(muI,muII,txtName,line))
                titles='<div id="outline-container-%s-%s"><h3 id="sec-%s-%s-%s">%s</h4>\n'%(muI,muII,muI,muII,txtName,line)
                ctt.write(titles)
                tem=line
                muII +=1
            elif m3.match(line) is not None:
                if index:
                    tb.write('<ul><li><a  href="#sec-%s-%s-%s-%s">%s</a></li></ul>\n'%(muI,muII,muIII,txtName,line))
                    tb.write('\n')
                    titles='<div id="outline-container-%s-%s-%s"><h4 id="sec-%s-%s-%s-%s">%s</h4>\n '%(muI,muII,muIII,muI,muII,muIII,txtName,line)
                    ctt.write(titles)            
                    muIII=muIII+1
                    tem=line
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
###############################
def make_Mulu_contentv1(files,m1=re.compile(r'^第\w{1,3}[编|篇]'),m2=re.compile(r'^第\w{1,3}章'),m3=re.compile(r'^第\w{1,3}节'),index=True):
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
        tem=os.path.splitext(txtName)
        if tem[1].lower() in ['.txt']:
            try:
                txt=open(txtName,'r',encoding='utf8')
                text=txt.readlines()
            except:
                txt=open(txtName,'r',encoding='gbk')
                text=txt.readlines()            
            txt.close()
        elif tem[1].lower() in ['.doc','.docx']:
            text=msdoc2text(txtName)
            tl=text.split('\n')
            text=[i.strip() for i in tl if len(i.strip())>0]
            
        text=[x.strip() for x in text]
        s='\n'.join(text)
        ss=re.sub(r'\n{1,}',r'\n\n',s)
        text=ss.splitlines()

        ntitle=os.path.splitext(os.path.basename(txtName))[0]#[2:]
        ntitle=cc.sub('',ntitle)
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
