#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import time
import json

def get_two_float(f_str, n):
    f_str = str(f_str)
    a, b, c = f_str.partition('.')
    c = (c+"0"*n)[:n]
    return ".".join([a, c])

def StatisticsJson(jsondate):

    cb_total = 0

    cb_Less90_count = 0
    cb_Less90_list = []
    cb_Less90_max_ytm = 0           #收益率
    cb_Less90_max_ytm_name = 0
    cb_Less90_min_premium = 0       #溢价率率
    cb_Less90_min_premium_name = 0

    cb_Less95_count = 0
    cb_Less95_list = []
    cb_Less95_max_ytm = 0
    cb_Less95_max_ytm_name = 0
    cb_Less95_min_premium = 0
    cb_Less95_min_premium_name = 0

    cb_Less100_count = 0
    cb_Less100_list = []
    cb_Less100_max_ytm = 0
    cb_Less100_max_ytm_name = 0
    cb_Less100_min_premium = 0
    cb_Less100_min_premium_name = 0

    cb_Larger125_count = 0
    cb_Larger125_list = []
    cb_Larger125_max_ytm = 0
    cb_Larger125_max_ytm_name = 0
    cb_Larger125_min_premium = 0
    cb_Larger125_min_premium_name = 0
    
    cb_3A_count = 0
    cb_3A_list = []
    cb_3A_max_ytm = 0
    cb_3A_max_ytm_cb = 0
    cb_3A_min_premium = 0
    cb_3A_min_premium_cb = 0
    
    cb_3A_max_ytm = cb_Less90_max_ytm = cb_Less95_max_ytm = cb_Less100_max_ytm = cb_Larger125_max_ytm = -100 #初始化最高收益率
    cb_3A_min_premium = cb_Less90_min_premium = cb_Less95_min_premium = cb_Less100_min_premium = cb_Larger125_min_premium= 100 #初始化最小溢价率        
    
    total = jsondate['total']
    total_list = jsondate['rows']
    items = iter(total_list)
    for item in items:
        name = item['cell']['bond_nm']
        if name[2] == '转':
            cb_total = cb_total + 1           
            if item['cell']['ytm_rt'] != '-':
                ytm = float(item['cell']['ytm_rt'].split('%')[0])
            else:
            	ytm = float(0)
            premium = float(item['cell']['premium_rt'].split('%')[0])
            price = float(item['cell']['price'])
            rating = item['cell']['rating_cd']            
            if rating == 'AAA':
                cb_3A_list.append(item)
                cb_3A_count = cb_3A_count + 1
                if cb_3A_max_ytm < ytm:
                    cb_3A_max_ytm = ytm
                    cb_3A_max_ytm_cb = item
                if cb_3A_min_premium > premium:
                    cb_3A_min_premium = premium
                    cb_3A_min_premium_cb = item
            if price <= 90:
                cb_Less90_count = cb_Less90_count + 1
                cb_Less90_list.append(item)
                if cb_Less90_max_ytm < ytm:
                    cb_Less90_max_ytm = ytm
                    cb_Less90_max_ytm_name = name
                if cb_Less90_min_premium > premium:
                    cb_Less90_min_premium = premium
                    cb_Less90_min_premium_name = name
            if 90 < price <= 95:
                cb_Less95_count = cb_Less95_count + 1
                cb_Less95_list.append(item)
                if cb_Less95_max_ytm < ytm:
                    cb_Less95_max_ytm = ytm
                    cb_Less95_max_ytm_name = name
                if cb_Less95_min_premium > premium:
                    cb_Less95_min_premium = premium
                    cb_Less95_min_premium_name = name
            if 95 < price <= 100:
                cb_Less100_count = cb_Less100_count + 1
                cb_Less100_list.append(item)
                if cb_Less100_max_ytm < ytm:
                    cb_Less100_max_ytm = ytm
                    cb_Less100_max_ytm_name = name
                if cb_Less100_min_premium > premium:
                    cb_Less100_min_premium = premium
                    cb_Less100_min_premium_name = name
            if 125 <= price :
                cb_Larger125_count = cb_Larger125_count + 1
                cb_Larger125_list.append(item)
                if cb_Larger125_max_ytm < ytm:
                    cb_Larger125_max_ytm = ytm
                    cb_Larger125_max_ytm_name = name
                if cb_Larger125_min_premium > premium:
                    cb_Larger125_min_premium = premium
                    cb_Larger125_min_premium_name = name

    print('{} 可转债价格统计： {}'.format('-'*20,'-'*20))
    print('可转债个数：', cb_total)
    print('跌破90元,占比：{}%（历史最低：占11%）'.format(get_two_float(cb_Less90_count*100/cb_total, 2))) 
    print('跌破95元,占比：{}%（历史最低：占18%）'.format(get_two_float((cb_Less90_count+cb_Less95_count)*100/cb_total, 2)))
    print('跌破100元,占比：{}%（历史最低：占48%）'.format(get_two_float((cb_Less90_count+cb_Less95_count+cb_Less100_count)*100/cb_total, 2)))
    print('超过125元,占比：{}%'.format(get_two_float(cb_Larger125_count*100/cb_total, 2)))
    print('{} AAA可转债统计： {}'.format('-'*20,'-'*20))    
    print('收益率最高的3A可转债: {}，价格：{}，ytm:{}，溢价率：{}，'.format(cb_3A_max_ytm_cb['cell']['bond_nm'], 
        cb_3A_max_ytm_cb['cell']['price'], cb_3A_max_ytm_cb['cell']['ytm_rt'], cb_3A_max_ytm_cb['cell']['premium_rt']))
    print('溢价率最小的3A可转债: {}，价格：{}，ytm:{}，溢价率：{}，'.format(cb_3A_min_premium_cb['cell']['bond_nm'],
        cb_3A_min_premium_cb['cell']['price'], cb_3A_min_premium_cb['cell']['ytm_rt'], cb_3A_min_premium_cb['cell']['premium_rt'])) 

    return True

if __name__ == "__main__":
    target = 'https://www.jisilu.cn/data/cbnew/cb_list/'
    LST_time = int(time.time())
    params = {'___jsl': 'LST___t='+str(LST_time)}
    payload = {'fprice':'',
               'tprice':'',
               'volume':'',
               'svolume':'',
               'premium_rt':'',
               'ytm_rt':'',
               'rating_cd':'',
               'is_search':'N',
               'btype':'',
               'listed':'Y',
               'industry':'',
               'bond_ids':'',
               'rp':50,
               'page':1}
    req = requests.post(url=target,params=params,data=payload,verify=False)
    StatisticsJson(req.json())
