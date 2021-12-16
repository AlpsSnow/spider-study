import akshare as ak
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Float, Integer

#建立连接
conn=create_engine('mysql+pymysql://root:123@localhost:3306/db1',encoding='utf8')
'''
# 获取煤炭行业成分股
stock_board_industry_cons_em_df = ak.stock_board_industry_cons_em(symbol="煤炭行业")
print(stock_board_industry_cons_em_df.head(3))
print(stock_board_industry_cons_em_df.tail(3))
print('\n')

try:
    #df数据写入数据库的000001表
    stock_board_industry_cons_em_df.to_sql('mthy_list',con=conn,if_exists='append',index=False)
except Exception as e:
    print('error')
'''

dtypedict = {
  '持股变动信息-变动数量': Float
}

# 获取所有高管增减持数据
stock_em_ggcg_df = ak.stock_em_ggcg()
print(stock_em_ggcg_df.head(3))
print(stock_em_ggcg_df.tail(3))

try:
    #df数据写入数据库的000001表
    stock_em_ggcg_df.to_sql('all_ggcg',con=conn,if_exists='append',index=False, dtype=dtypedict)
except Exception as e:
    print('error')

conn.dispose()



