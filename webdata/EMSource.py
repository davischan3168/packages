#!/usr/bin/env python3
# -*-coding:utf-8-*-

import webdata as wd
import sys

class EMSource(object):
    def __init__(self,code=None):
        self.__code=code

    def setcode(self,code):
        self.__code=code

    def tradinghk(self):
        df=wd.HK_trade_data_EM(self.__code)
        return df

    def fsummaryhk(self):
        df=wd.HK_Summary_EM(self.__code)
        return df

    def pvhk(self):
        df=wd.HK_Preview_EM(self.__code)
        return df

    def epsindexhk(self):
        df=wd.HK_EPS_Index_EM(self.__code)
        return df

    def captitalrepayhk(self):
        df=wd.HK_Captital_Repay_EM(self.__code)
        return df

    def growhk(self):
        df=wd.HK_Grow_Ability_EM(self.__code)
        return df

    def BShk(self):
        df=wd.HK_Balance_Sheet_EM(self.__code)
        return df

    def Incomehk(self):
        df=wd.HK_Income_EM(self.__code)
        return df

    def CFhk(self):
        df=wd.HK_Cash_Flow_EM(self.__code)
        return df
    
    def ValueAsshk(self):
        df=wd.HK_Value_Ass_EM(self.__code)
        return df

    def basicInfo(self):
        df=wd.HK_Basic_info_EM(self.__code)
        return df

    def divhk(self):
        df=wd.HK_dividend_EM(self.__code)
        return df
    
    def previewhk(self):
        df=wd.HK_Preview_EM(self.__code)
        return df
    
    def coreconcept(self):
        df=wd.get_coreconcept_f10_EM(self.__code)
        return df
    def industryanalys(self):
        df=wd.get_IndustryAnalysis_f10_EM(self.__code)
        return df
    def sharegroup(self):
        df=wd.get_sharesGroupby_f10_EM(self.__code)
        return df
    def bussiness(self):
        df=wd.get_bussiAnalys_f10_EM(self.__code)
        return df
    
if __name__=="__main__":
    em=EMSource(sys.argv[1])
