# _*_coding:utf-8_*_


"""
分析任务
"""
import re


class AnalysisTasks(object):

    USER_NAME = 'user_name'
    USER_PASS = 'user_pass'
    START_DATE = 'start_date'
    TASK_TARGET = 'task_target'
    ACTION_TIME = 'action_time'
    FROM_STATION = 'from_station'
    TO_STATION = 'to_station'
    PASS_STATION = 'pass_station'
    CARE_PASS = 'care_pass'
    SEAT_TYPE = 'seat_type'
    FORCE_ACTION = 'force_action'
    CHOOSE_SEAT = 'choose_seat'
    TICKET_TYPE = 'ticket_type'
    ROBBER_INFO = 'robber_info'
    PHONE_NUMBER = 'phone_number'

    def __init__(self):
        self.task_info = {}

    '''
    分析
    '''
    def analysis(self):
        task = open('config/task_info.txt', 'r')
        for line in task:
            if line.startswith('#')\
                    or line == '\n'\
                    or len(line) == 0:  # 去掉注释、换行、空字符
                continue

            p = re.compile('(\w+):(.*)')
            m = p.match(line)
            self.task_info[m.group(1)] = m.group(2)

        return self.task_info


if __name__ == '__main__':
    tasks = AnalysisTasks()
    tasks.analysis()
    print(tasks.task_info)
    print('a' if tasks.task_info[AnalysisTasks.TICKET_TYPE] == 2 else 'b')

