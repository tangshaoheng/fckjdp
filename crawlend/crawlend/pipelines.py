# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from _md5 import md5
from datetime import datetime

import pymysql
from twisted.enterprise import adbapi
from twisted.python import failure, log
from .items import SharesItem


class CrawlendPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, SharesItem):
            item.save()
            return item


class SharesPipeline(object):

    def __init__(self):
        # 打开文件
        self.file = open('data.json', 'w', encoding='utf-8')

    # 该方法用于处理数据
    def process_item(self, item, spider):
        # 读取item中的数据
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # 写入文件
        self.file.write(line)
        # 返回item
        return item

    # 该方法在spider被开启时被调用。
    def open_spider(self, spider):
        pass

    # 该方法在spider被关闭时被调用。
    def close_spider(self, spider):
        self.file.close()


class MySQLStoreYybPipeline(object):

    def __init__(self, db_pool):
        # 创建数据库连接
        print("进来了")
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):
        db_args = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        db_pool = adbapi.ConnectionPool('pymysql', **db_args)
        return cls(db_pool)

    # pipeline默认调用
    def process_item(self, item, spider):
        d = self.db_pool.runInteraction(self._do_upd_insert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d

    # 将每行更新或写入数据库中
    def _do_upd_insert(self, conn, item, spider):
        yyb_name_md5_id = self._get_name_md5_id(item)

        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        conn.execute("""
            select 1 from yyb_ranking where yyb_name_md5_id = %s
        """, yyb_name_md5_id)
        ret = conn.fetchone()
        ret = False

        if ret:
            conn.execute("""
                update yyb_ranking set yyb_name = %s, label = %s, sb_cnt = %s, zj_sum = %s, 
                nn_sb_cnt = %s, nn_buy_shares_cnt = %s, nn_three_date_bab_success_rate = %s	
            """, (item['name'], item['label'], item['sb_cnt'], item['zj_sum'],
                  item['nn_sb_cnt'], item['nn_buy_shares_cnt'], item['nn_three_date_bab_success_rate']))
        else:
            conn.execute("""
            insert into yyb_ranking(yyb_name, label, sb_cnt, zj_sum, 
            nn_sb_cnt, nn_buy_shares_cnt, nn_three_date_bab_success_rate) 
            values(%s, %s, %s, %s, %s, %s, %s)
            """, (item['name'], item['label'], item['sb_cnt'],
                  item['zj_sum'], item['nn_sb_cnt'], item['nn_buy_shares_cnt'],
                  item['nn_three_date_bab_success_rate']))

    # 获取name的md5编码
    def _get_name_md5_id(self, item):
        # name进行md5处理，为避免重复抓取数据
        return md5(item['name']).hexdigest()

    # 判断昨日数据是否已经入
    # def _has_yesterday_data(self, conn):
    #     flag = False
    #
    #     conn.execute("""
    #                 select 1 from yyb_ranking where created_at = %s
    #             """, (created_at,))
    #     ret = conn.fetchone()
    #     return md5(item['name']).hexdigest()

    # 异常处理
    def _handle_error(self, failue, item, spider):
        log.err(failure)
