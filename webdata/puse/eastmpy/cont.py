#!/usr/bin/env python3
# -*-coding:utf-8-*-

import datetime as dt
import sys

PY3 = (sys.version_info[0] >= 3)

def _tofl(x):
    try:
        if ',' in x:
            x=x.replace(',','')
        if '%' in x:
            x=x.replace('%','')
        if '万' in x:
            x=x.replace('万','')
            x=float(x)*10000
        if '亿' in x:
            x=x.replace('亿','')
            x=float(x)*100000000            
        return float(x)
    except:
        return x

today=dt.datetime.today()

year1=list(range(today.year+1))
year2=list(range(today.year-10))
hh=[str(s) for s in year1 if s not in year2]
hh.reverse()
yearl=','.join(hh)

Review_url='http://hkf10.eastmoney.com/F9HKStock/GetStockBussinessViewList.do?securityCode={0}.HK&yearList={1}&dateSearchType=1&=0&rotate=0&seperate=0&order=desc&cashType=0&exchangeValue=0'

Future_url='http://hkf10.eastmoney.com/F9HKStock/GetStockBussinessFutureViewList.do?securityCode={0}.HK&yearList={1}&dateSearchType=1&=0&rotate=0&seperate=0&order=desc&cashType=0&exchangeValue=0'

VA_url='http://hkf10.eastmoney.com/F9HKStock/GetValueAssessment.do?securityCode={0}.HK&curType=CNY&yearList={1}&dateSearchType=1&rotate=0&seperate=0&order=desc&cashType=0&exchangeValue=0&customSelect=0&CurrencySelect=1'

AH_url='http://hkf10.eastmoney.com/F9HKStock/GetStockAHShareTradeList.do?securityCode={0}.HK&yearList={1},{2}&dateSearchType=3&rotate=1&seperate=0&order=asc&cashType=0&exchangeValue=0&customSelect=0&CurrencySelect=0'
#1为起始时间,2016-07-26,2为截止时间2017-07-03

bs_url='http://hkf10.eastmoney.com/F9HKStock/GetFinanceAssetData.do?securityCode={0}.HK&comType=127000000606281483&yearList={1}&reportTypeList=1,5,3,6&dateSearchType=1&listedType=0,1&reportTypeInScope=1&reportType=0&rotate=0&seperate=0&order=desc&cashType=1&exchangeValue=1&customSelect=0&CurrencySelect=0'

profit_url='http://hkf10.eastmoney.com/F9HKStock/GetFinanceProfitData.do?securityCode={0}.HK&comType=127000000606280264&yearList={1}&reportTypeList=1,5,3,6&dateSearchType=1&listedType=0,1&reportTypeInScope=1&reportType=0&rotate=0&seperate=0&order=desc&cashType=1&exchangeValue=1&customSelect=0&CurrencySelect=0'

cfl_url='http://hkf10.eastmoney.com/F9HKStock/GetFinanceCashFlowData.do?securityCode={0}.HK&yearList={1}&reportTypeList=1,5,3,6&dateSearchType=1&listedType=0,1&reportTypeInScope=1&reportType=0&rotate=0&seperate=0&order=desc&cashType=1&exchangeValue=1&customSelect=0&CurrencySelect=0'

fas_url='http://hkf10.eastmoney.com/F9HKStock/GetAnalysisSummaryData.do?securityCode={0}.HK&yearList={1}&reportTypeList=1,5,3,6&dateSearchType=1&listedType=0,1&reportTypeInScope=1&reportType=0&rotate=0&seperate=0&order=desc&cashType=0&exchangeValue=0&customSelect=0&CurrencySelect=0'

eps_index='http://hkf10.eastmoney.com/F9HKStock/GetEachStockData.do?securityCode={0}.HK&yearList={1}&reportTypeList=1,5,3,6&dateSearchType=1&listedType=0,1&reportTypeInScope=1&reportType=0&rotate=0&seperate=0&order=desc&cashType=0&exchangeValue=0&customSelect=0&CurrencySelect=0'

