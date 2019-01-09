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
import webdata.puse.sinapy.cons as ws

hy={ '交通运输': 'new_jtys',
 '仪器仪表': 'new_yqyb',
 '供水供气': 'new_gsgq',
 '公路桥梁': 'new_glql',
 '其它行业': 'new_qtxy',
 '农林牧渔': 'new_nlmy',
 '农药化肥': 'new_nyhf',
 '化工行业': 'new_hghy',
 '化纤行业': 'new_hqhy',
 '医疗器械': 'new_ylqx',
 '印刷包装': 'new_ysbz',
 '发电设备': 'new_fdsb',
 '商业百货': 'new_sybh',
 '塑料制品': 'new_slzp',
 '家具行业': 'new_jjhy',
 '家电行业': 'new_jdhy',
 '建筑建材': 'new_jzjc',
 '开发区': 'new_kfq',
 '房地产': 'new_fdc',
 '摩托车': 'new_mtc',
 '有色金属': 'new_ysjs',
 '服装鞋类': 'new_fzxl',
 '机械行业': 'new_jxhy',
 '次新股': 'new_stock',
 '水泥行业': 'new_snhy',
 '汽车制造': 'new_qczz',
 '煤炭行业': 'new_mthy',
 '物资外贸': 'new_wzwm',
 '环保行业': 'new_hbhy',
 '玻璃行业': 'new_blhy',
 '生物制药': 'new_swzz',
 '电力行业': 'new_dlhy',
 '电器行业': 'new_dqhy',
 '电子信息': 'new_dzxx',
 '电子器件': 'new_dzqj',
 '石油行业': 'new_syhy',
 '纺织机械': 'new_fzjx',
 '纺织行业': 'new_fzhy',
 '综合行业': 'new_zhhy',
 '船舶制造': 'new_cbzz',
 '造纸行业': 'new_zzhy',
 '酒店旅游': 'new_jdly',
 '酿酒行业': 'new_ljhy',
 '金融行业': 'new_jrhy',
 '钢铁行业': 'new_gthy',
 '陶瓷行业': 'new_tchy',
 '飞机制造': 'new_fjzz',
 '食品行业': 'new_sphy'}

dy={'上海': '上海',
 '云南': '云南',
 '内蒙古': '内蒙古',
 '北京': '北京',
 '吉林': '吉林',
 '四川': '四川',
 '天津': '天津',
 '宁夏': '宁夏',
 '安徽': '安徽',
 '山东': '山东',
 '山西': '山西',
 '广东': '广东',
 '广西': '广西',
 '新疆': '新疆',
 '江苏': '江苏',
 '江西': '江西',
 '河北': '河北',
 '河南': '河南',
 '浙江': '浙江',
 '海南': '海南',
 '湖北': '湖北',
 '湖南': '湖南',
 '甘肃': '甘肃',
 '福建': '福建',
 '西藏': '西藏',
 '贵州': '贵州',
 '辽宁': '辽宁',
 '重庆': '重庆',
 '陕西': '陕西',
 '青海': '青海',
 '黑龙江': '黑龙江'}


gn={'3G概念': '3G概念',
 'CDM项目': 'CDM项目',
 'IGCC': 'IGCC',
 'OTC医药': 'OTC医药',
 'QFII持股板块': 'QFII持股板块',
 'ST股板块': 'ST股板块',
 '三通概念': '三通概念',
 '世博概念': '世博概念',
 '中字头': '中字头',
 '交叉持股': '交叉持股',
 '信托持股': '信托持股',
 '借壳上市': '借壳上市',
 '关中天水': '关中天水',
 '再融资': '再融资',
 '农业龙头': '农业龙头',
 '出口退税': '出口退税',
 '分拆上市': '分拆上市',
 '创投概念': '创投概念',
 '参股金融': '参股金融',
 '图们江': '图们江',
 '基金重仓': '基金重仓',
 '增持承诺': '增持承诺',
 '外资并购': '外资并购',
 '大订单': '大订单',
 '奥运概念': '奥运概念',
 '奥运概念股': '奥运概念股',
 '循环经济': '循环经济',
 '成渝特区': '成渝特区',
 '数字电视': '数字电视',
 '整体上市': '整体上市',
 '新材料': '新材料',
 '新能源': '新能源',
 '智能电网': '智能电网',
 '期股概念': '期股概念',
 '未股改': '未股改',
 '横琴新区': '横琴新区',
 '次新股': '次新股',
 '次新股板块': '次新股板块',
 '江苏沿海': '江苏沿海',
 '海峡西岸': '海峡西岸',
 '滨海新区': '滨海新区',
 '灾后重建': '灾后重建',
 '煤化工': '煤化工',
 '物联网': '物联网',
 '珠江三角': '珠江三角',
 '社保重仓': '社保重仓',
 '稀缺资源': '稀缺资源',
 '网络游戏': '网络游戏',
 '股指期货': '股指期货',
 '股权激励': '股权激励',
 '航天军工': '航天军工',
 '节能环保': '节能环保',
 '融资融券': '融资融券',
 '资产注入': '资产注入',
 '软件开发': '软件开发',
 '辽宁沿海': '辽宁沿海',
 '迪士尼': '迪士尼',
 '退市警示': '退市警示',
 '铁路基建': '铁路基建',
 '长三角': '长三角',
 '黄河三角': '黄河三角',
 '黄金股': '黄金股'}

