# _*_coding:utf-8_*_
import json
import re
import urllib
from json import loads

import requests
from PIL import Image
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import random
import time

# 禁用安全请求警告
from robber.AnalysisTasks import AnalysisTasks
from robber.StationInfo import StationInfo

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_random():
    return str(random.random())  # 生产一个18位的随机数


def get_13_time():  # 一个十三位的时间戳
    return str(int(time.time() * 1000))


# R计划
class Robber(object):

    def __init__(self):
        self.headers = {
            'Host': 'kyfw.12306.cn',
            'Connection': 'keep-alive',
            'Origin': 'https://kyfw.12306.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36',
            'Accept': '*/*',
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        }

        # 分析任务信息
        tasks = AnalysisTasks()
        self.task_info = tasks.analysis()

        # 分析站点信息
        stationInfo = StationInfo()
        stationInfo.analysis()
        self.station = stationInfo.station

        # 创建一个网络请求session实现登录验证
        self.session = requests.session()
        self.session.verify = False  # 忽略https 证书验证

    def get_init(self):  # 请求了一个首页
        self.headers["Referer"] = "https://kyfw.12306.cn/otn/login/init"
        url = 'https://kyfw.12306.cn/otn/login/init'
        r = self.session.get(url=url, headers=self.headers)

        print('首页获取成功，状态码：', r)

    def get_newpasscode(self):  # 这个页面不知道是干啥的，但是12306 请求了，咱们为了模仿的像一点也去请求
        url = 'https://kyfw.12306.cn/otn/resources/js/newpasscode/captcha_js.js?_={}'.format(get_13_time())
        r = self.session.get(url)
        print('newpasscode获取成功，状态码：', r)

    # 获取验证码图片
    def getImg(self):
        url = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand"
        response = self.session.get(url=url, headers=self.headers, verify=False)
        # 把验证码图片保存到本地
        with open('img.jpg', 'wb') as f:
            f.write(response.content)
        # 用pillow模块打开并解析验证码,这里是假的，自动解析以后学会了再实现
        try:
            im = Image.open('img.jpg')
            # 展示验证码图片，会调用系统自带的图片浏览器打开图片，线程阻塞
            im.show()
            # 关闭，只是代码关闭，实际上图片浏览器没有关闭，但是终端已经可以进行交互了(结束阻塞)
            im.close()
        except:
            print(u'请输入验证码')
        # =======================================================================
        # 根据打开的图片识别验证码后手动输入，输入正确验证码对应的位置，例如：2,5
        # ---------------------------------------
        #         |         |         |
        #    0    |    1    |    2    |     3
        #         |         |         |
        # ---------------------------------------
        #         |         |         |
        #    4    |    5    |    6    |     7
        #         |         |         |
        # ---------------------------------------
        # =======================================================================
        captcha_solution = input('请输入验证码位置，以","分割[例如2,5]:')
        return captcha_solution

    # 验证结果
    def checkYanZheng(self, solution):
        # 分割用户输入的验证码位置
        soList = solution.split(',')
        # 由于12306官方验证码是验证正确验证码的坐标范围,我们取每个验证码中点的坐标(大约值)
        yanSol = ['35,35', '105,35', '175,35', '245,35', '35,105', '105,105', '175,105', '245,105']
        yanList = []
        for item in soList:
            print(item)
            yanList.append(yanSol[int(item)])
        # 正确验证码的坐标拼接成字符串，作为网络请求时的参数
        yanStr = ','.join(yanList)
        checkUrl = "https://kyfw.12306.cn/passport/captcha/captcha-check"
        data = {
            'login_site': 'E',  # 固定的
            'rand': 'sjrand',  # 固定的
            'answer': yanStr  # 验证码对应的坐标，两个为一组，跟选择顺序有关,有几个正确的，输入几个
        }
        # 发送验证
        cont = self.session.post(url=checkUrl, data=data, headers=self.headers, verify=False)
        # 返回json格式的字符串，用json模块解析
        dic = loads(cont.content)
        code = dic['result_code']
        # 取出验证结果，4：成功  5：验证失败  7：过期
        if str(code) == '4':
            return True
        else:
            return False

    def login(self):
        url = 'https://kyfw.12306.cn/passport/web/login'
        data = {
            'username': self.task_info[AnalysisTasks.USER_NAME],
            'password': self.task_info[AnalysisTasks.USER_PASS],
            'appid': 'otn'
        }
        r = self.session.post(url=url, data=data, headers=self.headers)
        self.uamtk = r.json()["uamtk"]
        print(r.text)

    def userLogin(self):
        url = 'https://kyfw.12306.cn/otn/login/userLogin'
        r = self.session.post(url=url, headers=self.headers)
        # print(r.text)

    def passport(self):
        url = 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin'
        r = self.session.get(url=url)
        # print(r.text)

    def getjs(self):  # 不知道是干啥的，但是也提交吧
        url = 'https://kyfw.12306.cn/otn/HttpZF/GetJS'
        r = self.session.get(url)

    def post_uamtk(self):
        url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        data = {'appid': 'otn'}
        r = self.session.post(url=url, data=data, allow_redirects=False, headers=self.headers)
        self.newapptk = r.json()["newapptk"]
        r.encoding = 'utf-8'
        print(r.text)

    def post_uamauthclient(self):
        url = 'https://kyfw.12306.cn/otn/uamauthclient'
        data = {
            'tk': self.newapptk
        }
        r = self.session.post(url=url, data=data, headers=self.headers)
        self.apptk = r.json()["apptk"]
        r.encoding = 'utf-8'
        print(r.text)

    def get_userLogin(self):
        url = 'https://kyfw.12306.cn/otn/login/userLogin'
        r = self.session.get(url)
        r.encoding = 'utf-8'
        # print(r.text)

    def get_leftTicket(self):
        self.headers["Referer"] = "https://kyfw.12306.cn/otn/leftTicket/init"
        url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        r = self.session.get(url=url, headers=self.headers)
        r.encoding = 'utf-8'
        # print(r.text)

    def get_GetJS(self):
        url = 'https://kyfw.12306.cn/otn/HttpZF/GetJS'
        self.session.get(url)

    def get_qufzjql(self):
        url = 'https://kyfw.12306.cn/otn/dynamicJs/qufzjql'
        self.session.get(url)

    def get_otzizfc(self):
        url = 'https://kyfw.12306.cn/otn/dynamicJs/otzizfc'
        self.session.get(url)

    def get_checkUser(self):
        self.headers["Referer"] = "https://kyfw.12306.cn/otn/leftTicket/init"
        url = 'https://kyfw.12306.cn/otn/login/checkUser'
        data = {
            '_json_att': ''
        }
        r = self.session.post(url=url, data=data, headers=self.headers)
        print('get_checkUser=====' + r.text)
        result = r.json()
        return result['data']['flag']

    def queryZ(self):
        response = self.session.get('https://kyfw.12306.cn/otn/leftTicket/queryO?'
                                    'leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&'
                                    'leftTicketDTO.to_station={}&purpose_codes={}'
                                    .format(self.task_info[AnalysisTasks.START_DATE],
                                            self.station[self.task_info[AnalysisTasks.FROM_STATION]],
                                            self.station[self.task_info[AnalysisTasks.TO_STATION]],
                                            '0x00' if self.task_info[AnalysisTasks.TICKET_TYPE] == 2 else 'ADULT'))

        response.encoding = 'utf-8'
        result = response.json()

        return result['data']['result']

    # 点击预定下单，当车次完全没有车票的时候，该结果返回"提交失败，请重试..."
    def postSubmitOrderRequest(self):
        self.headers["Referer"] = "https://kyfw.12306.cn/otn/leftTicket/init"
        url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        data = {
            'secretStr': urllib.parse.unquote(self.secretStr),  # 预定提交的令牌
            'train_date': self.task_info[AnalysisTasks.START_DATE],  # 出发时间
            'back_train_date': time.strftime('%Y-%m-%d', time.localtime()),  # 返回时间，没有则为当前日期
            'tour_flag': 'dc',  # dc 单程   fc 返程
            'purpose_codes': '0x00' if self.task_info[AnalysisTasks.TICKET_TYPE] == 2 else 'ADULT',
            # ADULT 成人  0x00  学生
            'query_from_station_name': self.task_info[AnalysisTasks.FROM_STATION],
            'query_to_station_name': self.task_info[AnalysisTasks.TO_STATION],
            'undefined': ''
        }
        r = self.session.post(url=url, data=data, headers=self.headers)
        print('postSubmitOrderRequest=====' + r.text)

        result = r.json()
        tResult = (0, '')  # 成功
        if not result['status']:
            message = result['messages'][0]
            p = re.compile('^您还有未处理的订单，请您到.*')
            if p.search(message):
                tResult = (1, '陈Sir，您有未处理的订单')  # 有未完成订单
            else:
                tResult = (2, '')

        return tResult

    def postInitDc(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        r = self.session.post(url=url, headers=self.headers)
        self.REPEAT_SUBMIT_TOKEN = re.findall("globalRepeatSubmitToken = '(.*?)';", r.text)[0]
        ticketInfoForPassengerForm = re.search("ticketInfoForPassengerForm=(.*?);", r.text).group(1)
        ticketInfoForPassengerForm = ticketInfoForPassengerForm.replace("'", '"')
        self.ticketInfoForPassengerForm = json.loads(ticketInfoForPassengerForm)
        self.orderRequestDTO = self.ticketInfoForPassengerForm['orderRequestDTO']  # 车次信息

    # 获取乘客信息
    def postetPassengerDTOs(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        data = {
            'REPEAT_SUBMIT_TOKEN': self.REPEAT_SUBMIT_TOKEN,
            '_json_att': ''
        }
        r = self.session.post(url=url, data=data, headers=self.headers)
        r.encoding = 'utf-8'
        print('postetPassengerDTOs=====' + r.text)
        result = r.json()
        return result['status']

    # 检查订单信息
    def checkOrderInfo(self):
        self.headers["Referer"] = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        self.passengerTicketStr = ''
        self.oldPassengerStr = ''

        lstRobber = self.task_info[AnalysisTasks.ROBBER_INFO].split('|')
        lstPhone = self.task_info[AnalysisTasks.PHONE_NUMBER].split('|')
        for i in range(len(lstRobber)):
            if i < len(lstPhone):
                phone = lstPhone[i]
            else:
                phone = ''

            temp = self.task_info[AnalysisTasks.SEAT_TYPE] + ',0,' \
                   + self.task_info[AnalysisTasks.TICKET_TYPE] + ',' \
                   + lstRobber[i] + ',' \
                   + phone + ',N'

            if i + 1 < len(lstRobber):
                temp += '_'

            self.passengerTicketStr += temp
            self.oldPassengerStr += lstRobber[i] + ',1_'

        print('passengerTicketStr=====   ' + self.passengerTicketStr)
        print('oldPassengerStr=====   ' + self.oldPassengerStr)

        data = {
            'cancel_flag': 2,  # 固定值
            'bed_level_order_num': '000000000000000000000000000000',  # 固定值
            #  O(O是二等座，换一等座为M),0,1(1是成人票  2儿童  3学生  4残疾）,蔡耿妍,1,445221199007155946,15602950715,N
            #  座位编号,0,票类型,乘客名,证件类型,证件号,手机号码,保存常用联系人(Y或N)
            #  O,0,1,陈楚斌,1,440582198903026739,18680319375,N
            'passengerTicketStr': self.passengerTicketStr,  # 旅客信息字符串  第一个O是二等座，换一等座为M
            'oldPassengerStr': self.oldPassengerStr,  # 旅客信息字符串
            'tour_flag': self.ticketInfoForPassengerForm['tour_flag'],  # dc 单程   fc 返程
            'randCode': '',
            'whatsSelect': 1,
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.REPEAT_SUBMIT_TOKEN
        }
        r = self.session.post(url=url, data=data, headers=self.headers)
        print('checkOrderInfo=====' + r.text)
        result = r.json()
        return result['data']['submitStatus']

    # 获取车次的排队信息
    def getQueueCount(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        data = {
            'train_date': time.strftime("%a %b %d %Y %H:%M:%S GMT+0800 (CST)",
                                        time.localtime(self.orderRequestDTO['train_date']['time'] / 1000)),  # 列车日期
            'train_no': self.orderRequestDTO['train_no'],  # 列车号
            'stationTrainCode': self.orderRequestDTO['station_train_code'],  # 车次
            'seatType': self.task_info[AnalysisTasks.SEAT_TYPE],  # 座位类型
            'fromStationTelecode': self.orderRequestDTO['from_station_telecode'],  # 发站编号
            'toStationTelecode': self.orderRequestDTO['to_station_telecode'],  # 到站编号
            'leftTicket': self.ticketInfoForPassengerForm['queryLeftTicketRequestDTO']['ypInfoDetail'],
            'purpose_codes': self.ticketInfoForPassengerForm['purpose_codes'],  # 默认取ADULT,表成人,学生表示为：0X00
            'train_location': self.ticketInfoForPassengerForm['train_location'],
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.REPEAT_SUBMIT_TOKEN
        }
        r = self.session.post(url=url, data=data, headers=self.headers)
        r.encoding = 'utf-8'

        # countT表示的是排队人数，而ticket指的是当前列车对应座位的剩余票数（二等，无座）
        # data:{count: "5", ticket: "527,149", op_2: "false", countT: "0", op_1: "true"}
        print('getQueueCount=====' + r.text)
        result = r.json()
        ticket = result['data']['ticket']
        lstTicket = ticket.split(',')
        if len(lstTicket) == 2:
            return int(lstTicket[0]) > 0 or self.task_info[AnalysisTasks.FORCE_ACTION] == 'Y'  # 验证二等座或者验证是否支持无座
        elif len(lstTicket) == 1:
            return int(lstTicket[0]) > 0 or self.task_info[AnalysisTasks.FORCE_ACTION] == 'Y'

    # 下单
    def confirmSingleForQueue(self):
        self.headers["Referer"] = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
        self.headers["Accept"] = "application/json, text/javascript, */*; q=0.01"
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        data = {
            'passengerTicketStr': self.passengerTicketStr,  # 旅客信息字符串  第一个O是二等座，换一等座为M
            'oldPassengerStr': self.oldPassengerStr,  # 旅客信息字符串
            'randCode': '',
            'purpose_codes': self.ticketInfoForPassengerForm['purpose_codes'],  # 默认取ADULT,表成人,学生表示为：0X00
            'key_check_isChange': self.ticketInfoForPassengerForm['key_check_isChange'],
            'leftTicketStr': self.ticketInfoForPassengerForm['leftTicketStr'],
            'train_location': self.ticketInfoForPassengerForm['train_location'],
            'choose_seats': self.task_info[AnalysisTasks.CHOOSE_SEAT],  # 选择的座位
            'dwAll': 'N',
            'roomType': '00',
            'whatsSelect': 1,
            'seatDetailType': '000',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.REPEAT_SUBMIT_TOKEN
        }
        r = self.session.post(url=url, data=data, headers=self.headers)
        r.encoding = 'utf-8'
        print('confirmSingleForQueue=====' + r.text)
        # '{"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":{"submitStatus":true},"messages":[],"validateMessages":{}}'
        result = r.json()
        if 'submitStatus' in result['data']:
            return result['data']['submitStatus']
        return False

    # 查询订单等待信息
    def queryOrderWaitTime(self):
        self.headers["Referer"] = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?' \
              'random=' + get_13_time() + '&tourFlag=' + self.ticketInfoForPassengerForm['tour_flag'] \
              + '&_json_att=&REPEAT_SUBMIT_TOKEN=' + self.REPEAT_SUBMIT_TOKEN
        r = self.session.get(url=url, headers=self.headers)
        print('订单等待信息: ' + r.text)

        # {"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":{"queryOrderWaitTimeStatus":true,"count":0,"waitTime":-1,"requestId":6380241705273706046,"waitCount":0,"tourFlag":"dc","orderId":"ED31069951"},"messages":[],"validateMessages":{}}
        result = r.json()
        if result['httpstatus'] == 200 \
                and result['status'] \
                and result['data']['waitTime'] == -1 \
                and result['data']['orderId'] is not None:
            return True
        else:
            return False

    # 查询车次停靠站信息
    def queryZStop(self, stationName, stationstr):
        if self.task_info[AnalysisTasks.CARE_PASS] == 'N' \
                or self.task_info[AnalysisTasks.PASS_STATION] is None \
                or len(self.task_info[AnalysisTasks.PASS_STATION]) == 0:  # 不需要经过途径站也可以下单
            return True

        response = self.session.get('https://kyfw.12306.cn/otn/czxx/queryByTrainNo?'
                                    'train_no={}&from_station_telecode={}&to_station_telecode={}&depart_date={}'
                                    .format(stationstr,
                                            self.station[self.task_info[AnalysisTasks.FROM_STATION]],
                                            self.station[self.task_info[AnalysisTasks.TO_STATION]],
                                            self.task_info[AnalysisTasks.START_DATE]))

        response.encoding = 'utf-8'
        result = response.json()

        info = result['data']['data']
        for station in info:
            if self.task_info[AnalysisTasks.PASS_STATION] == station['station_name'] \
                    and station['isEnabled']:
                return True
        else:
            print('车次' + stationName + '没有经过' + self.task_info[AnalysisTasks.PASS_STATION] + '，不是我们的目标~~~')
            return False

    # 查询出发时间是否在我们行动的范围内
    def queryActionTime(self, stationName, startTime):
        if self.task_info[AnalysisTasks.ACTION_TIME] is None \
                or len(self.task_info[AnalysisTasks.ACTION_TIME]) == 0:
            return True

        startTime = startTime[0:2]
        lstActionTime = self.task_info[AnalysisTasks.ACTION_TIME].split('-')
        if int(lstActionTime[0]) <= int(startTime) <= int(lstActionTime[1]):
            return True
        else:
            print('车次' + stationName + '出发时间为' + startTime + '点，不是我们的目标~~~')
            return False

    # 盗贼行为
    def robber(self):
        if robber.get_checkUser():  # 检查用户
            tResult = robber.postSubmitOrderRequest()  # 预定订单界面
            if tResult[0] == 0:  # 成功
                robber.postInitDc()  # 初始化下单界面
                if robber.postetPassengerDTOs():  # 获取联系人信息
                    if robber.checkOrderInfo():  # 检查订单
                        time.sleep(3)
                        if robber.getQueueCount():  # 获取订单数量信息
                            print('开始下单~~~')
                            robber.confirmSingleForQueue()  # 下单
                            isSuccess = robber.queryOrderWaitTime()  # 获取等待时间
                            time.sleep(3)
                            isSuccess = robber.queryOrderWaitTime()  # 获取等待时间
                            return isSuccess
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                if tResult[0] == 2:
                    return False
                elif tResult[0] == 1:
                    print(tResult[1])
                    return True
        else:
            return False


if __name__ == '__main__':
    # checkYanZheng('0,3')
    robber = Robber()
    robber.get_init()
    robber.get_newpasscode()
    yan = robber.getImg()
    chek = False

    startTime = time.time()  # 开始时间

    # 只有验证成功后才能执行登录操作
    while not chek:
        chek = robber.checkYanZheng(yan)
        if chek:
            print('验证通过!')
            robber.login()
            robber.userLogin()
            robber.passport()
            robber.getjs()
            robber.post_uamtk()
            robber.post_uamauthclient()
            robber.get_userLogin()
            robber.get_leftTicket()
            robber.get_GetJS()
            robber.get_qufzjql()
            robber.get_otzizfc()

            continueAction = True
            while continueAction:
                try:
                    lstRequest = robber.queryZ()
                    idx = 0

                    # 指定车次
                    if len(robber.task_info[AnalysisTasks.TASK_TARGET].strip()) > 0:
                        lstTarget = robber.task_info[AnalysisTasks.TASK_TARGET].split('|')
                    else:
                        lstTarget = []

                    try:
                        while True and len(lstRequest) > 0 and continueAction:
                            info = lstRequest[idx]
                            dandulist = str(info).split('|')
                            # print(dandulist)

                            if dandulist[3] in lstTarget or len(lstTarget) == 0:  # 找到目标或者任一目标对象即可
                                print(dandulist[3] + "\t" + dandulist[30])  # 拿到二等座信息
                                if robber.queryZStop(dandulist[3], dandulist[2]) \
                                        and robber.queryActionTime(dandulist[3], dandulist[8]):  # 检查途径站，启动时间
                                    robber.secretStr = dandulist[0]
                                    isSuccess = robber.robber()
                                    if not isSuccess:
                                        print('行动失败，继续监控目标~~~')
                                        time.sleep(3)
                                        idx += 1
                                        if idx == len(lstRequest):
                                            idx = 0
                                    else:
                                        print('陈Sir，任务完成~~~')
                                        endTime = time.time()
                                        print('总共费时: ' + str(endTime - startTime) + '秒')
                                        continueAction = False

                                        break
                                else:
                                    time.sleep(3)
                                    idx += 1
                                    if idx == len(lstRequest):
                                        idx = 0
                            else:
                                idx += 1
                                if idx == len(lstRequest):
                                    idx = 0

                    except Exception as err:
                        print('车票信息失效，请重新查询!{}'.format(err))
                        time.sleep(5)

                except Exception as err:
                    print('信息失效，请重新验证!{}'.format(err))
                    time.sleep(3)
                    chek = False
                    yan = robber.getImg()
                    break
        else:
            print('验证失败，请重新验证!')
            chek = False
            yan = robber.getImg()
