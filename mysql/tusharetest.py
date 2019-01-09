# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
import tushare as ts
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

df = ts.get_tick_data('600848', date='2014-12-22')
df['code']='600848'
engine = create_engine('mysql://root:801019@127.0.0.1/test?charset=utf8&use_unicode=0')

#存入数据库
df.to_sql('600848_data',engine)

#追加数据到现有表
#df.to_sql('tick_data',engine,if_exists='append')
