#!/usr/bin/env python3
# -*-coding:utf-8-*-

import sys,os,time
import re

title=r"""
\documentclass[myxecjk,msize]{gdhsarticle}%{kindle}
\iffalse
\geometry{paperheight=297mm,%
paperwidth=210mm,
left=2.3cm,%
right=2.3cm,%
top=2.1cm,%
bottom=2.1cm,%
headheight=0cm,%
headsep=0cm,
footskip=0cm
}%
\fi
\linespacing{1.52}%
\pagestyle{empty}
%\include{setting}
%\include{pagesign}
\setlength{\unitlength}{1cm}
\parindent=2em
\definecolor{defaultbgcolor-0}{RGB}{199,237,204}%for eye
\pagecolor{defaultbgcolor-0}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%以下正文%%%%%%%%%%%%
\begin{document}
"""

kindle=r"""
\documentclass[myxecjk,msize]{gdhsarticle}%{kindle}
\iffalse
\geometry{paperheight=297mm,%
paperwidth=210mm,
left=2.3cm,%
right=2.3cm,%
top=2.1cm,%
bottom=2.1cm,%
headheight=0cm,%
headsep=0cm,
footskip=0cm
}%
\fi
\linespacing{1.52}%
\pagestyle{empty}
%\include{setting}
%\include{pagesign}
\setlength{\unitlength}{1cm}
\parindent=2em
\definecolor{defaultbgcolor-0}{RGB}{199,237,204}%for eye
\pagecolor{defaultbgcolor-0}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%以下正文%%%%%%%%%%%%
\begin{document}
"""

end=r"""\end{document}"""
latexs={'article':title,'kindle':kindle}

def _write_file(path,r):
    f=open(path,'a',encoding='utf8')
    f.write(r)
    f.flush()
    return
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
def _Readfile(inpf,tc,tc1,tc2):
    try:
        con=open(inpf,encoding='utf-8')
        content=con.readlines()
    except:
        con=open(inpf,encoding='gbk')
        content=con.readlines()        
    con.close()
    
    listd=[]
    if tc is None:
        trec=re.compile(r'^第\w{1,3}篇')
    else:
        trec=tc
    if tc1 is None:
        trec1=re.compile(r'^第\w{1,3}章')
    else:
        trec1=tc1
    if tc2 is None:
        trec2=re.compile(r'^第\w{1,3}节')
    else:
        trec2=tc2
        
    for line in content:
        line=line.strip()
        if trec.match(line) is not None:
            line=r'\section{%s}'%line+'\n\n'
            listd.append(line)
        elif trec1.match(line) is not None:
            line=r'\section{%s}'%line+'\n\n'
            listd.append(line)

        elif trec2.match(line) is not None:
            line=r'\subsection{%s}'%line+'\n\n'
            listd.append(line)            
        
        elif len(line)>0:
            if '%' in line:
                line=re.sub(r'%{1,}','\%',line)+'\n\n'
                #print(line)
                #write_file(outpath,line)
                listd.append(line)
            else:
                line=line+'\n\n'
                #print(line)
                #write_file(outpath,line)
                listd.append(line)
    return listd
    
def TTlatex(inpf,oupf='OutputLatexPdf',mtype='article',tc=None,tc1=None,tc2=None):
    """
    inpf:INput Document for example txt docment
    -----------
    oupf: 输出的文件名称，不包含扩展名
    mtype:article,kindle
    """

    outpath=oupf+'.tex'

    if os.path.exists(outpath):
        os.remove(outpath)
    
    with open(outpath,'a') as f:
        f.writelines(latexs[mtype])
        f.flush()

    if os.path.isfile(inpf):
        try:
            listd=_Readfile(inpf,tc,tc1,tc2)
            conn=''.join(listd)
            #print(conn)
            #if len(conn)>0:
            _write_file(outpath,conn)
            #else:
            #    print('conn is empty.')
            _write_file(outpath,end)
            os.system('xelatex -no-pdf -interaction=nonstopmode %s' %outpath)
            os.system('xelatex -interaction=nonstopmode %s' %outpath)
            _removef(outpath)        
        except Exception as e:
            print(e)
            pass
    elif isinstance(inpf,list):
        try:
            for li in inpf:
                li=li.strip().replace('\n','\n\n')
                _write_file(outpath,conn)
            _write_file(outpath,end)
            os.system('xelatex -no-pdf -interaction=nonstopmode %s' %outpath)
            os.system('xelatex -interaction=nonstopmode %s' %outpath)
            _removef(outpath)
        except Exception as e:
            print(e)
            pass
            
    

    return

if __name__=="__main__":
    #Sql2Pdf(sys.argv[1])
    #Guwen2Pdf_book(sys.argv[1])
    TTlatex(sys.argv[1])

    
    