ylnl_sy_url='http://hkf10.eastmoney.com/F9HKStock/GetProfitAndQuantityData.do?securityCode={0}.HK&yearList={1}&reportTypeList=1,5,3,6&dateSearchType=1&listedType=0,1&reportTypeInScope=1&rotate=0&seperate=0&order=desc&cashType=0&exchangeValue=0&customSelect=0&CurrencySelect=0'

zbjg_cznl_url='http://hkf10.eastmoney.com/F9HKStock/GetCapitalAndRepayData.do?securityCode={0}.HK&yearList={1}&reportTypeList=1,5,3,6&dateSearchType=1&listedType=0,1&reportTypeInScope=1&reportType=0&rotate=0&seperate=0&order=desc&cashType=0&exchangeValue=0&customSelect=0&CurrencySelect=0'

cznl_url='http://hkf10.eastmoney.com/F9HKStock/GetGrowthAbilityData.do?securityCode={0}.HK&yearList={1}&reportTypeList=1,5,3,6&dateSearchType=1&listedType=0,1&reportTypeInScope=1&reportType=0&rotate=0&seperate=0&order=desc&cashType=0&exchangeValue=0&customSelect=0&CurrencySelect=0'

div_url='http://hkf10.eastmoney.com/F9HKStock/GetStockBonusList.do?securityCode={0}.HK&yearList={1}&reportTypeList=1,5,3,6&dateSearchType=1&rotate=0&seperate=0&order=desc&cashType=0&exchangeValue=0&customSelect=0&CurrencySelect=0'

buy_back_url='http://hkf10.eastmoney.com/F9HKStock/GetStockRepurchaseList.do?securityCode={0}.HK&yearList={1}&reportTypeList=1,5,3,6&dateSearchType=1&rotate=0&seperate=0&order=asc&cashType=0&exchangeValue=0&customSelect=0&CurrencySelect=0'

div_url='http://hkf10.eastmoney.com/F9HKStock/GetStockBonusList.do?securityCode={0}.HK&yearList={1}&reportTypeList=1,5,3,6&dateSearchType=1&rotate=0&seperate=0&order=desc&cashType=0&exchangeValue=0&customSelect=0&CurrencySelect=0'

split_url='http://hkf10.eastmoney.com/F9HKStock/GetStockShareSpiltReportList.do?securityCode={0}.HK&yearList={1}&reportTypeList=1,5,3,6&dateSearchType=1&rotate=0&seperate=0&order=asc&cashType=0&exchangeValue=0&customSelect=0&CurrencySelect=0'

hk_list='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._HKS&sty=FCOQB&sortType=C&sortRule=-1&page=1&pageSize=200000&js=var%20quote_123%3d{rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.21014565241026273'

hk_ls_name=['code','name','price','chg','chg%','volume','amount','open','high','low','pre_close','date']

HSGT_url={'HGT':'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGTHIS&token=70f12f2f4f091e459a279469fe49eca5&filter=(MarketType=1)&js=var%20yUMiNQGB={1}&ps=20000&p={0}&sr=-1&st=DetailDate&rt=49986371',
          'SGT':'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGTHIS&token=70f12f2f4f091e459a279469fe49eca5&filter=(MarketType=3)&js=var%20wAZmBSgm={1}&ps=20000&p={0}&sr=-1&st=DetailDate&rt=49986373',
          'GHT':'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGTHIS&token=70f12f2f4f091e459a279469fe49eca5&filter=(MarketType=2)&js=var%20JzHDbajS={1}&ps=20000&p={0}&sr=-1&st=DetailDate&rt=49986380',
          'GST':'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=HSGTHIS&token=70f12f2f4f091e459a279469fe49eca5&filter=(MarketType=4)&js=var%20UdBMCRKh={1}&ps=20000&p={0}&sr=-1&st=DetailDate&rt=49986383'}

