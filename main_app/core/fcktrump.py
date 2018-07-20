# -*- coding: utf-8 -*-
from __future__ import division
from utils.mail import mail_sender
from func.func import updown
from func.func import cant_up_item
from func.func import warn,suggest,global_index,pagination
from utils.logger import logger
import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
log = logger('xxxx')


if __name__ == '__main__':
    pagination()
    master = updown()
    up_item = cant_up_item()
    global_index = global_index()
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    def listrostring(list):
        string = ''
        for list_item in list:
                string += '代码：'+list_item[0]+'---'+'名称:'+list_item[1]+'---'+'次数:'+list_item[2]+'---'+'原因：'+list_item[3]+'<br>'
        return string
    subject = str(round(master.get('down') / (master.get('up') + master.get('down') ),3) *100)+'%-down'+'--'+\
              str(round(master.get('up') / (master.get('up') + master.get('down') ),3) *100)+'%-up'
    send_string = '口号：喝最烈的酒，日最野的狗<br> <br>' \
                  '现在时间：{time}，<br>' \
                  ' <br>' \
                  ' <br>' \
                  '上证指：{sz1A0001}，涨跌幅：{zdf_1a0001}<br>' \
                  '深圳指：{sh399001}，涨跌幅：{zdf_399001}<br>' \
                  ' <br>' \
                  '上涨数：{up}，<br>' \
                  '下跌数：{down}，<br>' \
                  '涨跌比:{ratio},<br>' \
                  '涨停数：{cant_up}，<br>' \
                  '跌停数：{cant_down},<br>' \
                  '昨日涨停今日受益：{uptodown} <br>' \
                  '大盘评级：{level}， <br>' \
                  ' <br>' \
                  '建议：{warn}， <br>' \
                  '是否开仓：{suggest}， <br>' \
                  ' <br>' \
                  '涨停票：<br> {upcant}'.format(time = nowTime,
                            sh399001 = global_index[0].get('zxj'),
                            zdf_399001 = global_index[0].get('zdf'),
                            sz1A0001 = global_index[1].get('zxj'),
                            zdf_1a0001 =global_index[1].get('zdf'),
                            up =master.get('up'),
                            down = master.get('down') ,
                            ratio = master.get('ratio'),
                            cant_up = master.get('cant_up'),
                            cant_down = master.get('cant_down'),
                             warn= warn(master.get('level')),
                            level = master.get('level'),
                            uptodown = master.get('uptodown'),
                            suggest = suggest(master.get('ratio')),
                            upcant = listrostring(up_item)
                            )

    try:
        mail_sender(subject,send_string)
        log.info(u'邮件发送成功')

    except Exception, e:
        log.error(str(e))
