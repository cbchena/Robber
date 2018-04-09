import json
import re

import time
from urllib.parse import unquote

import os

str0 = """
var can_add = 'Y';
           var member_tourFlag = 'dc';
  		   var IsStudentDate=true;
           var init_seatTypes=[{'end_station_name':null,'end_time':null,'id':'M','start_station_name':null,'start_time':null,'value':'\u4E00\u7B49\u5EA7'},{'end_station_name':null,'end_time':null,'id':'O','start_station_name':null,'start_time':null,'value':'\u4E8C\u7B49\u5EA7'}];

           var defaultTicketTypes=[{'end_station_name':null,'end_time':null,'id':'1','start_station_name':null,'start_time':null,'value':'\u6210\u4EBA\u7968'},{'end_station_name':null,'end_time':null,'id':'2','start_station_name':null,'start_time':null,'value':'\u513F\u7AE5\u7968'},{'end_station_name':null,'end_time':null,'id':'3','start_station_name':null,'start_time':null,'value':'\u5B66\u751F\u7968'},{'end_station_name':null,'end_time':null,'id':'4','start_station_name':null,'start_time':null,'value':'\u6B8B\u519B\u7968'}];

           var init_cardTypes=[{'end_station_name':null,'end_time':null,'id':'1','start_station_name':null,'start_time':null,'value':'\u4E8C\u4EE3\u8EAB\u4EFD\u8BC1'},{'end_station_name':null,'end_time':null,'id':'C','start_station_name':null,'start_time':null,'value':'\u6E2F\u6FB3\u901A\u884C\u8BC1'},{'end_station_name':null,'end_time':null,'id':'G','start_station_name':null,'start_time':null,'value':'\u53F0\u6E7E\u901A\u884C\u8BC1'},{'end_station_name':null,'end_time':null,'id':'B','start_station_name':null,'start_time':null,'value':'\u62A4\u7167'}];

           var ticket_seat_codeMap={'3':[{'end_station_name':null,'end_time':null,'id':'O','start_station_name':null,'start_time':null,'value':'\u4E8C\u7B49\u5EA7'}],'2':[{'end_station_name':null,'end_time':null,'id':'M','start_station_name':null,'start_time':null,'value':'\u4E00\u7B49\u5EA7'},{'end_station_name':null,'end_time':null,'id':'O','start_station_name':null,'start_time':null,'value':'\u4E8C\u7B49\u5EA7'}],'1':[{'end_station_name':null,'end_time':null,'id':'M','start_station_name':null,'start_time':null,'value':'\u4E00\u7B49\u5EA7'},{'end_station_name':null,'end_time':null,'id':'O','start_station_name':null,'start_time':null,'value':'\u4E8C\u7B49\u5EA7'}],'4':[{'end_station_name':null,'end_time':null,'id':'M','start_station_name':null,'start_time':null,'value':'\u4E00\u7B49\u5EA7'},{'end_station_name':null,'end_time':null,'id':'O','start_station_name':null,'start_time':null,'value':'\u4E8C\u7B49\u5EA7'}]};

           var ticketInfoForPassengerForm={'cardTypes':[{'end_station_name':null,'end_time':null,'id':'1','start_station_name':null,'start_time':null,'value':'\u4E8C\u4EE3\u8EAB\u4EFD\u8BC1'},{'end_station_name':null,'end_time':null,'id':'C','start_station_name':null,'start_time':null,'value':'\u6E2F\u6FB3\u901A\u884C\u8BC1'},{'end_station_name':null,'end_time':null,'id':'G','start_station_name':null,'start_time':null,'value':'\u53F0\u6E7E\u901A\u884C\u8BC1'},{'end_station_name':null,'end_time':null,'id':'B','start_station_name':null,'start_time':null,'value':'\u62A4\u7167'}],'isAsync':'1','key_check_isChange':'EECCCAFC0A231370287C3A80939E942953D5EB0F1DA4EC9FCBFC93D3','leftDetails':['\u4E00\u7B49\u5EA7(171.00\u5143)\u6709\u7968','\u4E8C\u7B49\u5EA7(107.00\u5143)\u6709\u7968','\u65E0\u5EA7(107.00\u5143)\u6709\u7968'],'leftTicketStr':'R%2F8D4O3IZmCCP7pyrZ7%2FDNZeyr0IONd0fG1v1U1agQ1pFMS5','limitBuySeatTicketDTO':{'seat_type_codes':[{'end_station_name':null,'end_time':null,'id':'M','start_station_name':null,'start_time':null,'value':'\u4E00\u7B49\u5EA7'},{'end_station_name':null,'end_time':null,'id':'O','start_station_name':null,'start_time':null,'value':'\u4E8C\u7B49\u5EA7'}],'ticket_seat_codeMap':{'3':[{'end_station_name':null,'end_time':null,'id':'O','start_station_name':null,'start_time':null,'value':'\u4E8C\u7B49\u5EA7'}],'2':[{'end_station_name':null,'end_time':null,'id':'M','start_station_name':null,'start_time':null,'value':'\u4E00\u7B49\u5EA7'},{'end_station_name':null,'end_time':null,'id':'O','start_station_name':null,'start_time':null,'value':'\u4E8C\u7B49\u5EA7'}],'1':[{'end_station_name':null,'end_time':null,'id':'M','start_station_name':null,'start_time':null,'value':'\u4E00\u7B49\u5EA7'},{'end_station_name':null,'end_time':null,'id':'O','start_station_name':null,'start_time':null,'value':'\u4E8C\u7B49\u5EA7'}],'4':[{'end_station_name':null,'end_time':null,'id':'M','start_station_name':null,'start_time':null,'value':'\u4E00\u7B49\u5EA7'},{'end_station_name':null,'end_time':null,'id':'O','start_station_name':null,'start_time':null,'value':'\u4E8C\u7B49\u5EA7'}]},'ticket_type_codes':[{'end_station_name':null,'end_time':null,'id':'1','start_station_name':null,'start_time':null,'value':'\u6210\u4EBA\u7968'},{'end_station_name':null,'end_time':null,'id':'2','start_station_name':null,'start_time':null,'value':'\u513F\u7AE5\u7968'},{'end_station_name':null,'end_time':null,'id':'3','start_station_name':null,'start_time':null,'value':'\u5B66\u751F\u7968'},{'end_station_name':null,'end_time':null,'id':'4','start_station_name':null,'start_time':null,'value':'\u6B8B\u519B\u7968'}]},'maxTicketNum':'5','orderRequestDTO':{'adult_num':0,'apply_order_no':null,'bed_level_order_num':null,'bureau_code':null,'cancel_flag':null,'card_num':null,'channel':null,'child_num':0,'choose_seat':null,'disability_num':0,'end_time':{'date':1,'day':4,'hours':9,'minutes':17,'month':0,'seconds':0,'time':4620000,'timezoneOffset':-480,'year':70},'exchange_train_flag':'0','from_station_name':'\u6DF1\u5733\u5317','from_station_telecode':'IOQ','get_ticket_pass':null,'id_mode':'Y','isShowPassCode':null,'leftTicketGenTime':null,'order_date':null,'passengerFlag':null,'realleftTicket':null,'reqIpAddress':null,'reqTimeLeftStr':null,'reserve_flag':'A','seat_detail_type_code':null,'seat_type_code':null,'sequence_no':null,'start_time':{'date':1,'day':4,'hours':7,'minutes':0,'month':0,'seconds':0,'time':-3600000,'timezoneOffset':-480,'year':70},'start_time_str':null,'station_train_code':'D3126','student_num':0,'ticket_num':0,'ticket_type_order_num':null,'to_station_name':'\u6F6E\u6C55','to_station_telecode':'CBQ','tour_flag':'dc','trainCodeText':null,'train_date':{'date':15,'day':4,'hours':0,'minutes':0,'month':2,'seconds':0,'time':1521043200000,'timezoneOffset':-480,'year':118},'train_date_str':null,'train_location':null,'train_no':'6i000D312606','train_order':null,'varStr':null},'purpose_codes':'00','queryLeftNewDetailDTO':{'BXRZ_num':'-1','BXRZ_price':'0','BXYW_num':'-1','BXYW_price':'0','EDRZ_num':'-1','EDRZ_price':'0','EDSR_num':'-1','EDSR_price':'0','ERRB_num':'-1','ERRB_price':'0','GG_num':'-1','GG_price':'0','GR_num':'-1','GR_price':'0','HBRW_num':'-1','HBRW_price':'0','HBRZ_num':'-1','HBRZ_price':'0','HBYW_num':'-1','HBYW_price':'0','HBYZ_num':'-1','HBYZ_price':'0','RW_num':'-1','RW_price':'0','RZ_num':'-1','RZ_price':'0','SRRB_num':'-1','SRRB_price':'0','SWZ_num':'-1','SWZ_price':'0','TDRZ_num':'-1','TDRZ_price':'0','TZ_num':'-1','TZ_price':'0','WZ_num':'147','WZ_price':'01070','WZ_seat_type_code':'O','YB_num':'-1','YB_price':'0','YDRZ_num':'-1','YDRZ_price':'0','YDSR_num':'-1','YDSR_price':'0','YRRB_num':'-1','YRRB_price':'0','YW_num':'-1','YW_price':'0','YYRW_num':'-1','YYRW_price':'0','YZ_num':'-1','YZ_price':'0','ZE_num':'414','ZE_price':'01070','ZY_num':'58','ZY_price':'01710','arrive_time':'0917','control_train_day':'','controlled_train_flag':null,'controlled_train_message':null,'day_difference':null,'end_station_name':null,'end_station_telecode':null,'from_station_name':'\u6DF1\u5733\u5317','from_station_telecode':'IOQ','is_support_card':null,'lishi':'02:17','seat_feature':'','start_station_name':null,'start_station_telecode':null,'start_time':'0700','start_train_date':'','station_train_code':'D3126','to_station_name':'\u6F6E\u6C55','to_station_telecode':'CBQ','train_class_name':null,'train_no':'6i000D312606','train_seat_feature':'','yp_ex':''},'queryLeftTicketRequestDTO':{'arrive_time':'09:17','bigger20':'Y','exchange_train_flag':'0','from_station':'IOQ','from_station_name':'\u6DF1\u5733\u5317','from_station_no':'01','lishi':'02:17','login_id':null,'login_mode':null,'login_site':null,'purpose_codes':'00','query_type':null,'seatTypeAndNum':null,'seat_types':'OMO','start_time':'07:00','start_time_begin':null,'start_time_end':null,'station_train_code':'D3126','ticket_type':null,'to_station':'CBQ','to_station_name':'\u6F6E\u6C55','to_station_no':'06','train_date':'20180315','train_flag':null,'train_headers':null,'train_no':'6i000D312606','useMasterPool':true,'useWB10LimitTime':true,'usingGemfireCache':false,'ypInfoDetail':'R%2F8D4O3IZmCCP7pyrZ7%2FDNZeyr0IONd0fG1v1U1agQ1pFMS5'},'tour_flag':'dc','train_location':'Q6'};

           var orderRequestDTO={'adult_num':0,'apply_order_no':null,'bed_level_order_num':null,'bureau_code':null,'cancel_flag':null,'card_num':null,'channel':null,'child_num':0,'choose_seat':null,'disability_num':0,'end_time':{'date':1,'day':4,'hours':9,'minutes':17,'month':0,'seconds':0,'time':4620000,'timezoneOffset':-480,'year':70},'exchange_train_flag':'0','from_station_name':'\u6DF1\u5733\u5317','from_station_telecode':'IOQ','get_ticket_pass':null,'id_mode':'Y','isShowPassCode':null,'leftTicketGenTime':null,'order_date':null,'passengerFlag':null,'realleftTicket':null,'reqIpAddress':null,'reqTimeLeftStr':null,'reserve_flag':'A','seat_detail_type_code':null,'seat_type_code':null,'sequence_no':null,'start_time':{'date':1,'day':4,'hours':7,'minutes':0,'month':0,'seconds':0,'time':-3600000,'timezoneOffset':-480,'year':70},'start_time_str':null,'station_train_code':'D3126','student_num':0,'ticket_num':0,'ticket_type_order_num':null,'to_station_name':'\u6F6E\u6C55','to_station_telecode':'CBQ','tour_flag':'dc','trainCodeText':null,'train_date':{'date':15,'day':4,'hours':0,'minutes':0,'month':2,'seconds':0,'time':1521043200000,'timezoneOffset':-480,'year':118},'train_date_str':null,'train_location':null,'train_no':'6i000D312606','train_order':null,'varStr':null};

           var init_limit_ticket_num='5';

           var oldTicketDTOs="";

           var goOrderDTO="";

           var gqComeFrom="";

           var transport_in_SF=false;str
"""

