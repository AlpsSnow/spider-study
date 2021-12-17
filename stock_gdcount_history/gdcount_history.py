import sys
import time
import akshare as ak
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits import axisartist
import matplotlib.dates as mdates
from datetime import datetime


if __name__ == "__main__":
    if len(sys.argv) < 2 :
        print("没有指定id")
        sys.exit()

    # get gd count
    stock_zh_a_gdhs_detail_em_df = ak.stock_zh_a_gdhs_detail_em(symbol=sys.argv[1])
    #stock_zh_a_gdhs_detail_em_df['股东户数统计截止日'] = stock_zh_a_gdhs_detail_em_df['股东户数统计截止日'].apply(lambda x:x.strftime('%Y-%m-%d'))
    stock_zh_a_gdhs_detail_em_df['股东户数-本次']=stock_zh_a_gdhs_detail_em_df['股东户数-本次'].apply(lambda x:(x/10000))
    stock_zh_a_gdhs_detail_em_df['户均持股数量']=stock_zh_a_gdhs_detail_em_df['户均持股数量'].apply(lambda x:(x/10000))
    stock_zh_a_gdhs_detail_em_df = stock_zh_a_gdhs_detail_em_df.reindex(index=stock_zh_a_gdhs_detail_em_df.index[::-1])
    print(stock_zh_a_gdhs_detail_em_df)

    # get history
    start_date = stock_zh_a_gdhs_detail_em_df['股东户数统计截止日'].iloc[0]
    start_date = start_date.strftime('%Y%m%d')
    print(start_date)

    end_date = time.strftime("%Y%m%d", time.localtime())

    print(end_date)

    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=sys.argv[1], period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
    print(stock_zh_a_hist_df)

    '''
    # get date for BQ(季度最后一个工作日)    
    start_date = "{}/{}/{}".format(start_date[6:],start_date[4:6],start_date[:4])
    end_date = time.strftime("%d/%m/%Y", time.localtime())
    cal=pd.date_range(start_date,end_date,freq='BQ')
    cal_df=cal.to_frame(index=False,name='Date')
    cal_df['Date']=cal_df['Date'].apply(lambda x: datetime.fromtimestamp(x).date())
    print(cal_df['Date'])
    '''

    # 季度最后工作日的history
    stock_zh_a_hist_df['日期'] = stock_zh_a_hist_df['日期'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
    #stock_zh_a_hist_df = stock_zh_a_hist_df[stock_zh_a_hist_df['日期'].isin(cal_df['Date'])]
    print(stock_zh_a_hist_df)

    
    # paint
    fig = plt.figure(figsize=(14,7))
    plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
    plt.rcParams['axes.unicode_minus']=False

    host = host_subplot(111,axes_class=axisartist.Axes,figure=fig)

    par1 = host.twinx()
    par2 = host.twinx()
    par3 = host.twinx()

    par2.axis['right'] = par2.new_fixed_axis(loc="right", offset=(60,0))

    par1.axis["right"].toggle(all=True)
    par2.axis["right"].toggle(all=True)


    p1, = host.plot(stock_zh_a_hist_df['日期'],stock_zh_a_hist_df['收盘'],label="历史行情")
    p2, = par1.plot(stock_zh_a_gdhs_detail_em_df['股东户数统计截止日'],stock_zh_a_gdhs_detail_em_df['股东户数-本次'],label="股东户数(万)")
    p3, = par2.plot(stock_zh_a_gdhs_detail_em_df['股东户数统计截止日'],stock_zh_a_gdhs_detail_em_df['户均持股数量'],label="户均持股数量(万)")

    '''
    host.set_xlim(0, 2)
    host.set_ylim(0, 2)
    par1.set_ylim(0, 4)
    par2.set_ylim(1, 65)
    '''
    host.set_xlabel("日期")
    host.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    host.axis['bottom'].major_ticklabels.set_rotation(-45)

    host.set_title(sys.argv[1]+"行情和股东信息")
    host.set_ylabel("收盘")
    par1.set_ylabel("股东户数(万)")
    par2.set_ylabel("户均持股数量(万)")

    host.legend()
    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["right"].label.set_color(p2.get_color())
    par2.axis["right"].label.set_color(p3.get_color())
    plt.show()
