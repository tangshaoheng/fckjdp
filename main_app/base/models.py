# -*- coding: utf-8 -*-
from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    is_active = models.BooleanField(u'是否有效', default=True)

    class Meta:
        abstract = True