ticketInfoForPassengerForm = re.findall("ticketInfoForPassengerForm=(.*);", str0)

str1 = re.search("ticketInfoForPassengerForm=(.*?);", str0).group(1)
#print(str1)
str1 = str1.replace("'",'"')
obj = json.loads(str1)

print(obj['orderRequestDTO']['train_date']['time'])
print(time.strftime("%a %b %d %Y %H:%M:%S GMT+0800 (CST)", time.localtime(obj['orderRequestDTO']['train_date']['time'] / 1000)))
print(obj['orderRequestDTO']['train_no'])
print(obj['orderRequestDTO']['station_train_code'])
print(obj['orderRequestDTO']['from_station_telecode'])
print(obj['orderRequestDTO']['to_station_telecode'])
print(obj['queryLeftTicketRequestDTO']['ypInfoDetail'])
print(obj['purpose_codes'])
print(obj['train_location'])
print(obj['tour_flag'])


t = json.loads('{"count":"5","ticket":"545,144","op_2":"false","countT":"0","op_1":"true"}')

print(t['ticket'].split(','))

'R%2F8D4O3IZmCCP7pyrZ7%2FDNZeyr0IONd0fG1v1U1agQ1pFMS5'
ul = 'R%2F8D4O3IZmCCP7pyrZ7%2FDNZeyr0IONd0fG1v1U1agQ1pFMS5'
print(unquote(ul))

