#!/usr/bin/env python3
# -*-coding:utf-8-*-

import webdata as wd

class Sina(object):
    def get_k_data(self,code):
        """
        股票价格
        """
        return

    def Fc_data(self,code):
        """
        国内期货
        """
        df = wd.FC_hday(code)
        return df

    def Gc_data(self,code):
        """
        国外期货
        """
        df = wd.FC_ghday(code)
        return df
    def If_data(self,code):
        """股指期货"""
        df = wd.IF_hday(code)
        return df

    def BigTrade(self,code):
        """大宗交易"""
        df = wd.dzjy_share(code)
        return df

    def BS(self,code):
        """资产负债表"""
        df = wd.BS_sina(code)
        return df

    def IS(self,code):
        """利润表"""
        df = wd.IS_sina(code)
        return df
    
    def CS(self,code):
        """现金流量表"""
        df = wd.CS_sina(code)
        return df
    
    def FIndex(self,code):
        """财务指标"""
        df = wd.FI_sina(code)
        return df        

    def Dadan(self,code,opt1=1):
        "大单"
        df=wd.get_dadan_sina(code,opt=opt1)
        return df

    def margin(self,code):
        """获得公司的融资融券的数据"""
        df=wd.margins_share(code)
        return df

    def dividend(self,code):
        """查询公司的分红情况"""
        df=wd.get_div(code)
        return df

    def Margin(self,code):
        """查询融资融券情况"""
        df=wd.margins_share(code)

    def holders(self,code,year,quarter):
        """查询机构持股情况"""

        return

if __name__=="__main__":
    aa=Sina()
