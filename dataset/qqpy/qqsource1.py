#!/usr/bin/env python3
# -*-coding:utf-8-*-
import time,random,requests,json,re
import pandas as pd
import datetime as dt
from io import StringIO
import webdata as wd

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from lxml import etree

today=dt.datetime.today()
today=today.strftime('%Y%m%d')

radar_type={1:'09000945',2:'09451000',3:'10001015',4:'10151030',5:'10301045',6:'10451100',7:'11001115',8:'11151130',9:'13001315',10:'13151330',11:'13301345',12:'13301345',13:'14001415',14:'14151430',15:'14301445',16:'14451515'}



def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timing out after 10 seconds and returning")
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return

class QQSource(object):
    def __init__(self,browser=0,use_cookie=0):
        self.browser=browser
        #self.code=code
        self.use_cookiex=use_cookie
        
        self.indu_url={'tt':'http://stockapp.finance.qq.com/mstats/#mod=list&id=bd_ind&module=BD&type=01&page=1&max=80','gn':'http://stockapp.finance.qq.com/mstats/#mod=list&id=bd_cpt&module=BD&type=02&page=1&max=80','dy':'http://stockapp.finance.qq.com/mstats/#mod=list&id=bd_cpt&module=BD&type=03&page=1&max=80','zjh':'http://stockapp.finance.qq.com/mstats/#mod=list&id=bd_cpt&module=BD&type=04&page=1&max=80'}
        self.index_url={'all':'http://stockapp.finance.qq.com/mstats/?pgv_ref=fi_quote_navi_bar#mod=list&id=indices&module=GIDX&type=ALL','eur':'http://stockapp.finance.qq.com/mstats/?pgv_ref=fi_quote_navi_bar#mod=list&id=indices_EU&module=GIDX&type=EU','am':'http://stockapp.finance.qq.com/mstats/?pgv_ref=fi_quote_navi_bar#mod=list&id=indices_AM&module=GIDX&type=AM','as':'http://stockapp.finance.qq.com/mstats/?pgv_ref=fi_quote_navi_bar#mod=list&id=indices_AS&module=GIDX&type=AS','oa':'http://stockapp.finance.qq.com/mstats/?pgv_ref=fi_quote_navi_bar#mod=list&id=indices_OA&module=GIDX&type=OA','af':'http://stockapp.finance.qq.com/mstats/?pgv_ref=fi_quote_navi_bar#mod=list&id=indices_AF&module=GIDX&type=AF'}
        
        self.concept=None
        self.indexcmpst=None
        if self.use_cookiex==0:
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = ('Mozilla/5.0(WindowsNT6.1;WOW64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/59.0.3071.115Safari/537.36x-requested-with:XMLHttpRequest')
            dcap["phantomjs.page.settings.loadImages"] = True
            
            if self.browser==0:
                self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
            if self.browser==1:
                self.driver=webdriver.Chrome()
            if self.browser==2:
                self.driver=webdriver.Firefox()
                
    def craw_concept(self,mtype='tt'):
        """
        获得行业或同概念分类的数据
        ---------------------------
        mtype: tt-腾讯行业,gn-概念分类,dy-地域分类,zjh-证监会行业
        """
        url=self.indu_url[mtype]
        self.driver.get(url)
        waitForLoad(self.driver)
        dataset=[]


        listbd=self.driver.find_elements_by_xpath("//ul[@id='list-body']/li")
            
        for lbd in listbd:
            try:
                ss=lbd.text
                ss=ss.split('\n')
                idd=re.findall('list-li-bkhz(\d+[a-zA-Z]*\d+)',lbd.get_attribute('id'))[0]
                ss.append(idd)
                #print(ss)
                dataset.append(ss)
            except Exception as e:
                print(e)
                break
        

        pages=int(self.driver.find_elements_by_xpath("//div[@id='page-navi']/a")[-2].text)
        #print(pages)
        if pages>1:
        
            for _ in range(pages-1):
                self.driver.find_element_by_link_text("下一页").click()
                waitForLoad(self.driver)
                listbd=self.driver.find_elements_by_xpath("//ul[@id='list-body']/li")
            
                for lbd in listbd:
                    try:
                        ss=lbd.text
                        ss=ss.split('\n')
                        idd=re.findall('list-li-bkhz(\d+[a-zA-Z]*\d+)',lbd.get_attribute('id'))[0]
                        ss.append(idd)
                        #print(ss)
                        dataset.append(ss)
                    except Exception as e:
                        print(e)
                    break
            
        df=pd.DataFrame(dataset)
        df=df.drop_duplicates()
        df.columns=['name','num','avg_price','Chg','Chg%','volume(x100)','amount(10k)','L.name','L.chg','L.price','L.chg%','id']
        if self.concept is None:
            self.concept=df
        else:
            self.concept=self.concept.append(df)

        self.concept.drop_duplicates(keep='last',inplace=True)
        return self.concept

        
    def read_conceptid(self,mtype='tt',lc=True):
        """读取同行业或概念的数据"""
        if lc:
            try:
                self.concept=pd.read_pickle('./output/qqsource/concept.pkl')
            except:
                self.concept=pd.read_csv('./output/qqsource/concept.csv',index_col=0,header=0)
                self.concept['id']=self.concept['id'].map(lambda x:str(x).zfill(6))
        else:
            for mtype in ['tt','gn','dy','zjh']:
                self.concept=self.craw_concept(self,mtype)
            
        return self.concept
                
    def get_industry_basic(self,indu):
        """获得同业的股票基本走势信息的数据"""
        if self.concept is None:
            df=self.read_conceptid()
        else:
            df=self.concept

        idd=list(df[df['name']==indu]['id'])[0]
        for i in ['1','2','3','4']:
            url='http://stock.gtimg.cn/data/get_hs_xls.php?id=pt{0}&type={1}&metric=chr'.format(idd,i)
            try:
                data=pd.read_excel(url,skiprows=1)
            except:
                pass
                
        data.columns=['code','name','price','chg%','chg','buy','sell','volume','amount','open','pre.close','high','low']
        return data

    def get_industry_moment(self,indu):
        """获得同业的股票阶段走势信息的数据"""
        if self.concept is None:
            df=self.read_conceptid()
        else:
            df=self.concept

        idd=list(df[df['name']==indu]['id'])[0]
        for i in ['1','2','3','4']:
            url='http://stock.gtimg.cn/data/get_hs_xls.php?id=pt{0}&type={1}&metric=name'.format(idd,i)
            try:
                data=pd.read_excel(url,skiprows=3,header=None)
            except:
                pass
                
        data.columns=['code','name','5high','5low','5chg%','5turnover','10high','10low','10chg%','10turnover','20high','20low','20chg%','20turnover']
        return data

    def get_industry_cashf(self,indu):
        """获得同业的股票资金流入流出信息的数据"""
        if self.concept is None:
            df=self.read_conceptid()
        else:
            df=self.concept

        idd=list(df[df['name']==indu]['id'])[0]
        
        url='http://stockapp.finance.qq.com/mstats/#mod=list&id=bd{0}&module=SS&type=pt{0}&sort=-1&page=1&max=80&index=2'.format(idd)
        self.driver.get(url)
        waitForLoad(self.driver)

        dataset=[]
   
        for _ in range(3):
            listbd=self.driver.find_elements_by_xpath("//ul[@id='list-body']/li")
            
            for lbd in listbd:
                try:
                    ss=lbd.text
                    ss=ss.split('\n')
                    dataset.append(ss)
                except Exception as e:
                    print(e)
                    break
            try:
                self.driver.find_element_by_link_text("下一页").click()
                waitForLoad(self.driver)
            except:
                pass
            
        df=pd.DataFrame(dataset)
        df=df.drop_duplicates()        

        try:
            df.columns=['code','name','Main.in','Main.out','Small.in','Small.out','Increase.Post','Main.in5','Main.out5']
        except:
            pass
        return df


    def index_Global(self,mtype='all'):
        """
        mtype: all 全球指数
               as  亚洲指数
               af  非洲指数
               eur 欧洲指数
               am  美洲指数
        """
        url=self.index_url[mtype]

        self.driver.get(url)
        waitForLoad(self.driver)
        
        dataset=[]
   
        for _ in range(2):
            listbd=self.driver.find_elements_by_xpath("//ul[@id='list-body']/li")
            
            for lbd in listbd:
                try:
                    ss=lbd.text
                    ss=ss.split('\n')
                    dataset.append(ss)
                except Exception as e:
                    print(e)
                    break
            self.driver.find_element_by_link_text("下一页").click()
            waitForLoad(self.driver)
            
        df=pd.DataFrame(dataset)
        df=df.drop_duplicates()
        df.columns=['name','price','Chg','Chg%','time']
        return df

    def newlist(self):
        """报盘新闻
        """
        url='http://web.ifzq.gtimg.cn/appstock/news/columnNews/getNews?page=1&limit=50&column=txbp&_var=finance_txbp'
        
        r=requests.get(url)
        text=r.text.split("=")[1]
        daa=json.loads(text)

        df=pd.DataFrame(daa['data']['data'])
        return df

    def Radar(self,mtype):
        """
        获取市场中出现异常交易的股票
        """
        if isinstance(mtype,int):
            url='http://stock.gtimg.cn/data/index.php?appn=radar&t=all&d={0}'.format(radar_type[mtype])
        elif isinstance(mtype,str):
            if mtype == 'all':
                url='http://stock.gtimg.cn/data/index.php?appn=radar&t=all&v=vLATEST'
            elif mtype == 'latest':
                    url='http://stock.gtimg.cn/data/index.php?appn=radar&t=latest&v=vLATEST'
                    
        r=requests.get(url)
        text=r.content.decode('gbk').split(",data:'")[1].replace("^'};",'')
        text=text.replace('^','\n')
        text=text.replace('~',',')
        df=pd.read_csv(StringIO(text),header=None)
        return df

    def holders(self,enday='2017-06-30'):
        """股东变化情况"""

        df=pd.DataFrame()
        
        url='http://web.ifzq.gtimg.cn/fund/zcjj/zcjj/allzc?colum=3&order=desc&page=1&pagesize=50&bgrq={0}&_var=v_jjcg'.format(enday)
        r=requests.get(url)
        text=r.text.split("=")[1]
        data=json.loads(text)
        df=df.append(pd.DataFrame(data['data']['data']))
        tp=data['data']['totalPages']
        for pn in range(2,tp+1):
            url='http://web.ifzq.gtimg.cn/fund/zcjj/zcjj/allzc?colum=3&order=desc&page={1}&pagesize=50&bgrq={0}&_var=v_jjcg'.format(enday,pn)
            r=requests.get(url)
            text=r.text.split("=")[1]
            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']['data']))
        df=df.reset_index(drop=True)
        df.columns=['','Share.Increase(10k)','Holder.Num','Curr.Rate%','code','name']
        return df
        
    def ggnotice(self,day=today):
        """day: 20170725"""
        url='http://stock.finance.qq.com/cgi-bin/sstock/q_gonggao_js?t=0&c=&b={0}&e=&p=1'.format(day)
        r=requests.get(url)
        text=r.text.split("_datas:[[")[1].replace("]],_o:0};","")
        text=text.replace("],[",'\n')
        df=pd.read_csv(StringIO(text),header=None)
        df=df.drop([0,4],axis=1)
        return df

    def Gold(self):
        """获得黄金价格信息"""
        url='http://stockapp.finance.qq.com/mstats/?pgv_ref=fi_quote_navi_bar#mod=list&id=gold&module=GOLD'
        self.driver.get(url)
        waitForLoad(self.driver)
        dataset=[]
        for _ in range(2):
            listbd=self.driver.find_elements_by_xpath("//ul[@id='list-body']/li")
            
            for lbd in listbd:
                try:
                    ss=lbd.text
                    ss=ss.split('\n')
                    #idd=re.findall('s[h|z]\d+',lbd.get_attribute('id'))[0]
                    #ss.append('xdi_'+idd)
                    #print(ss)
                    dataset.append(ss)
                except Exception as e:
                    print(e)
                    break
            try:
                self.driver.find_element_by_link_text("下一页").click()
                waitForLoad(self.driver)
            except:
                pass

        df=pd.DataFrame(dataset)
        df.columns=['name','price','avg_price','close','volume(kg)','amount','Chg','high','low','pre.close','open']

        return df

    def Future_Global(self,mtype='global'):
        """获得期货价格信息
        """
        if mtype == 'global':
            url='http://stockapp.finance.qq.com/mstats/?pgv_ref=fi_quote_navi_bar#mod=list&id=qh_global&module=GQH&type=ALL'

        if mtype=='dalian':
            url='http://stockapp.finance.qq.com/mstats/?pgv_ref=fi_quote_navi_bar#mod=list&id=qh_dalian&module=QH&type=EXDL&page=1&max=80'
        if mtype == 'shanghai':
            url='http://stockapp.finance.qq.com/mstats/?pgv_ref=fi_quote_navi_bar#mod=list&id=qh_shanghai&module=QH&type=EXSH&page=1&max=80'
        if mtype=='zhengzhou':
            url='http://stockapp.finance.qq.com/mstats/?pgv_ref=fi_quote_navi_bar#mod=list&id=qh_zhengzhou&module=QH&type=EXZZ&page=1&max=80'
        if mtype=='mall':
            url='http://stockapp.finance.qq.com/mstats/?pgv_ref=fi_quote_navi_bar#mod=list&id=qh&module=QH&type=ALL&page=1&max=80'

        self.driver.get(url)
        waitForLoad(self.driver)
        dataset=[]
        for _ in range(2):
            listbd=self.driver.find_elements_by_xpath("//ul[@id='list-body']/li")
            
            for lbd in listbd:
                try:
                    ss=lbd.text
                    ss=ss.split('\n')
                    dataset.append(ss)
                except Exception as e:
                    print(e)
                    break
            try:
                self.driver.find_element_by_link_text("下一页").click()
                waitForLoad(self.driver)
            except:
                pass

        df=pd.DataFrame(dataset)
        try:
            df.columns=['name','price','Chg%','high','low','tradeday','time']
        except:
            pass

        return df        

    def Exchange(self,mtype='all'):
        """获得汇率信息
        """
        if mtype == 'base':
            url='http://stockapp.finance.qq.com/mstats/?pgv_ref=fi_quote_navi_bar#mod=list&id=exchange_base&module=ER&type=BASE'
        elif mtype=='all':
            url='http://stockapp.finance.qq.com/mstats/?pgv_ref=fi_quote_navi_bar#mod=list&id=exchange&module=ER&type=ALL&max=80'
        elif mtype == 'cross':
            url='http://stockapp.finance.qq.com/mstats/?pgv_ref=fi_quote_navi_bar#mod=list&id=exchange_cross&module=ER&type=CROSS'

        self.driver.get(url)
        waitForLoad(self.driver)
        dataset=[]
        for _ in range(2):
            listbd=self.driver.find_elements_by_xpath("//ul[@id='list-body']/li")
            
            for lbd in listbd:
                try:
                    ss=lbd.text
                    ss=ss.split('\n')
                    dataset.append(ss)
                except Exception as e:
                    print(e)
                    break
            try:
                self.driver.find_element_by_link_text("下一页").click()
                waitForLoad(self.driver)
            except:
                pass

        df=pd.DataFrame(dataset)
        df.columns=['code','name','price','Chg%','Chg','high','low','pre.close','open','buy','sell','time']

        return df

    def get_industry_shares(self,indu):
        if self.concept is None:
            df=self.read_conceptid()

        dataset=pd.DataFrame()
        
        for code in ddd['code']:
            code=code[2:]
            dd=wd.get_finance_index_ths(code)
            print(dd.head())
            dd=dd.iloc[:4,:]
            dataset=dataset.append(dd)

        return dataset

    def index_cmpst(self):
        """指数的涨跌情况 """
        url='http://stockapp.finance.qq.com/mstats/#mod=list&id=idx&module=IDX'
        self.driver.get(url)
        waitForLoad(self.driver)
        
        dataset=[]

        for _ in range(2):
            listbd=self.driver.find_elements_by_xpath("//ul[@id='list-body']/li")
            
            for lbd in listbd:
                try:
                    ss=lbd.text
                    ss=ss.split('\n')
                    idd=re.findall('s[h|z]\d+',lbd.get_attribute('id'))[0]
                    ss.append('xdi_'+idd)
                    #print(ss)
                    dataset.append(ss)
                except Exception as e:
                    print(e)
                    break
            self.driver.find_element_by_link_text("下一页").click()
            waitForLoad(self.driver)
            
        df=pd.DataFrame(dataset)
        df=df.drop_duplicates()
        df.columns=['code','name','avg_price','Chg%','Chg','buy','sell','volume','amount','open','pre.close','high','low','id']
        if self.indexcmpst is None:
            self.indexcmpst=df
        else:
            self.indexcmpst=self.indexcmpst.append(df)

        self.indexcmpst.drop_duplicates(keep='last',inplace=True)
        return self.indexcmpst
    
    def get_index_cmpst_info(self,mtype):
        if self.indexcmpst is None:
            df=self.index_cmpst()
        if mtype in df.loc['name',:]:
            idd=df.loc['name','id']
            
        url="http://stockapp.finance.qq.com/mstats/#mod=list&id={0}&module=SS".format(idd)
        
    def unforbid(self,code=None):
        """
        大小非解禁时间表
        """
        df=wd.get_TobefreeTrade_qq(code)

        return df

    def forcast(self,report='20170630'):
        """获取企业的业绩预告信息"""
        df=wd.get_forcast_qq(report=report)
        return df

    def finance_index(self,rpday='20170630'):
        """获取年报季报的基本指标数据，按年获取    """
        df=wd.get_finance_index_qq(rpday=rpday)
        return df

    def longhub(self,start=None,end=None):
        """查看龙虎榜的信息"""
        df=wd.get_drogan_tiger_qq(start=start,end=end)
        return df

    def dazongjy(self,start='20010120'):
        """大宗交易"""
        df=wd.get_bigtradeinfo_qq(start=start)
        return df

    def industry_cashfl(self,mtype=1):
        """获取交易日当天的板块资金流动情况"""
        df=wd.get_cashfl_industry_qq(mtype=mtype)
        return df
    
if __name__=="__main__":
    qa=QQSource()
    

