# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from main_app.models import SharesItem


class CrawlendItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class SharesItem(DjangoItem):
    django_model = SharesItem


class NoDjangoSharesItem(scrapy.Item):
    # 营业部名称
    name = scrapy.Field()
    # 营业部label
    label = scrapy.Field()
    # 上榜次数
    sb_cnt = scrapy.Field()
    # 合计动用资金
    zj_sum = scrapy.Field()
    # 年内上榜次数
    nn_sb_cnt = scrapy.Field()
    # 年内买入股票只数
    nn_buy_shares_cnt = scrapy.Field()
    # 年内三日跟买成功率
    nn_three_date_bab_success_rate = scrapy.Field()
