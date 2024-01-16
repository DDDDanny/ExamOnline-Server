# -*- coding: utf-8 -*-
# @Time    : 2024/01/16 19:14:32
# @Author  : DannyDong
# @File    : models.py
# @Describe: Questions应用模型 


import uuid
from django.db import models
from django.utils import timezone


class Questions(models.Model):
    class Meta:
        db_table = 'questions'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 试题标题
    topic = models.TextField(max_length=500, help_text='试题标题')
    # 试题答案
    answer = models.TextField(max_length=500, help_text='试题答案')
    # 试题类型
    TYPE_CHOICES = [('select', 'Select'),('judge', 'Judge')]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='select', help_text='试题类型')
    # 试题状态
    status = models.BooleanField(default=True, help_text='试题状态')
    # 创建人
    created_user = models.CharField(max_length=255, help_text='创建人')
    # 创建时间
    created_at = models.DateTimeField(default=timezone.now, help_text='创建时间')
    # 更新人
    updated_user = models.CharField(max_length=255, null=True, help_text='更新人')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, null=True, help_text='更新时间')


if __name__ == '__main__':
    pass
