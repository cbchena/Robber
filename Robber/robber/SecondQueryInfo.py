# -*- coding: utf-8 -*-
from pip._vendor import requests

'''
模拟查询车次停靠信息
'''
def queryInfo():
    response = requests.get('https://kyfw.12306.cn/otn/czxx/queryByTrainNo?'
                            'train_no=6i000D312606&from_station_telecode=IOQ&to_station_telecode=CBQ&depart_date=2018-03-15')

    result = response.json()

    print(result)

    return result['data']['data']


for info in queryInfo():
    print(info)

