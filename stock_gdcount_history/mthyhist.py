import akshare as ak
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.types import NVARCHAR, Float, Integer

#建立连接
conn=create_engine('mysql+pymysql://root:123@localhost:3306/db1',encoding='utf8')

# 获取煤炭行业成分股
stock_board_industry_hist_em_df = ak.stock_board_industry_hist_em(symbol="煤炭行业", adjust="hfq")
print(stock_board_industry_hist_em_df.head(3))
print(stock_board_industry_hist_em_df.tail(3))
print('\n')

try:
    #df数据写入数据库
    stock_board_industry_hist_em_df.to_sql('mthy_hist',con=conn,if_exists='append',index=False)
except Exception as e:
    print('error')
conn.dispose()