s = '您还有未处理的订单，请您到<a href="../queryOrder/initNoComplete">[未完成订单]</a>进行处理!'
p = re.compile('^您还有未处理的订单，请您到.*')
if p.search(s):
    print("陈Sir，您有未处理的订单")

print((1, '陈Sir，您有未处理的订单')[0])

s = '{"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":{"submitStatus":true},"messages":[],"validateMessages":{}}'
j = json.loads(s)
print('submitStatus' in j['data'])

s = '{"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":{"queryOrderWaitTimeStatus":true,"count":0,"waitTime":-1,"requestId":6380241705273706046,"waitCount":0,"tourFlag":"dc","orderId":null},"messages":[],"validateMessages":{}}'
j = json.loads(s)
print(j['data']['orderId'])


s = 'https://kyfw.12306.cn/otn/leftTicket/queryO?' \
    'leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&' \
    'leftTicketDTO.to_station={}&purpose_codes=ADULT'

print(s.format('2018-03-16', 'IOQ', 'CBQ'))

print(time.strftime('%Y-%m-%d', time.localtime()))


print('a'.split('|'))


# yield函数
def fab(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        # print b
        a, b = b, a + b
        n = n + 1

for n in fab(5):
    print(n)

s1 = time.strptime('2018-03-17 11:36:46', '%Y-%m-%d %H:%M:%S')
s2 = time.strptime('2018-03-17 12:36:47', '%Y-%m-%d %H:%M:%S')
print(int(time.mktime(s2) - time.mktime(s1)))
print(time.mktime(s2))
print(time.time())

t = 'D2304.txt'
print(t[0:t.rindex('.')])

# if not os.path.exists('data_' + time.strftime('%Y-%m-%d', time.localtime())):
#     os.mkdir('data_' + time.strftime('%Y-%m-%d', time.localtime()))

file = open('target_info/datab/D7408.txt', 'r')
for line in file:
    print(line)
