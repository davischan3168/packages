#!/usr/bin/env python3
# -*-coding:utf-8-*-
import sys
import re
import os
import time
from xpinyin import  Pinyin
import subprocess
import util.ch2num as ut
p=Pinyin()

title=r"""
\documentclass[myxecjk,msize]{gdhsarticle}%{kindle}
\iffalse
\geometry{paperheight=297mm,%
paperwidth=210mm,
left=2.3cm,%
right=2.3cm,%
t..`op=2.1cm,%
bottom=2.1cm,%
headheight=0cm,%
headsep=0cm,
footskip=0cm
}%
\fi
\linespacing{1.52}%
\pagestyle{empty}
\usepackage{xpinyin}
\setmainfont{CMU Serif}
\setCJKmainfont{SimSun}
%\include{setting}
%\include{pagesign}
\setlength{\unitlength}{1cm}
\parindent=2em
\definecolor{defaultbgcolor-0}{RGB}{199,237,204}%for eye
\pagecolor{defaultbgcolor-0}
%`.`%%%%%%%%%%%%%%%%%%%%%%%%%%%%%以下正文%%%%%%%%%%%%
\begin{document}
"""

kindle=r"""
\documentclass[myxecjk,msize]{gdhsarticle}%{kindle}
\geometry{paperwidth=9.2cm,% 
paperheight=12.4cm, width=9cm, 
height=12cm,top=0.2cm,bottom=0.4cm,
left=0.2cm,right=0.2cm,foot=0cm, nohead,nofoot}%
\linespacing{1.52}%
\pagestyle{empty}
\usepackage{xpinyin}
\setmainfont{CMU Serif}
\setCJKmainfont{SimSun}
%\include{setting}
%\include{pagesign}
\setlength{\unitlength}{1cm}
\parindent=2em
\definecolor{defaultbgcolor-0}{RGB}{199,237,204}%for eye
%\pagecolor{defaultbgcolor-0}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%以下正文%%%%%%%%%%%%
\begin{document}
\setlength{\parindent}{0em}
%\begin{pinyinscope}
"""

pad=r"""
\documentclass[myxecjk,msize]{gdhsarticle}%{kindle}
\geometry{paperwidth=19cm,% 
paperheight=26cm, 
left=2.5cm,%
right=2.5cm,%
top=2cm,%
bottom=2cm,%
headheight=0cm,%
headsep=0cm,
footskip=0cm
}%
\linespacing{1.52}%
\pagestyle{empty}
\usepackage{xpinyin}
\setmainfont{CMU Serif}
\setCJKmainfont{SimSun}
%\include{setting}
%\include{pagesign}
\setlength{\unitlength}{1cm}
\parindent=2em
\definecolor{defaultbgcolor-0}{RGB}{199,237,204}%for eye
\pagecolor{defaultbgcolor-0}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%以下正文%%%%%%%%%%%%
\begin{document}
\setlength{\parindent}{0em}
%\begin{pinyinscope}
"""

end="""%\end{pinyinscope}
\end{document}"""
latexs={'article':title,'kindle':kindle,'pad':pad}
section='\section{%s}'

def _removef(outpath):
    lsd=['.aux','.log','.out','.xdv','.tex']
    base=os.path.split(outpath)
    basename=os.path.splitext(base[1])[0]
    for ex in lsd:
        try:
            mybsn=basename+ex
            path=os.path.join(base[0],mybsn)
            print(path)
            os.remove(path)
        except Exception as e:
            pass
    return

def Singal_File(inFile,mtype='article',pyin=False):
    #dirname=os.path.dirname(inFile)
    path=os.path.abspath(inFile)
    name=os.path.basename(path).split('.')[0].replace('&nbsp','')
    outFile=p.get_initials(os.path.splitext(path)[0],'')+'.tex'
    
    f=open(inFile,'r',encoding='utf8')
    content=f.readlines()
    f.close()

    cts=[li.strip() for li in content if len(li.strip())>0]
    cts='\n\n'.join(cts).replace('&nbsp','')
    cts=re.sub(r'%',r'\%',cts)

    fl=open(outFile,'w',encoding='utf8')
    fl.write(latexs[mtype]+'\n\n')
    fl.write(section%name)
    if pyin:
        fl.write('\n\n'+r'\begin{pinyinscope}')
    fl.write('\n\n'+cts+'\n\n')
    if pyin:
        fl.write('\n\n'+r'\end{pinyinscope}')  
    fl.write(end)
    fl.close()
    os.system('xelatex -no-pdf -interaction=nonstopmode %s' %oOutFile)
    os.system('xelatex -interaction=nonstopmode %s' %oOutFile)
    _removef(outpath)
    return
