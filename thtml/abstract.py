#!/usr/bin/env python3
# -*-coding:utf-8-*-

import re
from thtml.utilth import (GFlist,make_Mulu_content)
from thtml.txt2html import _hh
def abstract(path,rc=re.compile('裁判要点\W*(.*?)\W*相关法条')):
    with open(path,encoding='utf8') as f:
        text=f.read()

    if rc is not None:
        cmmt='裁判要点:\n\n'+rc.findall(text)[0]+'\n\n'
    else:
        cmmt=text
    return cmmt

def ToabsFile(path,rc=re.compile('裁判要点\W*(.*?)\W*相关法条')):
    files=[]
    if isinstance(txtpath,list):
        files.extend(txtpath)
    elif txtpath is None:
        txtpath=os.getcwd()
        ss=GFlist(txtpath,regrex1=regrex1,research=Research,startw=Startw)
        files=[i[1] for i in ss]
    elif os.path.isdir(txtpath):
        ss=GFlist(txtpath,regrex1=regrex1,research=Research,startw=Startw)
        files=[i[1] for i in ss]
    tdir='temp_dir'
    if not os.path.exists(tdir):
        os.mkdir(tdir)

    for f in files:
        bn=os.path.basename(f)
        nf=os.path.join(tdir,bn)
        text=abstract(f,rc=rc)
        with open(nf,'w',encoding='utf8') as gf:
            gf.write(text)

    return

def Toabshtml(txtpath,rc=re.compile('裁判要点\W*(.*?)\W*相关法条'),regrex1=None,Research=None,index=True,Startw=None):
    
    files=[]
    htmlcode1=_hh(txtpath)
 
        
    if isinstance(txtpath,list):
        files.extend(txtpath)
    elif txtpath is None:
        txtpath=os.getcwd()
        ss=GFlist(txtpath,regrex1=regrex1,research=Research,startw=Startw)
        files=[i[1] for i in ss]
    elif os.path.isdir(txtpath):
        ss=GFlist(txtpath,regrex1=regrex1,research=Research,startw=Startw)
        files=[i[1] for i in ss]
    try:
        html=open(htmlName,'a',encoding='utf8')
        html.write(htmlcode1)
    except:
        html=open(htmlName,'a',encoding='gbk')
        html.write(htmlcode1)

    tem=open('temp21243.txt','a',encoding='utf8')
    
    for pf in files:
        tem.write(abstract(pf))
        tem.write('\n\n')

    tem.close()
    

    html.write('</body></html>')
    html.close()
    print("\n转换成功,保存在%s"%htmlName)        
    
