#!/usr/bin/env python3
# -*-coding:utf-8-*-

import pandas as pd
import numpy as np
import sys,os
import lxml.html
from lxml import etree
import requests,json
import re
import time
import datetime
from bs4 import BeautifulSoup
today=time.strftime('%Y-%m-%d')
from io import StringIO
from webdata.puse.sinapy import cons as wc

def FC_realtime_sina(code):
    """
    获得商品期货的实时交易数据
    Parameters:
    -----------------
    code:String
      RB0 螺纹钢
      AG0 白银
      AU0 黄金
      CU0 沪铜
      AL0 沪铝
      ZN0 沪锌
      PB0 沪铅
      RU0 橡胶
      FU0 燃油
      WR0 线材
      A0 大豆
      M0 豆粕
      Y0 豆油
      J0 焦炭
      C0 玉米
      L0 乙烯
      P0 棕油
      V0 PVC
      RS0 菜籽
      RM0 菜粕
      FG0 玻璃
      CF0 棉花
      WS0 强麦
      ER0 籼稻
      ME0 甲醇
      RO0 菜油
      TA0 甲酸
      种名 + 0 （数字0），代表品种连续，如果是其他月份，请使用品种名 + YYYMM
    ktype：
        5、15、30、60分钟线
      --------------
    Return
    """
    code=code.upper()
    url='http://hq.sinajs.cn/list=%s' %code
    r=requests.get(url,timeout=10)
    r=r.content.decode('gbk')
    r=r.split('hq_str_',1)[1]
    r=r.replace('="',',')
    r=r.replace('";','')
    df=pd.read_csv(StringIO(r),header=None)
    for i in [2,16,17,19,20,21,22,23,24,25,26,27,28]:
        df=df.drop(i,axis=1)
    df.columns=['code','name','open','high','low','pre-close','b1','s1','close','settle','pre-settle','bv1','sv1','hold','deal','date']
    return df

def _fcif_handle(r):
    r=r.content.decode('utf8')
    r=r.replace('],','\n')
    r=r.replace('[[','')
    r=r.replace(']]','')
    r=r.replace('"','')
    r=r.replace('[','')
    df=pd.read_csv(StringIO(r),header=None)
    try:
        df.columns=['date','open','high','low','close','volume']
    except:
        pass
    return df

def FC_hmin(ktype,code):
    """
    Parameters:
    -----------------
    code:String
      RB0 螺纹钢
      AG0 白银
      AU0 黄金
      CU0 沪铜
      AL0 沪铝
      ZN0 沪锌
      PB0 沪铅
      RU0 橡胶
      FU0 燃油
      WR0 线材
      A0 大豆
      M0 豆粕
      Y0 豆油
      J0 焦炭
      C0 玉米
      L0 乙烯
      P0 棕油
      V0 PVC
      RS0 菜籽
      RM0 菜粕
      FG0 玻璃
      CF0 棉花
      WS0 强麦
      ER0 籼稻
      ME0 甲醇
      RO0 菜油
      TA0 甲酸
      种名 + 0 （数字0），代表品种连续，如果是其他月份，请使用品种名 + YYYMM
    ktype：
        5、15、30、60分钟线
      --------------
    Return
    """
    code=code.upper()
    url='http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine%sm?symbol=%s' %(ktype,code)
    r=requests.get(url,timeout=10)
    df=_fcif_handle(r)
    df['date']=pd.to_datetime(df['date'])
    df=df.set_index('date')
    return df

def IF_hmin(ktype,code):
    """
    Parameters:
    -----------------
      IF 股指期货
      请使用品种名 + YYMM
      --------------
    Return
    """
    url='http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesMiniKLine%sm?symbol=%s' %(ktype,code)
    r=requests.get(url,timeout=10)
    df=_fcif_handle(r)
    df['date']=pd.to_datetime(df['date'])
    df=df.set_index('date')    
    return df

def FC_hday(code):
    """
    Parameters:
    -----------------
    code:String
      RB0 螺纹钢
      AG0 白银
      AU0 黄金
      CU0 沪铜
      AL0 沪铝
      ZN0 沪锌
      PB0 沪铅
      RU0 橡胶
      FU0 燃油
      WR0 线材
      A0 大豆
      M0 豆粕
      Y0 豆油
      J0 焦炭
      C0 玉米
      L0 乙烯
      P0 棕油
      V0 PVC
      RS0 菜籽
      RM0 菜粕
      FG0 玻璃
      CF0 棉花
      WS0 强麦
      ER0 籼稻
      ME0 甲醇
      RO0 菜油
      TA0 甲酸
      种名 + 0 （数字0），代表品种连续，如果是其他月份，请使用品种名 + YYMM
      --------------
    Return
    """
    code=code.upper()
    url='http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesDailyKLine?symbol=%s' %(code)
    r=requests.get(url,timeout=10)
    df=_fcif_handle(r)
    df['date']=pd.to_datetime(df['date'])
    df=df.set_index('date')    
    return df


