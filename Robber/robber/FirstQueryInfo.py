# -*- coding: utf-8 -*-
import requests


'''
模拟查询车票信息
'''
def queryInfo():
    # 'https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date=2018-03-17&leftTicketDTO.from_station=IOQ&leftTicketDTO.to_station=CBQ&purpose_codes=ADULT'
    response = requests.get('https://kyfw.12306.cn/otn/leftTicket/queryO?'
                            'leftTicketDTO.train_date=2018-05-01&leftTicketDTO.from_station=IOQ&'
                            'leftTicketDTO.to_station=CBQ&purpose_codes=ADULT')
    response.encoding = 'utf-8'
    print(response.text)
    result = response.json()

    print(result)

    return result['data']['result']


'''
车次 3
车次代号 2
无座 26
软卧 23
硬座 29
硬卧 28
特等商务座 32
一等座 31
二等座 30
'''
for info in queryInfo():
    #print(info)
    tmp_list = info.split('|')
    #print(tmp_list)
    # print(tmp_list[26])  # 拿到无座的信息
    #print(tmp_list[0])
    #print(tmp_list[2])
    print('-----------------------')
    print(tmp_list[3] + "\t二等座\t" + tmp_list[30])
    print(tmp_list[3] + "\t一等座\t" + tmp_list[31])
    print(tmp_list[3] + "\t无  座\t" + tmp_list[26])
    print(tmp_list[26] != None and len(tmp_list[26]) == 0)
    print(tmp_list[26] == '*')
    print('-----------------------')
    #print(tmp_list[8])
    #print(tmp_list[8][0:2])




