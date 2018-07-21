# -*- coding: utf-8 -*-
import scrapy
from ..items import SharesItem


class GjzqCrawlSpider(scrapy.Spider):
    name = 'gjzq_crawl'
    allowed_domains = ['10jqka.com.cn']
    # 活动次数最多
    url_actvite = 'http://data.10jqka.com.cn/ifmarket/lhbyyb/type/1/tab/sbcs/field/sbcs/sort/desc/page/{page_index}/'
    # 资金实力最强
    url_power = 'http://data.10jqka.com.cn/ifmarket/lhbyyb/type/1/tab/zjsl/field/zgczje/sort/desc/page/{page_index}/'
    # 抱团能力最强
    url_team = 'http://data.10jqka.com.cn/ifmarket/lhbyyb/type/1/tab/btcz/field/xsjs/sort/desc/page/{page_index}/'
    # 定义需要抓取的url -> list
    start_urls = []
    for i in range(1, 2):
        target_url = url_actvite.format(page_index=i)
        start_urls.append(target_url)

    def parse(self, response):
        quotes = response.xpath('//tbody/tr')
        for quote in quotes:
            # 实例一个容器保存爬取的信息
            item = SharesItem()
            tr_of_all_tds = quote.xpath('td')
            # "营业部的第二层链接"
            yyb_second_url = tr_of_all_tds[1].xpath('a/@href').extract_first()

            item['name'] = tr_of_all_tds[1].xpath('a/@title').extract_first()
            item['label'] = tr_of_all_tds[1].xpath('label/text()').extract_first(default="")
            item['sb_cnt'] = tr_of_all_tds[2].xpath('string(.)').extract_first()
            item['zj_sum'] = tr_of_all_tds[3].xpath('string(.)').extract_first()
            item['nn_sb_cnt'] = tr_of_all_tds[4].xpath('string(.)').extract_first()
            item['nn_buy_shares_cnt'] = tr_of_all_tds[5].xpath('string(.)').extract_first()
            item['nn_three_date_bab_success_rate'] = tr_of_all_tds[6].xpath('string(.)').extract_first()

            yield item