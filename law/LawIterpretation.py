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
"获取最高法的司法解释文本"
ls={}
def _getHtml(html):
    global ls
    res=html.xpath('//div[@class="sec_list"]/ul/li/a')
    for item in res:
        title=item.xpath('@title')[0].strip().replace('&nbsp;','').replace('\n','').replace(' ','_').replace('\t','')
        url='http://www.court.gov.cn'+item.xpath('@href')[0]
        ls[title]=url
    return

def page(url):
    r=requests.get(url)
    html=lxml.html.parse(StringIO(r.content.decode('utf8')))
    _getHtml(html)

    nxurl=html.xpath('//ul[@id="yw1"]/li[@class="next"]/a/@href')
    if len(nxurl)>0:
        nxurl0='http://www.court.gov.cn'+nxurl[0]
        page(nxurl0)
        
    return

def getsfjs():
    if len(ls)<1:
        page('http://www.court.gov.cn/fabu-gengduo-16.html')

    for k,v in ls.items():

        path='law/sikao/sifa/'+k+'.txt'
        if not os.path.exists(path):
            rr=requests.get(v)
            soup=BeautifulSoup(rr.text,'lxml')
            text=soup.find('div',attrs={'class':'txt_txt'}).text
            try:
                f=open(path,'w',encoding='utf8')
                f.write(text)
            except:
                f=open(path,'w',encoding='utf8')
                f.write(text)            
            f.close()
            print("Finish getting %s"%k)
        else:
            pass
            #print("File exists %s"%k)
        time.sleep(0.5)

    return

def LawInterpretation(url='http://www.court.gov.cn/fabu-gengduo-16.html',pgs=13):
    uls=[]
    datasets={}
    uls.append(url)
    if pgs>1:
        for p in range(2,pgs+1):
            url='http://www.court.gov.cn/fabu-gengduo-16.html?page=%s'%p
            uls.append(url)

    for url in uls:
        r=requests.get(url,headers=hds())
        #urls=[]
        txt=r.content.decode('utf8')
        html=lxml.html.parse(StringIO(txt))
        lis=html.xpath('//div[@id="container"]/div[@class="sec_list"]/ul/li')
        
        for li in lis:
            name=re.sub(r'\s*','',li.xpath('a/@title')[0].strip())
            name=name.replace('“','').replace('”','').replace(':','：').replace('&nbsp','')
            #print(name)
            href='http://www.court.gov.cn'+li.xpath('a/@href')[0]
            #if name.startswith('指导案例'):
            datasets[name]=href

    for tt,ul in datasets.items():
        path='law/sikao/sifa/'+tt+'.txt'
        
        if not os.path.exists(path):
            rr=requests.get(ul,headers=hds())
            soup=BeautifulSoup(rr.text,'lxml')
            txt=soup.find('div',attrs={'class','txt_txt'}).text
            print("getting file %s"%path)
            try:
                f=open(path,'w',encoding='utf8')
                f.write(txt)
                f.close()
            except:
                f=open(path,'w',encoding='gbk')
                f.write(txt)
                f.close()
            finally:
                f.close()
            time.sleep(0.1)    
    return

def Interpretation2html(path='law/sikao/sifa',func=wd.txt2html_odir,index=False):
    """
    path:文件夹的名称
    func:txt2html_odir,形成一个个单独的文件
        :txt2htmlv1,合并成一个文件
    """
    ss=[]
    for root,ds,fs in os.walk(path):
        for f in fs:
            #print(f)
            dfd=os.path.splitext(f)
            if dfd[1] in ['.txt']:
                #dd=re.findall('\d{1,3}',dfd[0])
                #dd=int([i for i in dd if len(i)>0][0])
                ss.append(os.path.abspath(root+'/'+f))

    func(ss,index=index)
    return

    

if __name__=="__main__":
    #getsfjs()
    LawInterpretation()
        
    Interpretation2html(func=wd.txt2htmlv1)
    os.rename('output.html','司法解释.html')