def _fgh(r):
    text=r.text.split('=([{')[1]
    text=text.replace('}]);','')
    ddd=text.split('},{')
    
    zt='\n'.join(ddd)
    zt=zt.replace('date:','').replace('volume:','')
    zt=zt.replace('close:','').replace('high:','')
    zt=zt.replace('open:','').replace('low:','')
    df=pd.read_csv(StringIO(zt),header=None)
    df.columns=['date','open','high','low','close','volume']
    df=df.set_index('date')
    df.index=pd.to_datetime(df.index)
    df=df.applymap(lambda x: float(x))
    return df
    
def FC_ghday(code):
    """
    获取全球的股指期货、金属、农产品等数据
    -----------------------------
    DJS:道指期货
    ES:标普期货
    NAS:纳指期货	
    
    ZSD:LME锌3个月
    SND:LME镍(NID)
    PBD:LME铅3个月
    NID:LME镍3个月
    HG: 纽约铜
    CAD:LME铜3个月
    AHD:LME铝3个月
    GC:COMEX黄金
    
    OIL IPE布伦特原油
    NG: NYMEX天然气
    CL:NYMEX原油

    BP:IMM-英镑
    CD:IMM-加元
    DXF:美元指数期货
    EC:IMM-欧元
    JY:IMM-日元
    SF:IMM-瑞郎

    BO:黄豆油
    C:CBOT-玉米
    LHC:CME瘦肉猪
    S:CBOT-黄豆
    SB:NYBOT-11糖
    SM:黄豆粉
    W:CBOT-小麦
    """
    code=code.upper()
    url='http://stock2.finance.sina.com.cn/futures/api/jsonp.php/var%20_{0}=/GlobalFuturesService.getGlobalFuturesDailyKLine?symbol={0}'.format(code)
    r=requests.get(url,timeout=10)
    #print(r.text)
    df= _fgh(r)
    df['code']=code
    return df
    

def IF_hday(code):
    """
    IF:股指期货，后接年份（两位数）月份（两位数），分为当月、下月、下季（季末）、
    隔季（季末）
    IH:后接年份（两位数）月份（两位数），分为当月、下月、下季（季末）、
    隔季（季末）
    IC:后接年份（两位数）月份（两位数），分为当月、下月、下季（季末）、
    隔季（季末）
    """
    code=code.upper()
    url='http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesDailyKLine?symbol=%s' %(code)
    r=requests.get(url,timeout=10)
    df=_fcif_handle(r)
    return df

def _get_FC_hd(html):
    tbs=html.xpath('//div[@class="historyList"]/table[1]//tr')
    dls=[etree.tostring(node) for node in tbs]
    cc=''.join(str(dls))
    scc='<table>%s</table>'%cc
    df=pd.read_html(scc,header=1)[0]
    #print(df)
    #time.sleep(1)
    return df

def FC_hd(code,start='2010-01-01',end=today):
    """
    获得期货的历史数据，可以选择时间段
    """
    code=code.upper()
    if code in wc.czce:
        jys='czce'
    elif code in wc.dce:
        jys='dce'
    elif code in wc.shfe:
        jys='shfe'
    elif code in wc.cffex:
        jys='cffex'
    #url='http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?page={3}&breed={0}0&start={1}&end={2}&jys=shfe&pz={0}&hy={0}0&type=inner'.format(code,start,end,1)
    url=wc.FC_url.format(code,start,end,1,jys)
    r=requests.get(url)
    text=r.content.decode('gbk')
    html=lxml.html.parse(StringIO(text))
    df=_get_FC_hd(html)
    page=html.xpath('//div[@class="historyList"]/table[2]//tr//@href')
    tpgs=re.findall(r'page=(\d+)',page[1])[0]
    tpgs=int(tpgs)
    if tpgs>1:
        for i in range(2,tpgs+1):
            #url='http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?page={3}&breed={0}0&start={1}&end={2}&jys=shfe&pz={0}&hy={0}0&type=inner'.format(code,start,end,i)
            url=wc.FC_url.format(code,start,end,i,jys)
            r=requests.get(url)
            text=r.content.decode('gbk')
            html=lxml.html.parse(StringIO(text))
            df=df.append(_get_FC_hd(html))
    df.columns=['date','close','open','high','low','amount']
    df['date']=pd.to_datetime(df['date'])
    df=df.set_index('date')
    df=df.applymap(lambda x: float(x))
    df=df.sort_index()
    df=df[['open','high','low','close','amount']]
    return df

if __name__=="__main__":
    code='AU0'
    #df=get_hday_fc(code)
    #df=get_realtime_fc_sina(code)
    #df=get_hmin_fc(5,code)
    #df=get_hday_if('Ic1706')
    #df=FC_gloabal_hday(sys.argv[1])
    df=FC_hd(sys.argv[1])