###########################################
def Singal_input(InFile,pyin=False):
    path=os.path.abspath(InFile)
    dname=os.path.dirname(path)
    
    name=os.path.splitext(os.path.basename(path))[0].replace('_','').replace(' ','').replace('·','').replace('，','').replace('&nbsp','').replace(';','').replace('〈','').replace('〉','').strip()
    #print(name)
    if len(name)<12:
        outFile=p.get_pinyin(name)+'.tex'
    else:
        outFile=p.get_initials(name)+'.tex'
    outFile=outFile.replace('、','').replace('&nbsp','').replace(':','').replace('-','').replace('：','').replace('（','').replace('）','').replace('《','').replace('》','').replace('—','')
    if sys.platform.startswith('win'):
        rt1=dname.split('\\')
        dname='/'.join(rt1)
    outFile2=dname+'/'+outFile
    
    f=open(InFile,'r',encoding='utf8')
    content=f.readlines()
    f.close()

    cts=[]
    for li in content:
        if li.strip() in ['裁判要点','基本案情','裁判结果','裁判理由','相关法条','【关键词】','【诉讼过程】','【基本案情】','【抗辩理由】','【案件结果】','【要旨】','【指导意义】','【相关法律规定】']:
            cts.append(r'\subsection{%s}'%li.strip())
        else:
            nl=li.strip()
            if len(nl)>0:
                cts.append(nl)
    cts='\n\n'.join(cts).replace('&nbsp','')
    #cts=re.sub(r'\\',r'/',cts)
    cts=cts.replace('#','\#').replace('&','\&').replace('$','\$').replace('|','\|').replace('_','\_')
    cts=re.sub(r'%',r'\%',cts)
    
    fl=open(outFile2,'w',encoding='utf8')
    fl.write(section%name)
    if pyin:
        fl.write('\n\n'+r'\begin{pinyinscope}')
    fl.write('\n\n'+cts+'\n\n')
    if pyin:
        fl.write('\n\n'+r'\end{pinyinscope}')  
    fl.close()
    return outFile2
######################################
def Mains(DirName,OutFile='Main',mtype='pad',num=True,pyin=False,Total='max'):
    txt_files={}
    
    for root,dirs,files in os.walk(DirName):
        for f in files:
            if os.path.splitext(f)[1] in ['.txt']:
                if sys.platform.startswith('win'):
                    rt1=root.split('\\')
                    root='/'.join(rt1)
                pf=root+'/'+f
                #print(pf)
                if num:
                    fnum=re.findall('第(\d*)批',ut.ChNumToArab(f))
                    if len(fnum)==0:
                         txt_files[f]=Singal_input(pf,pyin)
                    else:
                         txt_files[fnum[0].zfill(3)]=Singal_input(pf,pyin)
                else:
                    txt_files[f]=Singal_input(pf,pyin)

                
    if len(txt_files)>0:
        txt_files1=sorted(txt_files.items(),key=lambda txt_files:txt_files[0])

    #print(txt_files1)
    ##########################3
    if Total=='max':
        OutFile1=OutFile+'.tex'
        fl=open(OutFile1,'w',encoding='utf8')
        fl.write(latexs[mtype]+'\n\n')        
        for f in txt_files1:
            fl.write('\input{%s}'%f[1])
            fl.write(r'\newpage')
            #fl.write('\n\n')
        
        fl.write(end)
        fl.close()
        os.system('xelatex -no-pdf -interaction=nonstopmode %s' %OutFile1)
        os.system('xelatex -interaction=nonstopmode %s' %OutFile1)
        #cmd=subprocess.Popen('xelatex -no-pdf -interaction=nonstopmode %s'%OutFile1,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
        #cmd=subprocess.Popen('xelatex -interaction=nonstopmode %s'%OutFile1,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)        
        #_removef(OutFile1)
        ###########################3
    elif isinstance(Total,int):
        for f in txt_files1:
            txp=[txt_files1[i:i+Total] for i in range(0,len(txt_files),Total)]
            fn=1
            for ff in txp:
                OutFile1=OutFile+'_%s.tex'%str(fn).zfill(2)
                fl=open(OutFile1,'w',encoding='utf8')
                fl.write(latexs[mtype]+'\n\n')
                for f in ff:
                    fl.write('\input{%s}'%f[1])
                    fl.write(r'\newpage')
                    #fl.write('\n\n')
        
                fl.write(end)
                fl.close()
                os.system('xelatex -no-pdf -interaction=nonstopmode %s' %OutFile1)
                os.system('xelatex -interaction=nonstopmode %s' %OutFile1)
                #cmd=subprocess.Popen('xelatex -no-pdf -interaction=nonstopmode %s'%OutFile1,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
                #cmd=subprocess.Popen('xelatex -interaction=nonstopmode %s'%OutFile1,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
                _removef(OutFile1)
                
                fn +=1
        
    else:
        print('Total is max out int, please input the right parameter.')


    for root,dirs,files in os.walk(DirName):
        for f in files:
            if os.path.splitext(f)[1] in ['.tex']:
                os.remove('%s'%os.path.abspath(root+'/'+f))
                pass

    return

    
    

if __name__=="__main__":
    #d=Singal_File(sys.argv[1])
    d=Mains(sys.argv[1],num=False)
    #d=Singal_input(sys.argv[1],pyin=True)
