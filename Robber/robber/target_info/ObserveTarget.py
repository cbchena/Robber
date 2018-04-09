# -*- coding: utf-8 -*-
import os
import requests
import time
from robber.StationInfo import StationInfo

# 观察目标对象，记录目标数据
from robber.target_info.ReportTarget import ReportTarget


class ObserveTarget(object):

    def __init__(self):
        self.from_station = '深圳北'
        self.to_station = '潮汕'
        self.observeTime = 10 * 60  # 观察时间

        # 分析站点信息
        stationInfo = StationInfo()
        stationInfo.analysis()
        self.station = stationInfo.station

        self.date = '2018-04-26'

    def observe(self):
        # time.strftime('%Y-%m-%d', time.localtime())
        response = requests.get('https://kyfw.12306.cn/otn/leftTicket/queryO?'
                                'leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&'
                                'leftTicketDTO.to_station={}&purpose_codes=ADULT'
                                .format(self.date,
                                        self.station[self.from_station],
                                        self.station[self.to_station],
                                        ))
        response.encoding = 'utf-8'
        result = response.json()

        print(result)

        return result['data']['result']


if __name__ == '__main__':

    observeTarget = ObserveTarget()

    # 生成统计文件
    path = 'data_' + observeTarget.date
    if not os.path.exists(path):
        os.mkdir(path)

    startTime = time.time()
    while True:
        endTime = time.time()
        minus = endTime - startTime
        if minus > observeTarget.observeTime:  # 观察时间

            # 结束，生成报表
            reportTarget = ReportTarget()
            reportTarget.report(path, observeTarget.date)
            break
        else:
            lstInfo = observeTarget.observe()
            for info in lstInfo:
                tmp_list = info.split('|')
                # print('-----------------------')
                # print(tmp_list)
                # print(tmp_list[3] + "\t二等座\t" + tmp_list[30])
                # print(tmp_list[3] + "\t一等座\t" + tmp_list[31])
                # print(tmp_list[3] + "\t无  座\t" + tmp_list[26])
                # print('-----------------------')
                if (tmp_list[31] == '*' or len(tmp_list[30]) == 0)\
                                and (tmp_list[30] != '*' and len(tmp_list[30]) == 0) \
                                and (tmp_list[26] != '*' and len(tmp_list[26]) == 0):
                    continue

                targetInfo = open(path + '/' + tmp_list[3] + '.txt', 'a')
                lstCare = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), observeTarget.from_station,
                           observeTarget.to_station,
                           tmp_list[13], tmp_list[8], tmp_list[9],
                           tmp_list[10], tmp_list[31], tmp_list[30], tmp_list[26]]

                targetInfo.write('|'.join(lstCare) + '\n')
                targetInfo.close()

            time.sleep(5)
