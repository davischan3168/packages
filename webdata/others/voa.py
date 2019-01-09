#!/usr/bin/env python3
# -*-coding:utf-8-*-

import requests
import lxml.html
import sys,os,time
from bs4 import BeautifulSoup
from io import StringIO

def get_voa_list(url):
    #url='http://www.51voa.com/VOA_Special_English'
    urlb='http://www.51voa.com'
    r=requests.get(url)
    txt=r.text
    html=lxml.html.parse(StringIO(txt))
    res=html.xpath('//div[@id="list"]/ul/li')
    urls={}
    for a in res:
        try:
            name=a.xpath('a[last()]/text()')[0].strip()
            href=urlb+a.xpath('a[last()]/@href')[0]
            urls[name]=href
        except Exception as e:
            print(e)

    return urls

def get_mp3_text(url):
    r=requests.get(url)
    txt=r.text
    html=lxml.html.parse(StringIO(txt))
    try:
        mp3url=html.xpath('//a[@id="mp3"]/@href')[0].strip().replace(':','').replace("'",'').replace(' ','').replace('\t','').replace('\n','')
        path=os.path.join('../voa',os.path.basename(mp3url))
        r=requests.get(mp3url)
        if not os.path.exists(path):
            with open(path,'wb') as f:
                f.write(r.content)

        title=html.xpath('//div[@id="title"]/h1/text()')[0].strip().replace(':','').replace("'",'').replace(' ','').replace('\t','').replace('\n','')
        content=html.xpath('//div[@id="content"]//text()')
        content=[x.strip() for x in content]
        content='\n'.join(content)
        fpath='../voa/'+title+'.txt'
        if not os.path.exists(fpath):
            with open(fpath,'w') as f:
                f.write(content)
    except Exception as e:
        print(e)
    
    return

def get_allmp3(url):
    urls=get_voa_list(url)
    for k,v in urls.items():
        print(v)
        get_mp3_text(v)
        

if __name__=="__main__":
    
    #get_mp3_text(sys.argv[1])
    get_allmp3(sys.argv[1])
    
