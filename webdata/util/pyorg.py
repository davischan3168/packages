# encoding:utf-8
##
# 实现批量修改文件夹下说有文件的名称，循环所有的文件夹
# 
##
import os,re
import sys

def write_file(path,r):
    #if 'win'in 
    f=open(path,'a',encoding='utf8')
    f.write(r)
    f.close()
    return
import datetime as dt
import urllib.parse

date=dt.datetime.strftime(dt.datetime.today(),"%Y-%m-%d %a %H:%M")

styles="""
<meta  http-equiv="Content-Type" content="text/html;charset=utf-8" />
<head>
<body bgcolor="#C7EDF0">
<title>%s</title>
<!-- %s -->"""
    
titles='''
#+TITLE: Change to Name
#+AUTHOR: Davis Chen
#+DATE: today
#+EMAIL: chenzuliang@163.com
#+DESCRIPTION: the page description, e.g. for the XHTML meta tag
#+KEYWORDS: the page keywords, e.g. for the XHTML meta tag
#+LANGUAGE: language for HTML, e.g. ‘en’ (org-export-default-language)
#+TEXT: Some descriptive text to be inserted at the beginning.
#+STYLE: <link rel="stylesheet" type="text/css" href="./worg.css" />
#+TEXT: Several lines may be given.
#+OPTIONS: H:5 num:t toc:t \\n:nil @:t ::t |:t ^:t f:t TeX:t ...
#+LINK_UP: the ``up'' link of an exported page
#+LINK_HOME: the ``home'' link of an exported page
#+TODO: TODO(t!/@) INPROGRESS(n!/@) WAITING(w!/@)| DONE(d!/@) CANCEL(c!/@)
#+TAGS: @office(o) @home(h) @traffic(t)
#+TAGS: computer(c) nocomputer(n) either(e)
#+TAGS: immediately(i) wait(w) action(a)
'''
def delet_file(pf):
    for (pf,dirs,files) in os.walk(pf):
        for old in files:
            if '_content.txt' in os.path.split(old)[1]:
                rmfile=os.path.join(pf,old)
                os.remove(rmfile)

# 读取目录下的文件,形成org文件
def Topyorg(pf):
    #global titles
    pfname=pf.replace('/','')
    
    with open(pfname+'_content.org','w') as f:
        f.writelines(titles)
        f.flush()
    if os.path.isdir(pf):

        if pf.endswith('/'):
            pf=pf[:-1]

        for root,dirs,files in os.walk(pf):
            rname=os.path.basename(root)
            dline= '- d [[./'+root+']['+rname+']]\n'
            try:
                if not rname.startswith('.'):
                    if not rname.startswith('_'):
                        write_file(pfname+'_content.org',dline)
                        #print(dline)
            except Exception as e:
                print(e)
            #"""
            for old in files:
                files1=os.path.splitext(old)
                #if (files1[1] not in ['.tmp','.tex','.bat','.el','.sh','.lnk','.ini','.py','.org','.gss','._gs','.gsl','.cls'])and  (files1[0] not in ['Thumbs']) and (re.match(r'^[(\~\$)|(\~)]',files[0]) is None) :
                #过滤临时文件
                if (files1[1] not in ['.tmp','.tex','.bat','.el','.sh','.lnk','.ini','.py','.org','.gss','._gs','.gsl','.cls'])and  (files1[0] not in ['Thumbs']) and (files[0].startswith('~') is False) :
                    filename=files1[0]
                    #fpath=os.path.join(root,old)
                    fpath=root+'/'+old
                    line='''  - [ ]  [[./%s][%s]]\n'''%(fpath,filename)
                    try:
                        write_file(pfname+'_content.org',line)
                        #print(line)
                    except Exception as e:
                        print(e)
    return

def Topyhtml(pf):
    pfname=pf.replace('/','')
    htmlf=pfname+'_content.html'
    if os.path.exists(htmlf):
        os.remove(htmlf)
    style0=styles%(pfname,date)
    with open(htmlf,'w') as f:
        f.writelines(style0)
        f.write('<div id="content"> \n')
        f.write('<h1 class="title">%s</h1>\n<ul class="org-ul">\n'%pfname)

        f.flush()
    if os.path.isdir(pf):

        if pf.endswith('/'):
            pf=pf[:-1]

        for root,dirs,files in os.walk(pf):
            rname=os.path.basename(root)
            dline= '\n<li>- d <a href=%s>%s</a> \n</li>\n'%(root,rname)
            try:
                if not rname.startswith('.'):
                    if not rname.startswith('_'):
                        write_file(htmlf,dline)
                        #print(dline)
                        write_file(htmlf,'<ul class="org-ul">')
            except Exception as e:
                print(e)
            for old in files:
                files1=os.path.splitext(old)
                #if (files1[1] not in ['.tmp','.tex','.bat','.el','.sh','.lnk','.ini','.py','.org','.gss','._gs','.gsl','.cls']) and  (re.match(r'^[(\~\$)|(\~)]',files[0]) is None) and  (files1[0] not in ['Thumbs']):
                #过滤临时文件
                if (files1[1] not in ['.log','.tmp','.tex','.bat','.el','.sh','.lnk','.ini','.py','.org','.gss','._gs','.gsl','.cls','.pyc'])and (files1[0].startswith('~') is False) and (files1[0].startswith('#') is False):
                    filename=files1[0]
                    #fpath=root+'\\'+old
                    fpath=os.path.join(root,old)
                    fpath=urllib.parse.quote(fpath)
                    line='<li><code>[&#xa0;]</code> <a href=%s>%s</a>\n</li>'%(fpath,filename)
                    try:
                        write_file(htmlf,line)
                        #print(line)
                    except Exception as e:
                        print(e)
            write_file(htmlf,r"</ul>"+'\n')
    write_file(htmlf,'</div>\n</body>\n</html>')
            
    return    

if __name__=="__main__":
    pf=sys.argv[1]
    #Topyorg(pf)
    Topyhtml(pf)
