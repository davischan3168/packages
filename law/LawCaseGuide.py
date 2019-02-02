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

def gettxt(url):
    r=requests.get(url,headers=hds())
    txt=r.content.decode('utf8')
    html=lxml.html.parse(StringIO(txt))
    html=html.xpath('//div[@id="container"]/div[1]//div[@class="txt_txt"]//text()')
    text='\n'.join(html)
    return text

def getlist(url):
    r=requests.get(url,headers=hds())
    txt=r.content.decode('utf8')
    #print(txt)
    html=lxml.html.parse(StringIO(txt))
    lis=html.xpath('//div[@id="container"]/div[@class="sec_list"]/ul/li')
    datasets={}
    for li in lis:
        name=re.sub(r'\s*','',li.xpath('a/@title')[0].strip())
        name=name.replace('“','').replace('”','')
        print(name)
        href='http://www.court.gov.cn'+li.xpath('a/@href')[0]
        if name.startswith('指导案例'):
            datasets[name]=href

    nxp=html.xpath('//ul[@id="yw1"]/li/a[text()="下一页"]/@href')
    nxtt=[]
    while len(nxp)>0:
        ull='http://www.court.gov.cn'+nxp[0]
        if ull not in nxtt:
            r=requests.get(ull,headers=hds())
            print(ull)
            txt=r.text
            html=lxml.html.parse(StringIO(txt))
            lis=html.xpath('//div[@id="container"]/div[@class="sec_list"]/ul/li')
            nxp=html.xpath('//ul[@id="yw1"]/li/a[text()="下一页"]/@href')
            for li in lis:
                #name=li.xpath('a/@title')[0].strip()
                name=re.sub(r'\s*','',li.xpath('a/@title')[0].strip())
                name=name.replace('“','').replace('”','')
                href='http://www.court.gov.cn'+li.xpath('a/@href')[0]
                if name.startswith('指导案例'):
                    datasets[name]=href
            
        else:
            break

    return datasets

def lawcase(url):
    urls=getlist(url)
    n=1
    for k,v in urls.items():
        path='law/case/'+k+'.txt'
        #print(n)
        #n=n+1
        #if n>10:
        #    break
        if not os.path.exists(path):
            print(k,v)

            text=gettxt(v)
            print(text)
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

def lawcaseII(url='http://www.court.gov.cn/fabu-gengduo-77.html',pgs=1):
    uls=[]
    datasets={}
    uls.append(url)
    if pgs>1:
        for p in range(2,pgs+1):
            url='http://www.court.gov.cn/fabu-gengduo-77.html?page=%s'%p
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
            if name.startswith('指导案例'):
                datasets[name]=href

    for tt,ul in datasets.items():
        path='law/case/'+tt+'.txt'
        
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
        
def Lawtohtml(path='law/case',func=wd.txt2html_odir,index=False):
    """
    path:文件夹的名称
    func:txt2html_odir,形成一个个单独的文件
        :txt2htmlv1,合并成一个文件
    """    
    ss={}
    for root,ds,fs in os.walk(path):
        for f in fs:
            #print(f)
            dfd=os.path.splitext(f)
            if dfd[1] in ['.txt']:
                dd=re.findall('\d{1,3}',dfd[0])
                dd=int([i for i in dd if len(i)>0][0])
                ss[dd]=os.path.abspath(root+'/'+f)

    dds=sorted(ss.items(),key=lambda item:item[0])
    df=[]
    for i in dds:
        df.append(i[1])

    func(df,index=index)
    return
        
    
if __name__=="__main__":
    #ddd=getlist(sys.argv[1])
    #url='http://www.court.gov.cn/fabu-gengduo-77.html'
    #lawcase(url)
    lawcaseII()
    Lawtohtml(func=wd.txt2htmlv1)
    os.rename('output.html','最高法指导性案例.html')
    #lawcase(sys.argv[1])
    
    
    
