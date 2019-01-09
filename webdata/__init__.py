__version__ = '0.5.0'
__author__ = 'Davis Chan'

"""
for trading data
"""
from webdata.stock.trading import (get_hist_data, get_tick_data,
                                   get_today_all, get_realtime_quotes,
                                   get_h_data, get_today_ticks,
                                   get_index, get_hists,
                                    get_k_data,bar,get_day_all,
                                   get_sina_dd, bar, tick,
                                   get_markets, quotes,
                                   get_instrument, reset_instrument)

"""
for trading data
"""
from webdata.stock.fundamental import (get_stock_basics, get_report_data,
                                       get_profit_data,
                                       get_operation_data, get_growth_data,
                                        get_debtpaying_data, get_cashflow_data,
                                        get_balance_sheet, get_profit_statement, get_cash_flow)

"""
for macro data
"""
from webdata.stock.macro import (get_gdp_year, get_gdp_quarter,
                                 get_gdp_for, get_gdp_pull,
                                 get_gdp_contrib, get_cpi,
                                 get_ppi, get_deposit_rate,
                                 get_loan_rate, get_rrr,
                                 get_money_supply, get_money_supply_bal)

"""
for classifying data
"""
from webdata.stock.classifying import (get_industry_classified, get_concept_classified,
                                       get_area_classified, get_gem_classified,
                                       get_sme_classified, get_st_classified,
                                       get_hs300s, get_sz50s, get_zz500s,
                                       get_terminated, get_suspended)

"""
for macro data
"""
from webdata.stock.newsevent import (get_latest_news, latest_content,
                                     get_notices, notice_content,
                                     guba_sina)

"""
for reference
"""
from webdata.stock.reference import (profit_data, forecast_data,
                                     xsg_data, fund_holdings,
                                     new_stocks, sh_margins,
                                     sh_margin_details,
                                     sz_margins, sz_margin_details,
                                     top10_holders, profit_divis,
                                     moneyflow_hsgt, margin_detail,
                                     margin_target, margin_offset,
                                     margin_zsl, stock_issuance,
                                     stock_pledged, pledged_detail)                                     

"""
for shibor
"""
from webdata.stock.shibor import (shibor_data, shibor_quote_data,
                                  shibor_ma_data, lpr_data,
                                  lpr_ma_data)

"""
for LHB
"""
from webdata.stock.billboard import (top_list, cap_tops, broker_tops,
                                     inst_tops, inst_detail)


"""
for utils
"""
from webdata.util.dateu import (trade_cal,is_holiday)
from webdata.util.chrome_cookies import (firefox_cookies,chrome_cookieswin,
                                             chrome_cookies,chrome_cookies_win)

"""
for DataYes Token
"""
from webdata.util.upass import (set_token, get_token, get_broker,
                                set_broker, remove_broker)

#from webdata.datayes.api import *

from webdata.internet.boxoffice import (realtime_boxoffice, day_boxoffice,
                                        day_cinema, month_boxoffice)

"""
for fund data
"""
from webdata.fund.nav import (get_nav_open, get_nav_close, get_nav_grading,
                              get_nav_history, get_fund_info)

"""
for trader API
"""
from webdata.trader.trader import TraderAPI

"""
for futures API
"""
from webdata.futures.intlfutures import (get_intlfuture)

from webdata.coins.market import (coins_tick, coins_bar,
                                  coins_snapshot, coins_trade)

from webdata.util.conns import get_apis
from webdata.util.candle import pandas_candlestick_ohlc
from webdata.util.mdiff import diff_2files_html
#for person aastock.com
from webdata.puse.aastock import (HK_firatio_data_AAST,HK_code_HKEX,
                                  HK_bsheet_data_AAST, get_mainindex_data, 
                                  HK_earsummary_data_AAST,get_law,
                                  HK_buyback_data_AAST, get_HSI_index,
                                  HK_divs_AAST, summit_for_ipo,
                                  HK_cashfl_AAST,
                                  summit_for_ipoII,get_law_wenshu,
                                  download_file, all_invest_mainindex,
                                  all_invest_mainindexII)

"""
for eastmoney data
"""
from webdata.puse.eastmpy.eastmoney import (get_currency_data, get_hangye_list,
                                    get_diyu_list,get_gainian_list,
                                    get_usa_list, get_all_list,
                                    get_cashflow_em10days,get_dividen_allshare_EM,
                                    get_cashflow_em3days,div_share,
                                    get_cashflow_em5days,div_share_mkra,
                                    get_cashflow_emnow,holdby_total,
                                    get_cashflow_emshare,holdby_detail,
                                    get_global_index, get_global_index,
                                    get_mainland_index, get_mainland_index,
                                    get_ha_trading_data, get_hhist_data,
                                    get_ghist_data, get_hbf_t, comp2indu,
                                    get_hbf_d)


