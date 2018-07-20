# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from base.models import BaseModel
from django.db import models
from django.contrib import admin
from django.utils.timezone import now
now = now()

class TodayReport(BaseModel):

    sh399001 = models.CharField(max_length=10, verbose_name=u'昨日涨停今日受益',null=True,blank=True)
    zdf_399001 = models.CharField(max_length=10, verbose_name=u'昨日涨停今日受益',null=True,blank=True)
    sz1A0001 = models.CharField(max_length=10, verbose_name=u'上证指',null=True,blank=True)
    zdf_1a0001 = models.CharField(max_length=10, verbose_name=u'上证指涨跌幅',null=True,blank=True)
    uptodown = models.CharField(max_length=10, verbose_name=u'昨日涨停今日受益',null=True,blank=True)
    ratio = models.CharField(max_length=10, verbose_name=u'涨跌比',null=True,blank=True)
    level = models.CharField(max_length=10, verbose_name=u'大盘评级',null=True,blank=True)
    up = models.CharField(max_length=10, verbose_name=u'上涨数',null=True,blank=True)
    down = models.CharField(max_length=10, verbose_name=u'下跌数',null=True,blank=True)
    cant_up = models.CharField(max_length=10, verbose_name=u'涨停数',null=True,blank=True)
    cant_down = models.CharField(max_length=10, verbose_name=u'跌停数',null=True,blank=True)

    #'uptodown': 1.63, 'ratio': 4.95, 'level': 5.5, 'up': 2752, 'down': 556, 'cant_up': 49, 'cant_down': 11
    # up = r.get('zdfb_data').get('znum')
    # "上涨数"
    # down = r.get('zdfb_data').get('dnum')
    # "下跌数"
    # cant_up = r.get('zdt_data').get('last_zdt').get('ztzs')
    # "涨停"
    # cant_down = r.get('zdt_data').get('last_zdt').get('dtzs')
    # "跌停"
    # level = r.get('dppj_data')
    # "大盘评级"
    # uptodown = r.get('jrbx_data').get('last_zdf')
    # "昨日涨停今日受益"
    # sh399001 = global_index[0].get('zxj'),
    # zdf_399001 = global_index[0].get('zdf'),
    # sz1A0001 = global_index[1].get('zxj'),
    # zdf_1a0001 = global_index[1].get('zdf'),

    class Meta:
        verbose_name = 'TodayReport'
        verbose_name_plural = 'TodayReport'
        ordering = ['-create_time']

    def save(self, * args, ** kwargs):
        if len(self.__class__.objects.filter(create_time__year = now.year, create_time__month=now.month, create_time__day=now.day))>=1:
            raise Exception,u'多次插入'
        super(self.__class__, self).save(*args, ** kwargs)

    def __unicode__(self):
        return self.number


class KnSec_top10(BaseModel):

    location = models.CharField(max_length=45, verbose_name=u'地理位置',null=True,blank=True)
    attack_times = models.IntegerField(verbose_name=u'总攻击ip数',null=True,blank=True)

    class Meta:
        verbose_name = 'KnSec_times_top10'
        verbose_name_plural = 'KnSec_times_top10'
        ordering = ['-create_time']

    def __unicode__(self):
        return self.location



admin.site.register(URL)