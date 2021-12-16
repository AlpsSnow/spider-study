import pymysql
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

db=pymysql.connect(host='localhost',user='root',password='123',port=3306,db='db1',charset='utf8')


# 取得煤炭行业历史行情数据
cursor=db.cursor()
sql="select * from mthy_hist"
cursor.execute(sql)
mthy_hist=cursor.fetchall()
cols=cursor.description
col=[] #创建一个空列表以存放列名
for v in cols:
    col.append(v[0]) #循环提取列名，并添加到col空列表
mthy_hist_df=pd.DataFrame(mthy_hist,columns=col) #将查询结果转换成DF结构，并给列重新赋值

# 取得煤炭行业股票一览
cursor=db.cursor()
sql="select * from mthy_list"
cursor.execute(sql)
mthy_list=cursor.fetchall()
cols=cursor.description
col=[] #创建一个空列表以存放列名
for v in cols:
    col.append(v[0]) #循环提取列名，并添加到col空列表
mthy_list_df=pd.DataFrame(mthy_list,columns=col) #将查询结果转换成DF结构，并给列重新赋值

# 将'日期'的数据类型YYYY-MM-DD 为 YYYY-MM
mthy_hist_df['日期']=mthy_hist_df['日期'].apply(lambda x:x[0:7])

# 去掉重复日期的数据，只保留重复数据的最后一条记录
mthy_hist_df.drop_duplicates(subset=['日期'],keep='last',inplace=True)

# 取得全行业高管增减持历史数据
cursor=db.cursor()
sql="select * from all_ggcg"
cursor.execute(sql)
all_ggcg=cursor.fetchall()
cols=cursor.description
col=[] #创建一个空列表以存放列名
for v in cols:
    col.append(v[0]) #循环提取列名，并添加到col空列表
all_ggcg_df=pd.DataFrame(all_ggcg,columns=col) #将查询结果转换成DF结构，并给列重新赋值
db.close()

# 根据煤炭行业股票一览，从全行业高管增持历史数据筛选出煤炭行业高管增减持数据
mthy_ggcg_df=all_ggcg_df[all_ggcg_df['代码'].isin(mthy_list_df['代码'])]

# 煤炭行业高管增减持数据筛选出感兴趣的数据
result_df=mthy_ggcg_df[['代码','名称','持股变动信息-增减','持股变动信息-变动数量','变动截止日']]

# 根据增减持类型，调整数据正负值
def to_cal(x,y):
    if x=='减持':
        y=y*(-1)
    return y
result_df['持股变动信息-变动数量']=result_df.apply(lambda row:to_cal(row["持股变动信息-增减"],row["持股变动信息-变动数量"]),axis = 1)

'''
def to_cal(df):
    if df['持股变动信息-增减']=='减持':
        return df['持股变动信息-变动数量']*(-1)
    else:
        return df['持股变动信息-变动数量']
result_df['持股变动信息-变动数量']=result_df.apply(to_cal,axis = 1)'''

# 变更'变动截止日'列的数据类型YYYY-MM-DD 为 YYYY-MM
result_df['变动截止日']=result_df['变动截止日'].apply(lambda x:x[0:7])

# 将同一个月的数据进行分组求和
result_df=result_df.groupby('变动截止日',as_index=False).sum()

'''
# 统计每个季度的和
result_df['变动截止日']=pd.to_datetime(result_df['变动截止日'],format="%Y-%M-%d")
result_df.set_index('变动截止日',inplace=True)
result_df=result_df.resample('M').sum().reset_index()
result_df['变动截止日']=result_df['变动截止日'].apply(lambda x: x.strftime('%F'))
'''


# 筛选出发生高管增减持月份的历史行情数据
mthy_hist_df=mthy_hist_df[mthy_hist_df['日期'].isin(result_df['变动截止日'])]
#mthy_hist_df=mthy_hist_df[mthy_hist_df['日期']>='2013-01']
print(mthy_hist_df.head(3))
print(mthy_hist_df.tail(3))

color = [] 
for element in result_df['持股变动信息-变动数量']:
    if element>=0:
        color=np.append(color, 'r')
    else:
        color=np.append(color, 'g')

fig=plt.figure(figsize=(14,7)) #设置画布的宽，高
#显示中文标签
plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False
plt.xticks(rotation=270) #垂直显示x轴

plt.title("煤炭行业历史行情") #设置标题
plt.ylabel('收盘点位 or 增减持数量(百万)')
plt.xlabel("日期")
plt.xticks(rotation=270)
plt.ylim((-40000, 20000)) # 设置y轴范围
plt.plot(mthy_hist_df['日期'],mthy_hist_df['收盘'],color = 'b')
plt.bar(result_df['变动截止日'],result_df['持股变动信息-变动数量'],color=color)

plt.show()

'''
# 同一画布，上下两个图

fig=plt.figure(figsize=(14,7)) #设置画布的宽，高
#显示中文标签
plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False
plt.xticks(rotation=270) #垂直显示x轴
plt.subplot(2, 1, 1)
plt.title("煤炭行业历史行情") #设置标题
plt.ylabel('收盘点位')
plt.xlabel("日期")
plt.xticks(rotation=270)

print(mthy_hist_df)
plt.plot(result_df['变动截止日'],mthy_hist_df['收盘'],color = 'b')

plt.subplot(2, 1, 2)
plt.bar(result_df['变动截止日'],result_df['持股变动信息-变动数量'],color=color)
plt.ylabel('增减持数量(百万)')
plt.xticks(rotation=270)
plt.show()
'''

'''
# 左右双Y轴，共用x轴

fig, ax1 = plt.subplots()
fig.set_figheight(8)
fig.set_figwidth(16)
#显示中文标签
plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False
plt.xticks(rotation=270) #垂直显示x轴
ax1.plot(result_df['变动截止日'],mthy_hist_df['收盘'], color="red", label="收盘点位")
ax1.set_ylabel("收盘点位")

ax2 = ax1.twinx()
ax2.bar(result_df['变动截止日'],result_df['持股变动信息-变动数量'],color=color)
ax2.set_xlabel("月份")
ax2.set_ylabel("增减持数量(百万)")
fig.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
plt.show()
'''
