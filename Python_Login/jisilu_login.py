#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import time

if __name__ == "__main__":
    target = 'https://www.jisilu.cn/account/login/'
    cookies={}
    cookies['Hm_lpvt_164fe01b1433a19b507595a43bf58262']=str(int(time.time()))
    cookies['Hm_lvt_164fe01b1433a19b507595a43bf58262']='1626921687,1627000170,1627017807,1627260573'
    cookies['kbz_newcookie']='1'
    cookies['kbzw__Session']='3f9tjgiprevqdrf1n5fd18k2n5'
    cookies['kbzw__user_login']='7Obd08_P1ebax9aXuEr4Al0pFF4UBUgCIpakptzY1enY5unX1r6bl6mt2c3dobCap8Sup9mtk9KT1a6lmtucqMatlqiro6-Cq47p4tnH1peola6VqaiUs47FotLWoLbo5uDO4sKmrKGogZi43efZ2PDfl7DKgainoaickLjd56udtIzvmKqcl-npspqgj6SilbDez-LRpZOnqKOokqCSlL_e297S5tqlmqelow..'
    username='A股没法玩'
    name=username.encode("utf-8").decode('latin1')
    cookies['kbzw_r_uname']=name
    requests.packages.urllib3.disable_warnings()
    req = requests.get(url=target,cookies=cookies,verify=False)
    print("req.reason="+req.reason)
    print("req.status_code="+str(req.status_code))
    #print(req.content)