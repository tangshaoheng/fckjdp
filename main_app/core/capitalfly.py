# -*- coding: utf-8 -*-
from __future__ import division

from main_app.core.utils.mail import mail_sender
from main_app.core.func.func import pagination,capital_flow
from main_app.core.utils.logger import logger
import datetime

log = logger('log_instance')

if __name__ == '__main__':
    pagination()
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    capital_list = capital_flow()

    def listrostring_cant_up(list):
        '涨停'
        string = ''
        for list_item in list:
                if list_item[2]>=9.8:
                    string += '代码：'+list_item[0]+'---'+'名称:'+list_item[1]+'---'+'涨幅:'+str(list_item[2])+'---'+'行业：'+list_item[3]+'<br>'
        return string
    def listrostring_can_buy(list):
        '未涨停，还可以购买'
        string = ''
        for list_item in list:
                if list_item[2]< 9.6:
                    string += '代码：'+list_item[0]+'---'+'名称:'+list_item[1]+'---'+'涨幅:'+str(list_item[2])+'---'+'行业：'+list_item[3]+'<br>'
        return string

    def listrostring_can_buy_8(list):
        '涨幅5-8'
        string = ''
        for list_item in list:
                if list_item[2] >5 and list_item[2]< 8:
                    string += '代码：'+list_item[0]+'---'+'名称:'+list_item[1]+'---'+'涨幅:'+str(list_item[2])+'---'+'行业：'+list_item[3]+'<br>'
        return string

    def listrostring_can_buy_5(list):
        '涨幅0-5'
        string = ''
        for list_item in list:
                if list_item[2] >0 and list_item[2]<= 5:
                    string += '代码：'+list_item[0]+'---'+'名称:'+list_item[1]+'---'+'涨幅:'+str(list_item[2])+'---'+'行业：'+list_item[3]+'<br>'
        return string
    def listrostring_can_buy_0(list):
        '涨幅0-5'
        string = ''
        for list_item in list:
                if list_item[2]<= 0:
                    string += '代码：'+list_item[0]+'---'+'名称:'+list_item[1]+'---'+'涨幅:'+str(list_item[2])+'---'+'行业：'+list_item[3]+'<br>'
        return string

    subject = u'标的汇总'
    send_string = '口号：喝最烈的酒，日最野的狗<br> <br>' \
                  '现在时间：{time}，<br>' \
                  ' <br>' \
                  ' <br>' \
                  '已经涨停：<br> {cant_buy}' \
                  ' <br>' \
                  ' <br>' \
                  '未涨停：<br> {can_buy}' \
                  ' <br>' \
                  ' <br>' \
                  '涨幅5-8：<br> {can_buy_8}' \
                  ' <br>' \
                  ' <br>' \
                  '涨幅0-5：<br> {can_buy_5}' \
                  ' <br>' \
                  ' <br>' \
                  '涨幅负：<br> {can_buy_0}' \
                  ' <br>'.format(time = nowTime,
                                 cant_buy = listrostring_cant_up(capital_list),
                                 can_buy = listrostring_can_buy(capital_list),
                                 can_buy_8 = listrostring_can_buy_8(capital_list),
                                 can_buy_5 = listrostring_can_buy_5(capital_list),
                                 can_buy_0= listrostring_can_buy_0(capital_list)
                                 )

    try:
        mail_sender(subject,send_string)
        log.info(u'邮件发送成功')

    except Exception as e:
        log.error(str(e))
