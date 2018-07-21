# -*- coding: utf-8 -*-
from __future__ import division

import requests
from conf.settings import tonghuashun_api,global_api,tonghuashun_post_search_api
import datetime
import time

s = requests.Session()
# 开启一个session

def get(url,data = None,header = None):
    '''
    :param url: URL
    :param data: 参数
    :param header: 请求头
    :return: 未处理的response
    '''
    params = data
    if not header:
        header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.15 Safari/537.36'}
        response=s.get(url,headers=header,params=params)
    else:
        response = s.get(url,headers=header,params=params)
    return response

def post(url,data = None,header = None):
    '''
    :param url: URL
    :param data: 参数
    :param header: 请求头
    :return: 未处理的response
    '''

    data = data
    if not header:
        header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.15 Safari/537.36'}
        response =s.post(url,headers=header,data=data)
    else:
        response = s.post(url, headers=header, data=data)
    return response


def updown():
    "大盘总参：如果不是交易时间，则为前一个收盘数据，如果是交易时间，则为当下数据"
    ratio = {}
    api = tonghuashun_api
    try:
        r=get(api).json()
        print(r)
        up = r.get('zdfb_data').get('znum')
        "上涨数"
        down = r.get('zdfb_data').get('dnum')
        "下跌数"
        cant_up = r.get('zdt_data').get('last_zdt').get('ztzs')
        "涨停"
        cant_down = r.get('zdt_data').get('last_zdt').get('dtzs')
        "跌停"
        level = r.get('dppj_data')
        "大盘评级"
        uptodown =r.get('jrbx_data').get('last_zdf')
        "昨日涨停今日受益"
        updown = round(up/down,3)
        "涨跌比"
        ratio['up'] = up
        ratio['down'] = down
        ratio['ratio'] = updown
        ratio['cant_up'] = cant_up
        ratio['cant_down'] = cant_down
        ratio['level'] = level
        ratio['uptodown'] = uptodown
    except Exception as e:
        print(e)
    return ratio


def global_index():

    '''
    大盘指数
    :return:
    '''

    global_index = []
    try:
        try:
            r = get(global_api).json()
            global_index = r.get(u'中国').get('dataArr')
        except Exception as e:
            r = get(global_api).json()
            global_index = r.get(u'中国').get('dataArr')
    except Exception as e:
        r = get(global_api).json()
        global_index = r.get(u'中国').get('dataArr')
    return global_index


def pagination(perpage=70):

    '''
    :param perpage:  同花顺单页返回item个数
    :return:
    '''

    try:
        header = {
            'hexin-v': 'Ah9Nj1sjuPkzUrzl7_tej-BvqHiqhHPGjdl3FrFsursWKDFuuVQDdp2oB2fC',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
            }
        data = {
            'tid': 'stockpick',
            'w': u'大单流入大于1000万，流通市值小于51亿',
            'robot': '{"source":"Ths_iwencai_Xuangu","user_id":"425674582","log_info":"{\"other_info\":\"{\\\"eventId\\\":\\\"iwencai_pc_send_click\\\",\\\"ct\\\":1529713684261}\"}","user_name":"mo_425674582","version":"1.3"}'}
        r= post(tonghuashun_post_search_api,data).json()
        token = r.get('data').get('wencai_data').get('result').get('token')
        get_url = 'http://www.iwencai.com/stockpick/cache?token={token}&p=1&perpage={perpage}&changeperpage=1&showType=' \
                  '[%22%22,%22%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,' \
                  '%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22]'.format(token=token,perpage=perpage)
        get(get_url,header =header)
    except Exception:
        return False
    return True