invest_rating_url='http://hk.eastmoney.com/rating.html?code={0}&org=&rating=0'

bkurlsets={'2025规划': 'http://data.eastmoney.com/bkzj/BK0713.html',
 '3D打印': 'http://data.eastmoney.com/bkzj/BK0619.html',
 '3D玻璃': 'http://data.eastmoney.com/bkzj/BK0881.html',
 '5G概念': 'http://data.eastmoney.com/bkzj/BK0714.html',
 'AB股': 'http://data.eastmoney.com/bkzj/BK0498.html',
 'AH股': 'http://data.eastmoney.com/bkzj/BK0499.html',
 'B股': 'http://data.eastmoney.com/bkzj/BK0636.html',
 'HS300': 'http://data.eastmoney.com/bkzj/BK0500.html',
 'IPO受益': 'http://data.eastmoney.com/bkzj/BK0697.html',
 'LED': 'http://data.eastmoney.com/bkzj/BK0580.html',
 'MSCI中国': 'http://data.eastmoney.com/bkzj/BK0821.html',
 'OLED': 'http://data.eastmoney.com/bkzj/BK0840.html',
 'PPP模式': 'http://data.eastmoney.com/bkzj/BK0721.html',
 'QFII重仓': 'http://data.eastmoney.com/bkzj/BK0535.html',
 'ST概念': 'http://data.eastmoney.com/bkzj/BK0511.html',
 'S股': 'http://data.eastmoney.com/bkzj/BK0503.html',
 '一带一路': 'http://data.eastmoney.com/bkzj/BK0712.html',
 '上海板块': 'http://data.eastmoney.com/bkzj/BK0145.html',
 '上海自贸': 'http://data.eastmoney.com/bkzj/BK0643.html',
 '上证180': 'http://data.eastmoney.com/bkzj/BK0612.html',
 '上证380': 'http://data.eastmoney.com/bkzj/BK0705.html',
 '上证50': 'http://data.eastmoney.com/bkzj/BK0611.html',
 '专用设备': 'http://data.eastmoney.com/bkzj/BK0910.html',
 '中字头': 'http://data.eastmoney.com/bkzj/BK0505.html',
 '中药': 'http://data.eastmoney.com/bkzj/BK0615.html',
 '中证500': 'http://data.eastmoney.com/bkzj/BK0701.html',
 '中超概念': 'http://data.eastmoney.com/bkzj/BK0635.html',
 '举牌概念': 'http://data.eastmoney.com/bkzj/BK0685.html',
 '二胎概念': 'http://data.eastmoney.com/bkzj/BK0664.html',
 '云南板块': 'http://data.eastmoney.com/bkzj/BK0171.html',
 '云计算': 'http://data.eastmoney.com/bkzj/BK0579.html',
 '互联金融': 'http://data.eastmoney.com/bkzj/BK0637.html',
 '交运物流': 'http://data.eastmoney.com/bkzj/BK0422.html',
 '交运设备': 'http://data.eastmoney.com/bkzj/BK0429.html',
 '京津冀': 'http://data.eastmoney.com/bkzj/BK0684.html',
 '人工智能': 'http://data.eastmoney.com/bkzj/BK0800.html',
 '人脑工程': 'http://data.eastmoney.com/bkzj/BK0706.html',
 '仪器仪表': 'http://data.eastmoney.com/bkzj/BK0458.html',
 '体育产业': 'http://data.eastmoney.com/bkzj/BK0708.html',
 '保险': 'http://data.eastmoney.com/bkzj/BK0474.html',
 '债转股': 'http://data.eastmoney.com/bkzj/BK0980.html',
 '健康中国': 'http://data.eastmoney.com/bkzj/BK0719.html',
 '充电桩': 'http://data.eastmoney.com/bkzj/BK0700.html',
 '免疫治疗': 'http://data.eastmoney.com/bkzj/BK0698.html',
 '全息技术': 'http://data.eastmoney.com/bkzj/BK0699.html',
 '公用事业': 'http://data.eastmoney.com/bkzj/BK0427.html',
 '共享经济': 'http://data.eastmoney.com/bkzj/BK0807.html',
 '养老概念': 'http://data.eastmoney.com/bkzj/BK0653.html',
 '养老金': 'http://data.eastmoney.com/bkzj/BK0823.html',
 '内蒙古': 'http://data.eastmoney.com/bkzj/BK0175.html',
 '军工': 'http://data.eastmoney.com/bkzj/BK0490.html',
 '军民融合': 'http://data.eastmoney.com/bkzj/BK0808.html',
 '农牧饲渔': 'http://data.eastmoney.com/bkzj/BK0433.html',
 '农药兽药': 'http://data.eastmoney.com/bkzj/BK0730.html',
 '创业成份': 'http://data.eastmoney.com/bkzj/BK0638.html',
 '创业板综': 'http://data.eastmoney.com/bkzj/BK0742.html',
 '创投': 'http://data.eastmoney.com/bkzj/BK0506.html',
 '券商信托': 'http://data.eastmoney.com/bkzj/BK0473.html',
 '券商概念': 'http://data.eastmoney.com/bkzj/BK0711.html',
 '包装材料': 'http://data.eastmoney.com/bkzj/BK0733.html',
 '化工原料': 'http://data.eastmoney.com/bkzj/BK0512.html',
 '化工行业': 'http://data.eastmoney.com/bkzj/BK0538.html',
 '化纤行业': 'http://data.eastmoney.com/bkzj/BK0471.html',
 '化肥行业': 'http://data.eastmoney.com/bkzj/BK0731.html',
 '北京冬奥': 'http://data.eastmoney.com/bkzj/BK0717.html',
 '北京板块': 'http://data.eastmoney.com/bkzj/BK0150.html',
 '北斗导航': 'http://data.eastmoney.com/bkzj/BK0629.html',
 '区块链': 'http://data.eastmoney.com/bkzj/BK0830.html',
 '医疗器械': 'http://data.eastmoney.com/bkzj/BK0668.html',
 '医疗行业': 'http://data.eastmoney.com/bkzj/BK0727.html',
 '医药制造': 'http://data.eastmoney.com/bkzj/BK0465.html',
 '单抗概念': 'http://data.eastmoney.com/bkzj/BK0870.html',
 '参股保险': 'http://data.eastmoney.com/bkzj/BK0604.html',
 '参股券商': 'http://data.eastmoney.com/bkzj/BK0514.html',
 '参股期货': 'http://data.eastmoney.com/bkzj/BK0524.html',
 '参股银行': 'http://data.eastmoney.com/bkzj/BK0525.html',
 '可燃冰': 'http://data.eastmoney.com/bkzj/BK0818.html',
 '吉林板块': 'http://data.eastmoney.com/bkzj/BK0148.html',
 '商业百货': 'http://data.eastmoney.com/bkzj/BK0482.html',
 '四川板块': 'http://data.eastmoney.com/bkzj/BK0169.html',
 '园林工程': 'http://data.eastmoney.com/bkzj/BK0726.html',
 '国产芯片': 'http://data.eastmoney.com/bkzj/BK0891.html',
 '国产软件': 'http://data.eastmoney.com/bkzj/BK0696.html',
 '国企改革': 'http://data.eastmoney.com/bkzj/BK0683.html',
 '国家安防': 'http://data.eastmoney.com/bkzj/BK0667.html',
 '国际贸易': 'http://data.eastmoney.com/bkzj/BK0484.html',
 '土地流转': 'http://data.eastmoney.com/bkzj/BK0632.html',
 '在线教育': 'http://data.eastmoney.com/bkzj/BK0662.html',
 '在线旅游': 'http://data.eastmoney.com/bkzj/BK0692.html',
 '地热能': 'http://data.eastmoney.com/bkzj/BK0622.html',
 '基因测序': 'http://data.eastmoney.com/bkzj/BK0693.html',
 '基本金属': 'http://data.eastmoney.com/bkzj/BK0561.html',
 '基金重仓': 'http://data.eastmoney.com/bkzj/BK0536.html',
 '塑胶制品': 'http://data.eastmoney.com/bkzj/BK0454.html',
 '增强现实': 'http://data.eastmoney.com/bkzj/BK0801.html',
 '壳资源': 'http://data.eastmoney.com/bkzj/BK0820.html',
 '多元金融': 'http://data.eastmoney.com/bkzj/BK0738.html',
 '大数据': 'http://data.eastmoney.com/bkzj/BK0634.html',
 '大飞机': 'http://data.eastmoney.com/bkzj/BK0814.html',
 '天津板块': 'http://data.eastmoney.com/bkzj/BK0166.html',
 '太阳能': 'http://data.eastmoney.com/bkzj/BK0588.html',
 '央视50': 'http://data.eastmoney.com/bkzj/BK0610.html',
 '宁夏板块': 'http://data.eastmoney.com/bkzj/BK0162.html',
 '安徽板块': 'http://data.eastmoney.com/bkzj/BK0149.html',
 '安防设备': 'http://data.eastmoney.com/bkzj/BK0735.html',
 '家电行业': 'http://data.eastmoney.com/bkzj/BK0456.html',
 '小金属': 'http://data.eastmoney.com/bkzj/BK0695.html',
 '山东板块': 'http://data.eastmoney.com/bkzj/BK0164.html',
 '山西板块': 'http://data.eastmoney.com/bkzj/BK0167.html',
 '工业4.0': 'http://data.eastmoney.com/bkzj/BK0810.html',
 '工程建设': 'http://data.eastmoney.com/bkzj/BK0425.html',
 '工艺商品': 'http://data.eastmoney.com/bkzj/BK0440.html',
 '广东板块': 'http://data.eastmoney.com/bkzj/BK0153.html',
 '广西板块': 'http://data.eastmoney.com/bkzj/BK0154.html',
 '彩票概念': 'http://data.eastmoney.com/bkzj/BK0671.html',
 '快递概念': 'http://data.eastmoney.com/bkzj/BK0990.html',
 '成渝特区': 'http://data.eastmoney.com/bkzj/BK0534.html',
 '房地产': 'http://data.eastmoney.com/bkzj/BK0451.html',
 '手游概念': 'http://data.eastmoney.com/bkzj/BK0642.html',
 '文化传媒': 'http://data.eastmoney.com/bkzj/BK0486.html',
 '文教休闲': 'http://data.eastmoney.com/bkzj/BK0740.html',
 '新三板': 'http://data.eastmoney.com/bkzj/BK0600.html',
 '新材料': 'http://data.eastmoney.com/bkzj/BK0523.html',
 '新疆板块': 'http://data.eastmoney.com/bkzj/BK0147.html',
 '新能源': 'http://data.eastmoney.com/bkzj/BK0493.html',
 '新能源车': 'http://data.eastmoney.com/bkzj/BK0900.html',
 '旅游酒店': 'http://data.eastmoney.com/bkzj/BK0485.html',
 '无人机': 'http://data.eastmoney.com/bkzj/BK0704.html',
 '无人驾驶': 'http://data.eastmoney.com/bkzj/BK0802.html',
 '无线充电': 'http://data.eastmoney.com/bkzj/BK0960.html',
 '昨日涨停': 'http://data.eastmoney.com/bkzj/BK0815.html',
 '昨日触板': 'http://data.eastmoney.com/bkzj/BK0817.html',
 '昨日连板': 'http://data.eastmoney.com/bkzj/BK0816.html',
 '智慧城市': 'http://data.eastmoney.com/bkzj/BK0628.html',
 '智能家居': 'http://data.eastmoney.com/bkzj/BK0680.html',
 '智能机器': 'http://data.eastmoney.com/bkzj/BK0640.html',
 '智能电网': 'http://data.eastmoney.com/bkzj/BK0581.html',
 '智能电视': 'http://data.eastmoney.com/bkzj/BK0656.html',
 '智能穿戴': 'http://data.eastmoney.com/bkzj/BK0641.html',
 '有色金属': 'http://data.eastmoney.com/bkzj/BK0478.html',
 '木业家具': 'http://data.eastmoney.com/bkzj/BK0476.html',
 '机构重仓': 'http://data.eastmoney.com/bkzj/BK0552.html',
 '机械行业': 'http://data.eastmoney.com/bkzj/BK0545.html',
 '材料行业': 'http://data.eastmoney.com/bkzj/BK0537.html',
 '核能核电': 'http://data.eastmoney.com/bkzj/BK0577.html',
 '次新股': 'http://data.eastmoney.com/bkzj/BK0501.html',
 '民航机场': 'http://data.eastmoney.com/bkzj/BK0420.html',
 '氟化工': 'http://data.eastmoney.com/bkzj/BK0690.html',
 '水利建设': 'http://data.eastmoney.com/bkzj/BK0597.html',
 '水泥建材': 'http://data.eastmoney.com/bkzj/BK0424.html',
 '江苏板块': 'http://data.eastmoney.com/bkzj/BK0159.html',
 '江西板块': 'http://data.eastmoney.com/bkzj/BK0160.html',
 '汽车行业': 'http://data.eastmoney.com/bkzj/BK0481.html',
 '沪企改革': 'http://data.eastmoney.com/bkzj/BK0672.html',
 '沪港通': 'http://data.eastmoney.com/bkzj/BK0702.html',
 '沪股通': 'http://data.eastmoney.com/bkzj/BK0707.html',
 '河北板块': 'http://data.eastmoney.com/bkzj/BK0155.html',
 '河南板块': 'http://data.eastmoney.com/bkzj/BK0156.html',
 '油价相关': 'http://data.eastmoney.com/bkzj/BK0563.html',
 '油改概念': 'http://data.eastmoney.com/bkzj/BK0663.html',
 '油气设服': 'http://data.eastmoney.com/bkzj/BK0606.html',
 '浙江板块': 'http://data.eastmoney.com/bkzj/BK0172.html',
 '海南板块': 'http://data.eastmoney.com/bkzj/BK0176.html',
 '海工装备': 'http://data.eastmoney.com/bkzj/BK0601.html',
 '海洋经济': 'http://data.eastmoney.com/bkzj/BK0623.html',
 '海绵城市': 'http://data.eastmoney.com/bkzj/BK0724.html',
 '深圳特区': 'http://data.eastmoney.com/bkzj/BK0549.html',
 '深成500': 'http://data.eastmoney.com/bkzj/BK0568.html',
 '深港通': 'http://data.eastmoney.com/bkzj/BK0930.html',
 '深股通': 'http://data.eastmoney.com/bkzj/BK0804.html',
 '深证100R': 'http://data.eastmoney.com/bkzj/BK0743.html',
 '港口水运': 'http://data.eastmoney.com/bkzj/BK0450.html',
 '湖北板块': 'http://data.eastmoney.com/bkzj/BK0157.html',
 '湖南板块': 'http://data.eastmoney.com/bkzj/BK0158.html',
 '滨海新区': 'http://data.eastmoney.com/bkzj/BK0566.html',
 '煤化工': 'http://data.eastmoney.com/bkzj/BK0492.html',
 '煤炭采选': 'http://data.eastmoney.com/bkzj/BK0437.html',
 '燃料电池': 'http://data.eastmoney.com/bkzj/BK0682.html',
 '物联网': 'http://data.eastmoney.com/bkzj/BK0554.html',
 '特斯拉': 'http://data.eastmoney.com/bkzj/BK0644.html',
 '独家药品': 'http://data.eastmoney.com/bkzj/BK0676.html',
 '猪肉概念': 'http://data.eastmoney.com/bkzj/BK0882.html',
 '环保工程': 'http://data.eastmoney.com/bkzj/BK0728.html',
 '玻璃陶瓷': 'http://data.eastmoney.com/bkzj/BK0546.html',
 '珠宝首饰': 'http://data.eastmoney.com/bkzj/BK0734.html',
 '甘肃板块': 'http://data.eastmoney.com/bkzj/BK0152.html',
 '生态农业': 'http://data.eastmoney.com/bkzj/BK0669.html',
 '生物疫苗': 'http://data.eastmoney.com/bkzj/BK0548.html',
 '生物识别': 'http://data.eastmoney.com/bkzj/BK0970.html',
 '电信运营': 'http://data.eastmoney.com/bkzj/BK0736.html',
 '电力行业': 'http://data.eastmoney.com/bkzj/BK0428.html',
 '电商概念': 'http://data.eastmoney.com/bkzj/BK0665.html',
 '电子信息': 'http://data.eastmoney.com/bkzj/BK0447.html',
 '电子元件': 'http://data.eastmoney.com/bkzj/BK0459.html',
 '病毒防治': 'http://data.eastmoney.com/bkzj/BK0675.html',
 '皖江区域': 'http://data.eastmoney.com/bkzj/BK0589.html',
 '石墨烯': 'http://data.eastmoney.com/bkzj/BK0617.html',
 '石油行业': 'http://data.eastmoney.com/bkzj/BK0464.html',
 '社保重仓': 'http://data.eastmoney.com/bkzj/BK0520.html',
 '福建板块': 'http://data.eastmoney.com/bkzj/BK0151.html',
 '租售同权': 'http://data.eastmoney.com/bkzj/BK0822.html',
 '移动支付': 'http://data.eastmoney.com/bkzj/BK0556.html',
 '稀土永磁': 'http://data.eastmoney.com/bkzj/BK0578.html',
 '稀缺资源': 'http://data.eastmoney.com/bkzj/BK0519.html',
 '粤港自贸': 'http://data.eastmoney.com/bkzj/BK0677.html',
 '精准医疗': 'http://data.eastmoney.com/bkzj/BK0806.html',
 '纺织服装': 'http://data.eastmoney.com/bkzj/BK0436.html',
 '综合行业': 'http://data.eastmoney.com/bkzj/BK0539.html',
 '网红直播': 'http://data.eastmoney.com/bkzj/BK0940.html',
 '网络安全': 'http://data.eastmoney.com/bkzj/BK0655.html',
 '网络游戏': 'http://data.eastmoney.com/bkzj/BK0509.html',
 '美丽中国': 'http://data.eastmoney.com/bkzj/BK0626.html',
 '股权激励': 'http://data.eastmoney.com/bkzj/BK0567.html',
 '股权转让': 'http://data.eastmoney.com/bkzj/BK0803.html',
 '腾安价值': 'http://data.eastmoney.com/bkzj/BK0681.html',
 '航天航空': 'http://data.eastmoney.com/bkzj/BK0480.html',
 '航母概念': 'http://data.eastmoney.com/bkzj/BK0715.html',
 '船舶制造': 'http://data.eastmoney.com/bkzj/BK0729.html',
 '节能环保': 'http://data.eastmoney.com/bkzj/BK0494.html',
 '苹果概念': 'http://data.eastmoney.com/bkzj/BK0666.html',
 '草甘膦': 'http://data.eastmoney.com/bkzj/BK0950.html',
 '蓝宝石': 'http://data.eastmoney.com/bkzj/BK0674.html',
 '虚拟现实': 'http://data.eastmoney.com/bkzj/BK0722.html',
 '融资融券': 'http://data.eastmoney.com/bkzj/BK0596.html',
 '装修装饰': 'http://data.eastmoney.com/bkzj/BK0725.html',
 '西藏板块': 'http://data.eastmoney.com/bkzj/BK0174.html',
 '触摸屏': 'http://data.eastmoney.com/bkzj/BK0583.html',
 '证金持股': 'http://data.eastmoney.com/bkzj/BK0718.html',
 '贬值受益': 'http://data.eastmoney.com/bkzj/BK0812.html',
 '贵州板块': 'http://data.eastmoney.com/bkzj/BK0173.html',
 '贵金属': 'http://data.eastmoney.com/bkzj/BK0732.html',
 '赛马概念': 'http://data.eastmoney.com/bkzj/BK0709.html',
 '超导概念': 'http://data.eastmoney.com/bkzj/BK0679.html',
 '超级品牌': 'http://data.eastmoney.com/bkzj/BK0811.html',
 '超级电容': 'http://data.eastmoney.com/bkzj/BK0703.html',
 '车联网': 'http://data.eastmoney.com/bkzj/BK0920.html',
 '转债标的': 'http://data.eastmoney.com/bkzj/BK0528.html',
 '软件服务': 'http://data.eastmoney.com/bkzj/BK0737.html',
 '输配电气': 'http://data.eastmoney.com/bkzj/BK0457.html',
 '辽宁板块': 'http://data.eastmoney.com/bkzj/BK0161.html',
 '迪士尼': 'http://data.eastmoney.com/bkzj/BK0540.html',
 '送转预期': 'http://data.eastmoney.com/bkzj/BK0633.html',
 '通用航空': 'http://data.eastmoney.com/bkzj/BK0625.html',
 '通讯行业': 'http://data.eastmoney.com/bkzj/BK0448.html',
 '造纸印刷': 'http://data.eastmoney.com/bkzj/BK0470.html',
 '酿酒行业': 'http://data.eastmoney.com/bkzj/BK0477.html',
 '重庆板块': 'http://data.eastmoney.com/bkzj/BK0170.html',
 '量子通信': 'http://data.eastmoney.com/bkzj/BK0710.html',
 '金属制品': 'http://data.eastmoney.com/bkzj/BK0739.html',
 '钛白粉': 'http://data.eastmoney.com/bkzj/BK0805.html',
 '钢铁行业': 'http://data.eastmoney.com/bkzj/BK0479.html',
 '铁路基建': 'http://data.eastmoney.com/bkzj/BK0592.html',
 '银行': 'http://data.eastmoney.com/bkzj/BK0475.html',
 '锂电池': 'http://data.eastmoney.com/bkzj/BK0574.html',
 '长株潭': 'http://data.eastmoney.com/bkzj/BK0593.html',
 '长江三角': 'http://data.eastmoney.com/bkzj/BK0594.html',
 '阿里概念': 'http://data.eastmoney.com/bkzj/BK0689.html',
 '陕西板块': 'http://data.eastmoney.com/bkzj/BK0165.html',
 '雄安新区': 'http://data.eastmoney.com/bkzj/BK0813.html',
 '青海板块': 'http://data.eastmoney.com/bkzj/BK0163.html',
 '页岩气': 'http://data.eastmoney.com/bkzj/BK0603.html',
 '预亏预减': 'http://data.eastmoney.com/bkzj/BK0570.html',
 '预盈预增': 'http://data.eastmoney.com/bkzj/BK0571.html',
 '风能': 'http://data.eastmoney.com/bkzj/BK0595.html',
 '食品安全': 'http://data.eastmoney.com/bkzj/BK0614.html',
 '食品饮料': 'http://data.eastmoney.com/bkzj/BK0438.html',
 '高校': 'http://data.eastmoney.com/bkzj/BK0491.html',
 '高送转': 'http://data.eastmoney.com/bkzj/BK0723.html',
 '高速公路': 'http://data.eastmoney.com/bkzj/BK0421.html',
 '黄金概念': 'http://data.eastmoney.com/bkzj/BK0547.html',
 '黑龙江': 'http://data.eastmoney.com/bkzj/BK0146.html'}
