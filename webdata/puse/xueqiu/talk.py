#!/usr/bin/env python3
# -*-coding:utf-8-*-
from webdata.util.hds import user_agent as hds
import lxml.html
from io import StringIO
import sys,os,json,time
import requests
from webdata.util.chrome_cookies import firefox_cookies as gcookies

def get_searchjson_xueqiu(code,host='.xueqiu.com',lp=10):
    if code[0] in ['6','9']:
        code='SH'+code
    elif code[0] in ['0','2','3']:
        code='SZ'+code
    else:
        sys.exit()

    exlist=[]
    s=requests.Session()
    for i in range(lp+1):
        url='https://xueqiu.com/statuses/search.json?count=10&comment=0&symbol={0}&hl=0&source=all&sort=time&page={1}&q='.format(code,i)
        r=s.get(url,cookies=gcookies(host),headers=hds())
        data=json.loads(r.text)
        for txs in data['list']:
            text=txs['text']
            dtext=lxml.html.parse(StringIO(text))
            dtem=dtext.xpath('//p/text()')
            if len(dtem)>0:
                exlist.append(dtem)

    return exlist

def _hotline(data):
    
    exlist=[]
    for its in data['list']:
        datasets={}
        dataI=json.loads(its['data'])
        datasets['target']=dataI['target']
        datasets['title']=dataI['title']
        datasets['desc']=dataI['user']['description']
        datasets['id']=dataI['user']['id']
        datasets['reply_count']=dataI['reply_count']
        datasets['created_at']=dataI['created_at']
        datasets['text']=get_text(dataI['target'])
        if len(datasets['text'])>10:
            exlist.append(datasets)
        time.sleep(0.02)
    return exlist

def hotline_xueqiu(host='.xueqiu.com'):
    hurl='https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&max_id=-1&count=10&category=-1'
    s=requests.Session()
    r=s.get(hurl,cookies=gcookies(host),headers=hds())
    data=json.loads(r.text)
    exlist=[]
    exlist.extend(_hotline(data))
    nmid=data['next_max_id']
    go=1
    url='https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&max_id={0}&count=15&category=-1'.format(nmid)
    for i in range(nmid,0,-15):
        r=s.get(hurl,cookies=gcookies(host),headers=hds())
        dataI=json.loads(r.text)
        exlist.extend(_hotline(dataI))
        go=go+1
        if go>20:
            break
        

    return exlist

def get_text(tartget,host='.xueqiu.com'):
    base='https://xueqiu.com'
    url=base+str(tartget)
    s=requests.Session()
    r=s.get(url,cookies=gcookies(host),headers=hds())    
    html=lxml.html.parse(StringIO(r.text))
    xc=html.xpath('//article/div/p//text()')
    text='\n'.join(xc)
    return text
    

        
        
        
        
    
    
    
if __name__=="__main__":
    #df=get_searchjson_xueqiu(sys.argv[1])
    dd=hotline()
    #text=get_text('/2395350277/105331151')