def capital_flow():
    '''
    资金流
    :return:
    '''
    capital = []
    try:
        data = {
            'tid': 'stockpick',
            'w': u'大单流入大于1000万，流通市值小于51亿',
            'robot': '{"source":"Ths_iwencai_Xuangu","user_id":"425674582","log_info":"{\"other_info\":\"{\\\"eventId\\\":\\\"iwencai_pc_send_click\\\",\\\"ct\\\":1529713684261}\"}","user_name":"mo_425674582","version":"1.3"}'}
        response = post(tonghuashun_post_search_api, data).json()
        result = response.get('data').get('wencai_data').get('result').get('result')
        for item in result:
            capital.append([item[0],item[1],item[3],item[-3]])
    except Exception:
        return False
    return capital


def cant_down_item():

    '''
    当日跌停
    :return:
    '''

    cant_down = {}
    try:
        data = {
            'tid': 'stockpick',
            'w': u'跌停',
            'robot': {"source": "Ths_iwencai_Xuangu", "user_id": "425674582",
                "log_info": "{\"other_info\":\"{\\\"eventId\\\":\\\"iwencai_pc_send_click\\\",\\\"ct\\\":1529236182583}\"}",
                "user_name": "mo_425674582", "version": "1.3"}
            }
        response = post(tonghuashun_post_search_api,data=data).json()
        result= response.get('data').get('wencai_data').get('result').get('result')
    except Exception:
        return False
    return cant_down


def cant_up_item():
    '''
    当日涨停
    :return:
    '''

    up_list = []
    try:
        data = {
            'tid': 'stockpick',
            'w': u'涨停',
            'robot': {"source": "Ths_iwencai_Xuangu", "user_id": "425674582",
                "log_info": "{\"other_info\":\"{\\\"eventId\\\":\\\"iwencai_pc_send_click\\\",\\\"ct\\\":1529236182583}\"}",
                "user_name": "mo_425674582", "version": "1.3"}
            }
        response = post(tonghuashun_post_search_api,data=data).json()
        result = response.get('data').get('wencai_data').get('result').get('result')
        for item in result:
            up_list.append([item[0],item[1],item[-8],item[-7]])
    except Exception:
        return False
    return up_list


def buyday():
    '''
    判断是否是交易时间
    :return:
    '''

    worktime=['09:25:00','11:30:00','13:00:00','15:00:00']
    dayofweek = datetime.datetime.now().weekday()
    beginwork=datetime.datetime.now().strftime("%Y-%m-%d")+' '+worktime[0]
    endwork=datetime.datetime.now().strftime("%Y-%m-%d")+' '+worktime[1]
    beginwork_a=datetime.datetime.now().strftime("%Y-%m-%d")+' '+worktime[2]
    endwork_a=datetime.datetime.now().strftime("%Y-%m-%d")+' '+worktime[3]
    beginworkseconds=time.time()-time.mktime(time.strptime(beginwork, '%Y-%m-%d %H:%M:%S'))
    endworkseconds=time.time()-time.mktime(time.strptime(endwork, '%Y-%m-%d %H:%M:%S'))
    beginworkseconds_a =time.time()-time.mktime(time.strptime(beginwork_a, '%Y-%m-%d %H:%M:%S'))
    endworkseconds_a =time.time()-time.mktime(time.strptime(endwork_a, '%Y-%m-%d %H:%M:%S'))

    if (int(dayofweek) in range(5)) and int(beginworkseconds)>0 and int(endworkseconds)<0:
        return 1
    elif (int(dayofweek) in range(5)) and int(beginworkseconds_a)>0 and int(endworkseconds_a)<0:
        return 1
    else:
        return 0


def warn(r):
    u = u''
    if r<2.5:
        u = u"大盘风险极大，请勿参与"
    elif 2.5<=r and r <4 :
        u = u'大盘风险较大，请谨慎参与'
    elif 4<=r and r< 6:
        u = u'大盘震荡，适当参与'
    elif 6<=r and r<8:
        u = u'大盘走势良好，积极参与'
    else:
        u = u'大盘走势极好，积极参与'
    return  u

def suggest(r):
    if r >=1:
        return u'涨跌比：%s 涨跌比大于1，可以开仓' %r
    else:
        return u'涨跌比：%s 建议空仓' %r

if __name__ == '__main__':
    updown()


