#!/usr/bin/env python3
# -*-coding:utf-8-*-

import sys,os,time
import re
from thml.util import make_Mulu_content

cstr=['，','。','？','！','；','：']
#temp = "想做/ 兼_职/学生_/ 的 、加,我Q：  1 5.  8 0. ！！？？  8 6 。0.  2。 3     有,惊,喜,哦"  
#temp = temp.decode("utf8")  
#string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),temp)

div_style=r'<div style="word-spacing:5px;line-height:1.5">'
htmlcode='''<html>
<meta http-equiv="Content-Type" content="text/html; charset=%s" />
<body bgcolor="#C7EDF0">
<title> %s </title>'''

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
def _mytitle(txtName):

    if isinstance(txtName,list):
        mytitle='My Html File'
    elif os.path.isfile(txtName):
        mytitle=os.path.basename(os.path.splitext(txtName)[0])
    elif os.path.isdir(txtName):
        mytitle=os.path.basename(txtName)
    else:
        mytitle='My Html File'
    return mytitle
def _hh(txtName):
    if sys.platform.startswith('win'):
        htmlcode1=htmlcode%('utf8',_mytitle(txtName))
    elif sys.platform in ['linux']:
        htmlcode1=htmlcode%('utf8',_mytitle(txtName))
    return htmlcode1
    
##########################################3
def txt2htmlv1(txtName,m1=re.compile(r'^第\w{1,3}[编|篇]'),m2=re.compile(r'^第\w{1,3}章'),m3=re.compile(r'^第\w{1,3}节'),index=True):
    """
    txtName:文件的名称（含所在的文件夹）
    index：  True,将第四节的列入目录
             False,不含第四节的目录
    ---------------
    在python运行目录下生产一份html文件。
    """
    files=[]
    htmlcode1=_hh(txtName)

    if isinstance(txtName,str):
        files.append(txtName)
    elif isinstance(txtName,list):
        files.extend(txtName)

    htmlName="outputtxt.html"
    
    if os.path.exists(htmlName):
        os.remove(htmlName)

    #####################
    '''
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
            print(line)
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
                print(titles)
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

    tb=open(table,'r',encoding='utf8')
    ctt=open(content,'r',encoding='utf8')
    '''
    ###############
    tb,ctt=
    if os.path.exists(htmlName):
        os.remove(htmlName)    
    try:
        html=open(htmlName,'a',encoding='utf8')
        html.write(htmlcode1)
        html.write(tb)
        html.write(ctt)
    except:
        html=open(htmlName,'a',encoding='gbk')
        html.write(htmlcode1)
        html.write(tb)
        html.write(ctt)
        
    #tb.close()
    #ctt.close()
    html.write('</body></html>')
    html.close()
    print("\n转换成功,保存在%s"%htmlName)
    #os.remove(table)
    #os.remove(content)
    return
###############################################################
def txt2html_inonefile(txtName,m1=re.compile(r'^第\w{1,3}[编|篇]'),m2=re.compile(r'^第\w{1,3}章'),m3=re.compile(r'^第\w{1,3}节'),index=True):
    """
    txtName:文件的名称（含所在的文件夹）
    index：  True,将第四节的列入目录
             False,不含第四节的目录
    ---------------
    在txtName文件目录下生产一html文件。
    """
    files=[]
    htmlcode1=_hh(txtName)
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

    ############
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
            print(line)
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
                print(titles)
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
    ###################
    ctt.close()
    tb.close()    

    tb=open(table,'r',encoding='utf8')
    ctt=open(content,'r',encoding='utf8')
    if os.path.exists(htmlName):
        os.remove(htmlName)
    try:
        html=open(htmlName,'w',encoding='utf8')
        html.write(htmlcode1)
        html.write(tb.read())
        html.write(ctt.read())
    except:
        html=open(htmlName,'w',encoding='gbk')
        html.write(htmlcode1)
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
###################################################
def txt2html_odir(txtName,m1=re.compile(r'^第\w{1,3}[编|篇]'),m2=re.compile(r'^第\w{1,3}章'),m3=re.compile(r'^第\w{1,3}节'),index=False):
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
            txt2html_inonefile(f,m1=m1,m2=m2,m3=m3,index=index)
    else:
        txt2html_inonefile(txtName,m1=m1,m2=m2,m3=m3,index=index)
    return
####################################################
def txt2htmldir(path=None,func=txt2htmlv1,px='\d{1,3}',index=False):
    """
    path:文件夹的名称,若没有输入参数，则默认为None，即当前目录。
    func:txt2html_odir,形成一个个单独的文件，文件名与源文件相同，并保存在源文件的目录下。
        :txt2htmlv1，合并成一个文件，文件保存在当前工作目录下，输出为output.html。
    px: 按预先定义的方式进行排序
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

    if len(dirset)>0:
        ss={}
        try:
            for i in dirset:
                dd=re.findall(px,i)
                num=int([j for j in dd if len(j)>0][0])
                ss[num]=i
            dds=sorted(ss.items(),key=lambda item:item[0])
            dirsett=[]
            for i in dds:
                dirsett.append(i[1])
            #print(dirset)
        except Exception as e:
            print(e)
    if len(dirset)==len(dirsett):
        func(dirsett,index=index)
    else:
        func(dirset,index=index)
    return
##########################
def txt2htmlall(pathname,mformat='AIO',m1=re.compile(r'^第\w{1,3}[编|篇]'),m2=re.compile(r'^第\w{1,3}章'),m3=re.compile(r'^第\w{1,3}节'),index=True,Current=False):
    """
    pathname:file or 
    
    mformat:AIO：ALL In One,表示将目录下的所有文件加入到一个thml文件中
            OBO:One By One ,表示将目录下的文件生成对应一个一个的thml文件

    Current:与源文件在同一目录之下
            
    """
    if os.path.isfile(pathname):
        if pathname.endswith('.txt'):
            if Current:
                txt2html_odir(tt,m1=m1,m2=m2,m3=m3,index=index)
            else:
                txt2htmlv1(pathname,m1=m1,m2=m2,m3=m3,index=index)
    elif os.path.isdir(pathname):
        for root,dirs,files in os.walk(pathname):
            txts={}
            for f in files:
                if f.endswith('.txt'):
                    print(f)
                    pf=os.path.join(root,f)
                    txts[f]=pf
        if len(txts)>0:
            dds=sorted(txts.items(),key=lambda item:item[0])
            tt=[]
            for i in dds:
                tt.append(i[1])
            if mformat=='AIO':
                txt2htmlv1(tt,m1=m1,m2=m2,m3=m3,index=index)

            elif mformat=='OBO':
                txt2html_odir(tt,m1=m1,m2=m2,m3=m3,index=index)
            else:
                print('Input right parameter for mformat.... AIO or OBO')
                sys.exit()
    else:
        print('Input right parameter for path name.... file or dir')
        sys.exit()

    return


if __name__=="__main__":
    #txt2htmlv1(sys.argv[1])
    #txt2htm(sys.argv[1])
    #txt2htmldir(sys.argv[1],func=txt2htmlv1,index=False)
    #txt2html_inonefile(sys.argv[1])
    #txt2html_odir(sys.argv[1])
    txt2htmlall(sys.argv[1],mformat='OBO')
