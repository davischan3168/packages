#!/usr/bin/env python3
# -*-coding:utf-8-*-

def _tofl(x):
    try:
        x=x.replace('\t','').replace('%','')
        if x.strip()=='':
            x=np.nan
            return x
        else:
            return float(x)
    except:
        return x
    
income='http://quotes.money.163.com/service/gszl_%s.html?type=%s'
#收入构成历史数据的下载地址（按产品(cp)、行业（hy）、地域(dy)划分）

mainindex_url='http://quotes.money.163.com/service/zycwzb_%s.html?type=%s'
#主要财务指标,type的值为report,year,season三个值。

finance_analysis_url='http://quotes.money.163.com/service/zycwzb_{0}.html?type={1}&part={2}'
#主要财务指标分析（part-->,ylnl(盈利能力),chnl(偿还能力)、yynl(营运能力)、
#cznl(成长能力))\type的值为report,year,season三个值


finace_summary_url={'report':'http://quotes.money.163.com/service/cwbbzy_{0}.html','year':'http://quotes.money.163.com/service/cwbbzy_{0}.html?type=year'}
#财务报表摘要,分为按报告期和按年的数据。

bic_url={'report':'http://quotes.money.163.com/service/{1}_{0}.html','year':'http://quotes.money.163.com/service/{1}_{0}.html?type=year'}
#资产负债表（zcfzb)\利润表(lrb)\现金流量表(xjllb),分为按报告期和按年的数据。

trading={'sh':'http://quotes.money.163.com/service/chddata.html?code=0{0}&start={1}&end={2}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP','sz':'http://quotes.money.163.com/service/chddata.html?code=1{0}&start={1}&end={2}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP','gme':'http://quotes.money.163.com/service/chddata.html?code=1{0}&start={1}&end={2}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'}
#历史交易数据,开始时间19990626,截止时间20170620

cashf_url='http://quotes.money.163.com/service/zjlx_chart.html?symbol={0}'
#资金流向

cash_thy_url='http://quotes.money.163.com/service/zjlx_table.html?symbol={0}&type={1}'
#同行业的资金流入及流出情况，type的参数为zc(流入最多）和jc（流出最多）

notice_url='http://quotes.money.163.com/f10/gsgg_{0},{1}.html'
#1,mytype:zxgg,ipo,gbbd,fhrz

new_url='http://quotes.money.163.com/f10/gsxw_{0}.html'

base='http://quotes.money.163.com'
