#!/usr/bin/env python3
# -*-coding:utf-8-*-
import sys,os
import requests
import lxml.html
from bs4 import BeautifulSoup
from io import StringIO
import time,re
from webdata.util.hds import user_agent as hds
import webdata as wd
#from webdata.util.myenum import tonum

def gettxt(url):
    r=requests.get(url,headers=hds())
    txt=r.content.decode('utf8')
    html=lxml.html.parse(StringIO(txt))
    title=html.xpath('//div[@class="title"]//text()')
    html=html.xpath('//div[@id="zoom"]//text()')
    text='\n'.join(html)
    tza=title[0]+'\n\n'+text
    return tza

def gettxt_soup(url):
    r=requests.get(url,headers=hds())
    txt=r.content.decode('utf8')
    html=lxml.html.parse(StringIO(txt))
    title=html.xpath('//div[@class="title"]//text()')
    soup=BeautifulSoup(r.text,'lxml')
    df=soup.find(id='zoom')
    dfs=df.findAll('p')
    
    if len(dfs)>0:
        texts=[]
        for i in dfs:
            texts.append(i.text)
        text=''.join(texts)
    else:
        htmll=html.xpath('//div[@id="zoom"]//text()')
        text='\n'.join(htmll)
    
    tza=title[0]+'\n\n'+text
    return tza    

def getlist(url,page=5):
    r=requests.get(url,headers=hds())
    txt=r.content.decode('utf8')
    #print(txt)
    html=lxml.html.parse(StringIO(txt))
    lis=html.xpath('//div[@id="container"]/div[@class="sec_list"]/ul/li')
    datasets={}
    for li in lis:
        name=re.sub(r'\s*','',li.xpath('a/text()')[0].strip())
        name=name.replace('“','').replace('”','')
        date=li.xpath('i/text()')[0]
        name=date+'_'+name
        print(name)
        href='http://www.court.gov.cn'+li.xpath('a/@href')[0]
        #if name.endswith('指导性案例'):
        datasets[name]=href

    for i in range(2,page+1):
        urll=url+'?page=%s'%i
        r=requests.get(urll,headers=hds())
        txt=r.content.decode('utf8')
        #print(txt)
        html=lxml.html.parse(StringIO(txt))
        lis=html.xpath('//div[@id="container"]/div[@class="sec_list"]/ul/li')
        for li in lis:
            name=re.sub(r'\s*','',li.xpath('a/text()')[0].strip())
            name=name.replace('“','').replace('”','')
            date=li.xpath('i/text()')[0]
            name=date+'_'+name
            print(name)
            href='http://www.court.gov.cn'+li.xpath('a/@href')[0]
            #if name.endswith('指导性案例'):
            datasets[name]=href

    return datasets

def DXLawcase(url='http://www.court.gov.cn/zixun-gengduo-104.html'):
    urls=getlist(url)
    n=1
    for k,v in urls.items():
        path='law/DXLawcase/'+k+'.txt'
        #print(n)
        #n=n+1
        #if n>10:
        #    break
        if not os.path.exists(path):
            #print(k,v)

            text=gettxt_soup(v)
            #print(text)
            try:
                f=open(path,'w',encoding='utf8')
                f.write(text)
                f.close()
            except:
                f=open(path,'w',encoding='gbk')
                f.write(text)
                f.close()
            finally:
                f.close()
        time.sleep(0.1)

    return

def DXtohtml(path='law/casespp',func=wd.txt2html_odir,index=False):
    """
    path:文件夹的名称
    func:txt2html_odir,形成一个个单独的文件
        :txt2htmlv1,合并成一个文件
    """    
    ss={}
    for root,ds,fs in os.walk(path):
        for f in fs:
            #print(f)
            if os.path.splitext(f)[1] in ['.txt']:
                xu=tonum(f)
                ss[xu]=os.path.abspath(root+'/'+f)

    dd=sorted(ss.items(),key=lambda item:item[0])
    df=[]
    for i in dd:
        df.append(i[1])

    func(df,index=index)
    return
    
    

   
    
if __name__=="__main__":
    #ddd=getlist(sys.argv[1])
    #url='http://www.court.gov.cn/fabu-gengduo-77.html'
    #lawcase(url)
    DXLawcase()
    #SPPtohtml(func=wd.txt2htmlv1)
    #os.rename('output.html','最高检指导案例.html')
    #lawcase(sys.argv[1])
