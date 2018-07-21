# -*- coding: utf-8 -*-
from __future__ import division
from main_app.core.utils.mail import mail_sender
from main_app.core.func.func import post,get
from main_app.core.utils.logger import logger
from bs4 import BeautifulSoup
from conf.settings import longhu,url_team,url_power,url_actvite,level

log = logger('log_instance')

if __name__ == '__main__':
  #[u'知名游资', u'一线游资', u'毒瘤', u'跟风高手', u'新股专家']
    level0 = []
    level1 = []
    level2 = []
    level3 = []
    level4 = []
    ditc_active = {}

    key = 1
    for x in range(1,40):
        target = url_actvite.format(pages =x)
        html = get(url=target).content
        soup = BeautifulSoup(html, "lxml")
        all_ = soup.find_all(class_="tl rel")
        for items in all_:
            try:
                ditc_active[key] = [items.find('label').get_text(),items.a.get('title'),items.a.get('href')]
                key+=1
            except Exception as e:
                print(e)
                pass
    key_power = 1
    ditc_power = {}
    for x in range(1,40):
        target = url_power.format(pages =x)
        html = get(url=target).content
        soup = BeautifulSoup(html, "lxml")
        all_ = soup.find_all(class_="tl rel")
        for items in all_:
            try:
                ditc_power[key_power] = [items.find('label').get_text(),items.a.get('title'),items.a.get('href')]
                key_power+=1
            except Exception as e:
                pass

    ditc_team = {}
    key_team = 1
    for x in range(1,40):
        target = url_team.format(pages =x)
        html = get(url=target).content
        soup = BeautifulSoup(html, "lxml")
        all_ = soup.find_all(class_="tl rel")
        for items in all_:
            try:
                ditc_team[key_team] = [items.find('label').get_text(),items.a.get('title'),items.a.get('href')]
                key_team+=1
            except Exception as e:
                pass

    for items in ditc_team.values():
        if items[0] == level[0]:
            level0.append(items[1])
        if items[0] == level[1]:
            level1.append(items[1])
        if items[0] == level[2]:
            level2.append(items[1])
        if items[0] == level[3]:
            level3.append(items[1])
        if items[0] == level[4]:
            level4.append(items[1])
    for items in ditc_power.values():
        if items[0] == level[0]:
            level0.append(items[1])
        if items[0] == level[1]:
            level1.append(items[1])
        if items[0] == level[2]:
            level2.append(items[1])
        if items[0] == level[3]:
            level3.append(items[1])
        if items[0] == level[4]:
            level4.append(items[1])

    for items in ditc_active.values():
        if items[0] == level[0]:
            level0.append(items[1])
        if items[0] == level[1]:
            level1.append(items[1])
        if items[0] == level[2]:
            level2.append(items[1])
        if items[0] == level[3]:
            level3.append(items[1])
        if items[0] == level[4]:
            level4.append(items[1])
    print('--')

    print(u'知名游资')
    for items in set(level0):
        print(items)

    print(u'一线游资')
    for items in set(level1):
        print(items)

    print(u'毒瘤')
    for items in set(level2):
        print(items)

    print(u'跟风高手')
    for items in set(level3):
        print(items)

    print(u'新股专家')
    for items in set(level4):
        print(items)