"""
for sina data
"""
from webdata.puse.sinapy.sina import (get_sina_pepb, get_hangye_sina,
                               get_gainian_sina, get_zjh_sina,
                               get_share_all_sina, get_news, get_news_content,
                               get_share_percode_sina,index_hist_data,
                               get_hk_trading_sina,
                               get_kzz_trading_sina,
                               get_hk_ha_trading_sina,
                               get_hk_hangye_trading_sina,
                               get_hk_hcg_trading_sina,
                               get_hk_gqg_trading_sina,
                               get_week_zd_sina, get_month_zd_sina,
                               #get_hmin_fc, get_hmin_if, get_hday_fc,
                               #get_hday_if,
                               get_ddV, get_ddA, get_ddT,
                               get_predict, get_predict_percode,
                               get_bonus_issue,
                               get_div)


from webdata.puse.sinapy.finace import (BS_sina, FI_sina, CS_sina, IS_sina)
from webdata.puse.sinapy.FO import (FC_realtime_sina, FC_hmin, IF_hmin,FC_hd,
                                    FC_hday,IF_hday,FC_ghday)
from webdata.puse.sinapy.predict import (get_predict_Sina,
                                         get_predict_share_Sina,
                                         get_researchRate_Sina)

#from webdata.puse.sinapy.trade import (US_datasina,get_dadan_sina,
#                                           HK_datasina,HK_datasina_byquarter)
from webdata.puse.sinapy.margins import margins_share
from webdata.puse.sinapy.newdata import (get_pepb_Sina)
"""
for jqka data 
"""
from webdata.puse.thspy.jqka import ( get_current_hu_ths,get_cashflow_thspershare,
                                get_current_hongk_ths,
                                get_cashflow_thsnow,
                                get_cashflow_ths3days,
                                get_cashflow_ths5days,
                                get_cashflow_ths10days,
                                get_cashflow_ths20days,
                                get_finance_index_ths,
                                HK_finance_ths)
                                    
"""
For person app
"""
"""
from webdata.puse.myapp import ( annlysis_shares_holdbyfund, get_myquandl,
                                 get_hist_csv, tongbi,huanbi,
                                 get_h_csv, tutlemethon,pplot_diff,
                                 analysis_kdjv1,OLSV2A,PdDataFrame_diff,
                                 OLSV2_HA,PdSeries_diff,PDdiff,OHLC
                                 )
"""
from webdata.puse.myapp import ( annlysis_shares_holdbyfund, get_myquandl,
                                 tongbi,huanbi,
                                 tutlemethon,pplot_diff,
                                 analysis_kdjv1,PdDataFrame_diff,
                                 PdSeries_diff,PDdiff,OHLC
                                 )

from webdata.puse.sinapy.margins import(margins_all,
                                 margins_share)

#from webdata.puse.quandldata import(quandld,
#                                    quandlyd)

from webdata.util.hds import ( user_agent, getipproxies, get_cookies,
                               get_proxies_ip)

from webdata.util.rw import(ReadFile,WriteFile,GBK_2_UTF8,pylatex,pydoc)
from webdata.util.txt2html import(txt2htmlv1,txt2htmldir,txt2html_inonefile,txt2html_odir)
from webdata.util.pyorg import (Topyorg,Topyhtml)

from webdata.puse.technic.strage import (EMWA_STD,KDJv2_code,Tutlev2_code,
                                 Tutlev1_df,MACDv2_code,MACDv1_df,
                                 ChaikinADv2_code,ChaikinADv1_df,
                                 KDJv1_df,RSIdf,RSIcode)


from webdata.puse.technic.technical import (sharpe_ratio,sharpe_ratiov1)

from webdata.puse.sinapy.financialdata import (Financial_Summary,BalanceSheet,
                                        IncomeStatement,CashFlowStatement,
                                        Finance_Index)

#from webdata.sd.eastmoney import driver_share_cashflow
#from webdata.sd.Nasdaq import get_nasd_data
#from webdata.sd.aastock import HK_tick_AAST

#from webdata.puse.qqpy.qqsource import (tick_data_today,get_dadan,
#                                   hist_tick_pershare,hist_tick,finance_share_news,vmprice, qqhyxw,
#                                    get_text, qqfinance_index,qqfinance_summary, qqfinance_BS,qqfinance_CF,qqfinance_InSt)

#from webdata.sd.qqsource import (get_reportlistsd_qq,
#                                 get_reseachtext_qq)

#from webdata.puse.qqpy.financehk import HK_Finance_qq
#from webdata.puse.qqpy.holdsharehk import (HK_inst_qq,HK_dividen_qq,HK_Invest_Rating_qq)
#from webdata.puse.qqpy.newshk import (HK_news_qq, HK_notice_qq)
#from webdata.puse.qqpy.qqus import (get_usgrouby_data, get_usall_data,
#                                        get_k_usdata,get_k_hkindex)
#from webdata.puse.qqpy.afinanca import (get_cwfx_qq,get_holders_num_qq,get_income_composition_qq,
#                                        get_preview_qq,get_forcast_qq,get_reportjson_qq,
#                                        get_bigtradeinfo_qq,get_TobefreeTrade_qq,
#                                        get_finance_index_qq,get_drogan_tiger_qq,
#                                        get_cashfl_industry_qq,get_reportlistjson_qq)
#from webdata.puse.qqpy.tradehk import HK_trademin_qq

