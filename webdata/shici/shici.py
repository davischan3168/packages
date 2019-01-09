#!/usr/bin/env python3
# -*-coding:utf-8-*-
"""
__author__ = 'Davis'
http://wenxian.fanren8.com/
殆知阁
"""

import lxml.html
import sys
from lxml import etree
import requests
from io import StringIO,BytesIO
from webdata.util.hds import user_agent as hds

dataset=[]
base='http://122.200.75.13'
def _shici(url):
    
    global base
    global dataset
    print(url)
    r=requests.get(url,headers=hds())
    r=r.content.decode('utf8')
    html=lxml.html.parse(StringIO(r))
    res=html.xpath("//div[@class=\"panel-body\"]/span//text()")
    dataset.extend(res)
    nx=html.xpath("//ul[@class='pager']/li/a[text()='下一页']/../a/@href")
    url=base+nx[0]
    #urls.append(url)
    return url

def shici(url,output):
    """
    
    """
    url=_shici(url)
    while True:
        try:
            url=_shici(url)
        except:
            break
        
    _to_text(dataset,output)
    return
                
def _to_text(dataset,output):
    """
    make the content list to string, and 
    write it to output file.
    output is txt type file.
    """
    u=''.join(dataset)
    u=u.replace('\r\n','\n')
    f=open(output,'a',encoding='utf8')
    f.write(u)
    f.close()
    return

if __name__=="__main__":
    url='http://122.200.75.13/%E8%AF%97%E8%97%8F/%E8%AF%8D%E9%9B%86/%E5%85%A8%E5%AE%8B%E8%AF%8D.html'#
    #全宋词
    #url='http://122.200.75.13/%E8%AF%97%E8%97%8F/%E8%AF%97%E9%9B%86/%E5%85%A8%E5%94%90%E8%AF%97.html'
    #全唐诗

    shici(sys.argv[1],sys.argv[2])



