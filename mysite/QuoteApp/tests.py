from django.test import TestCase

# Create your tests here.
from urllib.request import urlopen
import pandas as pd
from datetime import datetime, timezone, timedelta
import requests
import sched
import time
import json


def stock_crawler(targets):
    #clear_output(wait=True)
    
    # 組成stock_list
    stock_list = '|'.join('tse_{}.tw'.format(target) for target in targets) 
    
    #　query data
    query_url = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch="+ stock_list
    data = json.loads(urlopen(query_url).read())
    if data['msgArray']==[]:
        return '請輸入上市類股票代號'

    # 過濾出有用到的欄位
    columns = ['c','n','z','tv','v','o','h','l','y']
    df = pd.DataFrame(data['msgArray'], columns=columns)
    df.columns = ['股票代號','公司簡稱','當盤成交價','當盤成交量','累積成交量','開盤價','最高價','最低價','昨收價']
    df.insert(9, "漲跌", 0.0)
    df.insert(10, "漲跌百分比", 0.0) 
    

    # 新增漲跌百分比
    for x in range(len(df.index)):
        if df['當盤成交價'].iloc[x] != '-':
            df.iloc[x, [2,3,4,5,6,7,8]] = df.iloc[x, [2,3,4,5,6,7,8]].astype(float)
            df['漲跌'].iloc[x] = round(df['當盤成交價'].iloc[x] - df['昨收價'].iloc[x],2)
            df['漲跌百分比'].iloc[x] = str(round((df['當盤成交價'].iloc[x] - df['昨收價'].iloc[x])/df['昨收價'].iloc[x] * 100 ,2))+"%"
    
    # 紀錄更新時間
    tz = timezone(timedelta(hours=+8))# 設定為 +8 時區
    time = datetime.now(tz).isoformat(timespec="seconds")# 取得現在時間、指定時區、轉為 ISO 格式
    #text= "更新時間:" + str(time.hour)+":"+str(time.minute) +'\n'+ '|'.join(df.columns)+'\n'+'|'.join(df.loc[0].astype(str))
    text= "更新時間:" + str(time) +'\n'+ '\n'.join([df.columns[i]+':'+df.loc[0].astype(str)[i] for i in range(len(df.columns))])
    return text

print(stock_crawler(['1521']))