def get_predict_Sina(mtype):
    """
    mtype:
         eps--每股收益,
         sales--营业收入,
         np--净利润,
         roe--净资产收益率
    """
    pn=1
    DF=pd.DataFrame()
    ws._write_head()
    while True:
        try:
            ws._write_console()
            url='http://vip.stock.finance.sina.com.cn/q/go.php/vPerformancePrediction/kind/{0}/index.phtml?num=60&p={1}'.format(mtype,pn)
            r=requests.get(url)
            r=r.content.decode('gbk')
            html=BeautifulSoup(r,'lxml')
            text=html.find(id='dataTable')
            df=pd.read_html(str(text),header=0)[0]
            if df.empty is True:
                break
            else:
                pn = pn + 1
                DF =DF.append(df)
                if pn >30:
                    break
        except:
            break
    DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
    DF=DF.set_index('股票代码')
    DF.index=DF.index.map(lambda x: str(x).split('.')[0].zfill(6))    
    return DF

def get_predict_share_Sina(code,mtype):
    """
    mtype:
         eps--每股收益,
         sales--营业收入,
         np--净利润,
         roe--净资产收益率
    """
    pn=1
    DF=pd.DataFrame()
    ws._write_head()
    while True:
        try:
            ws._write_console()
            url='http://vip.stock.finance.sina.com.cn/q/go.php/vPerformancePrediction/kind/{0}/index.phtml?symbol={1}&p={2}'.format(mtype,code,pn)
            r=requests.get(url)
            r=r.content.decode('gbk')
            html=BeautifulSoup(r,'lxml')
            text=html.find(id='dataTable')
            df=pd.read_html(str(text),header=0)[0]
            if df.empty is True:
                break
            else:
                pn = pn + 1
                DF =DF.append(df)
        except:
            break
    DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
    DF=DF.set_index('股票代码')
    DF.index=DF.index.map(lambda x: str(x).split('.')[0].zfill(6))    
    return DF

def get_researchRate_Sina(mtype,period=10,rate=None,srate=None,zf=None):
    """
    投资评级选股
    ------------------------------
    mtype: hy,dy,gn
    preiod: -1,10,30,60
    rate:5,4,3,2,1
    srate:5,4,3,2,1
    zf:1,2,3,4,5
    -----------------------------
    Return:
        DataFrame
           code: 股票代码
           name :股票名称
           rate :最新评级
           target: 目标价
           date :评级时间
           srate :综合评价
           chage :平均涨幅
           industry:行业
    """
    burl='http://vip.stock.finance.sina.com.cn/q/go.php/vIR_CustomSearch/index.phtml?sr_p=%s'%period
    if mtype == 'hy':
        name=input("Enter name in %s"%mtype)
        burl=burl+'&industry='+hy[name]
    elif mtype == 'dy':
        name=input("Enter name in %s"%mtype)
        burl=burl+'&zone='+dy[name]
    elif mtype == 'gn':
        name=input("Enter name in %s"%mtype)
        burl=burl+'&concept='+gn[name]
    else:
        pass

    if rate is not None:
        burl=burl+'&rating=%s'%rate

    if srate is not None:
        burl=burl+'&srating=%s'%srate

    if zf is not None:
        burl=burl+'&sprice=%s'%zf

    
    #burl=burl+'&p={0}'
    #print(burl)
    DF=pd.DataFrame()
    ws._write_head()
    pageno=1
    while True:
        #print(pageno)
        url=burl+'&p={0}'.format(pageno)
        try:
            ws._write_console()
            #print(url)
            r=requests.get(url)
            text=r.content.decode('gbk')
            items=lxml.html.parse(StringIO(text))
            tb=items.xpath('//table[@class="list_table"]//tr[position()>1]')
            sarr=[etree.tostring(node) for node in tb]
            sarr = '<table>%s</table>'%sarr
            df=pd.read_html(str(text),header=None)[0]
            df=df.drop(0,axis=0)
            if df.empty:
                #print("No data")
                break
            else:
                DF =DF.append(df)
                pageno = pageno +1
        except:
            #print(url)
            break
        
    
    try:
        DF=DF.drop([7,9,10,11,12,13],axis=1)
        DF.columns=['code','name','rate','target','srate','chage','industry']
    except:
        DF.columns=['code','name','rate','target','date','srate','chage','industry']
        pass
    DF=DF.reset_index(drop=True)
    #DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
    #DF=DF.set_index('股票代码')
    #DF.index=DF.index.map(lambda x: str(x).split('.')[0].zfill(6))
    DF=DF.replace('--',np.nan)
    DF['target']=DF['target'].map(lambda x:float(x))
    return DF
    
        
    
if __name__=="__main__":
    #df=predict_share('eps','600000')
    df=get_researchRate_Sina(sys.argv[1])
