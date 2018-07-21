# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from main_app.base.models import BaseModel
from django.db import models
from django.contrib import admin
from django.utils.timezone import now
now = now()


class TodayReport(BaseModel):
    """
        大盘总参
    """

    sz1A0001 = models.CharField(max_length=10, verbose_name=u'上证指',null=True,blank=True)
    zdf_1a0001 = models.CharField(max_length=10, verbose_name=u'上证指涨跌幅',null=True,blank=True)
    sh399001 = models.CharField(max_length=10, verbose_name=u'深圳指',null=True,blank=True)
    zdf_399001 = models.CharField(max_length=10, verbose_name=u'深圳指涨跌幅',null=True,blank=True)
    uptodown = models.CharField(max_length=10, verbose_name=u'昨日涨停今日受益',null=True,blank=True)
    ratio = models.CharField(max_length=10, verbose_name=u'涨跌比',null=True,blank=True)
    level = models.CharField(max_length=10, verbose_name=u'大盘评级',null=True,blank=True)
    up = models.CharField(max_length=10, verbose_name=u'上涨数',null=True,blank=True)
    down = models.CharField(max_length=10, verbose_name=u'下跌数',null=True,blank=True)
    cant_up = models.CharField(max_length=10, verbose_name=u'涨停数',null=True,blank=True)
    cant_down = models.CharField(max_length=10, verbose_name=u'跌停数',null=True,blank=True)

    class Meta:
        verbose_name = 'TodayReport'
        verbose_name_plural = 'TodayReport'
        ordering = ['-create_time']

    def save(self, * args, ** kwargs):
        if len(self.__class__.objects.filter(create_time__year = now.year, create_time__month=now.month, create_time__day=now.day))>=1:
            raise Exception(u'多次插入')
        super(self.__class__, self).save(*args, ** kwargs)

    def __unicode__(self):
        return self.sz1A0001


class CantUpToDay(BaseModel):
    """
    当日涨停以及涨停过的票
    """

    name = models.CharField(max_length=45, verbose_name=u'名字',null=True,blank=True)
    code = models.CharField(max_length=45, verbose_name=u'代码',null=True,blank=True)

    class Meta:
        verbose_name = 'CantUpToDay'
        verbose_name_plural = 'CantUpToDay'
        ordering = ['-create_time']

    def __unicode__(self):
        return self.name


class CantUpToDayAfter(BaseModel):
    """
    当日涨停的票、盘后统计的
    """

    name = models.CharField(max_length=45, verbose_name=u'名字',null=True,blank=True)
    code = models.CharField(max_length=45, verbose_name=u'代码',null=True,blank=True)

    class Meta:
        verbose_name = 'CantUpToDayAfter'
        verbose_name_plural = 'CantUpToDayAfter'
        ordering = ['-create_time']

    def __unicode__(self):
        return self.name


class CantDownToDay(BaseModel):
    """
    当日跌停以及跌停过的票
    """

    name = models.CharField(max_length=45, verbose_name=u'名字',null=True,blank=True)
    code = models.CharField(max_length=45, verbose_name=u'代码',null=True,blank=True)

    class Meta:
        verbose_name = 'CantDownToDay'
        verbose_name_plural = 'CantDownToDay'
        ordering = ['-create_time']

    def __unicode__(self):
        return self.name


class CantDownToDayAfter(BaseModel):
    """
    当日跌停的票、盘后统计的
    """

    name = models.CharField(max_length=45, verbose_name=u'名字',null=True,blank=True)
    code = models.CharField(max_length=45, verbose_name=u'代码',null=True,blank=True)

    class Meta:
        verbose_name = 'CantDownToDayAfter'
        verbose_name_plural = 'CantDownToDayAfter'
        ordering = ['-create_time']

    def __unicode__(self):
        return self.name


class Topic(BaseModel):
    """
    主题
    """

    topic = models.CharField(max_length=45, verbose_name=u'炒作主题', null=True, blank=True)

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topic'
        ordering = ['-create_time']

    def __unicode__(self):
        return self.topic


class Capitalfly1000(BaseModel):
    """
    资金流大于1000w
    """

    name = models.CharField(max_length=45, verbose_name=u'名字',null=True,blank=True)
    code = models.CharField(max_length=45, verbose_name=u'代码',null=True,blank=True)

    class Meta:
        verbose_name = 'Capitalfly1000'
        verbose_name_plural = 'Capitalfly1000'
        ordering = ['-create_time']

    def __unicode__(self):
        return self.name


class CapitalflyBig(BaseModel):
    """
    资金流大于1亿
    """

    name = models.CharField(max_length=45, verbose_name=u'名字', null=True, blank=True)
    code = models.CharField(max_length=45, verbose_name=u'代码', null=True, blank=True)

    class Meta:
        verbose_name = 'CapitalflyBig'
        verbose_name_plural = 'CapitalflyBig'
        ordering = ['-create_time']

    def __unicode__(self):
        return self.name


admin.site.register(TodayReport)