from webdata.puse.aastockpy.basic import (HK_basic_info_AAS,
                                          HK_finance_info_AAS)
from webdata.puse.aastockpy.tick import HK_TradeLog_AAS
from webdata.puse.aastockpy.peer import (HK_peer_AAS, HK_peerall_AAS)
from webdata.puse.aastockpy.news import HK_news_AAS

from webdata.puse.money163.income import get_income_m163
from webdata.puse.money163.news import (news_m163, notice_m163,
                                            get_newstext_m163)
from webdata.puse.money163.bic import get_BCISCF_m163
from webdata.puse.money163.trading import (get_mk_data_m163,get_cashflhy_m163,
                                               get_trading_data_m163,
                                               get_cashfl_m163)
from webdata.puse.money163.findex import (get_mainindex_m163,
                                              get_finance_index_m163,
                                              get_finance_summary_m163)

from webdata.puse.eastmpy.basic import (HK_Basic_info_EM,HK_Preview_EM)
from webdata.puse.eastmpy.trade import (HK_trade_data_EM, HK_AH_data_EM,get_realtime_EM,HK_Value_Ass_EM)
from webdata.puse.eastmpy.finance import (HK_Balance_Sheet_EM, HK_Income_EM,HK_Cash_Flow_EM)
from webdata.puse.eastmpy.finance_analys import (HK_Summary_EM, HK_EPS_Index_EM,HK_dividend_EM,
                                                 HK_Profit_Quantity_EM,  HK_Captital_Repay_EM,
                                                 HK_Grow_Ability_EM)
from webdata.puse.eastmpy.hkcode_list import HK_List_EM
from webdata.puse.eastmpy.HSGT import (HK_HSGT_EM,HK_GGT_EM,HK_HSG_EM)
from webdata.puse.eastmpy.areportlist import ( get_reportlist_EM,
                                               get_holder_change_EM)
from webdata.puse.eastmpy.aafinance import(get_finance_index_EM,get_financeindex_f9_EM,
                                           get_bsincf_f10_EM,get_financeindex_f10_EM,
                                           get_forcast_EM)
from webdata.puse.eastmpy.aacashf import (get_cashf_alltoday_EM, get_cashf_sharehist_EM,
                                          get_cashf_conceptshares_EM,get_cashf_concepthist_EM,
                                          get_cashf_concepthist_min_EM,
                                          get_cashf_conceptcenter_EM, get_cashf_sharehist_min_EM,
                                          get_conceptSelectShares_EM, get_cashf_concept_EM)
from webdata.puse.eastmpy.aaholder import (get_seniorM_holder_EM,
                                           get_sharesholded_change_EM,
                                           get_holdernum_change_EM,
                                           get_share_holdernum_change_EM,
                                           get_holder_analys_EM,
                                           get_search_inst_num_EM,
                                           get_holder_shareperiod_EM,
                                           get_holder_sharedetail_EM,
                                           get_drogan_tiger_EM)
from webdata.puse.eastmpy.aabasic import (get_coreconcept_f10_EM,get_forcast_f10_EM,
                                          get_IndustryAnalysis_f10_EM,get_sharesGroupby_f10_EM,
                                          get_bussiAnalys_f10_EM,
                                          get_newstext_EM,get_tick_today_EM,get_hynewslist_EM,
                                          get_concept_share_epsforcast_EM)
from webdata.puse.eastmpy.futureOption import(get_Future_comparetoGlobal,get_Future_info_EM)
from webdata.puse.eastmpy.Industryindex import (get_BDI_EM,get_BCI_EM,get_TDI_EM,get_BBPI_EM,
                                                get_MetalC_EM,get_TieKuangshi_EM,
                                                get_BPI_EM,get_CONC_EM,get_SPI_EM,get_ZHQPI_EM,
                                                get_ZGMHPI_EM,get_STI_EM)
#from webdata.puse.eastmpy.classifyed import(get_code_classified_EM,get_bkindex_EM)

from webdata.puse.eastmpy.classifyindex import (get_allclassified_EM,get_classified_index_EM,get_shares_GroupbyClassify_EM)


#from webdata.puse.thspy.trade import (get_realtime_ths,get_k_data_year_THS,get_kdata_THS)
"""
from webdata.puse.thspy.finance import (get_financeindex_shares_THS,
                                        get_financeindex_all_THS,
                                        get_position_industry_THS,
                                        get_forecast_data_THS,
                                        get_income_THS,
                                        get_pepb_all_THS)
"""
from webdata.puse.xueqiu.finance import (finance_xueqiu,div_xueqiu)
from webdata.puse.xueqiu.trading import (get_kdata_xueqiu,get_dadan_xueqiu)
from webdata.puse.xueqiu.talk import (get_searchjson_xueqiu,hotline_xueqiu)

