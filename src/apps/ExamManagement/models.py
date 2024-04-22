# -*- coding: utf-8 -*-
# @Time    : 2024/02/21 13:43:31
# @Author  : DannyDong
# @File    : models.py
# @Describe: Exam应用模型

import uuid

from django.db import models
from django.utils import timezone


class Exam(models.Model):
    class Meta:
        db_table = 'exam'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 绑定试卷ID
    paper_id = models.CharField(max_length=255, help_text='绑定试卷ID')
    # 考试名称
    title = models.CharField(max_length=100, help_text='考试名称')
    # 考试开始时间
    start_time = models.DateTimeField(verbose_name='考试开始时间')
    # 考试结束时间
    end_time = models.DateTimeField(verbose_name='考试结束时间')
    # 及格分数
    pass_mark = models.PositiveIntegerField(default=60, help_text='及格分数')
    # 是否发布
    is_published = models.BooleanField(default=False, help_text='是否发布')
    # 发布时间
    publish_date = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')
    # 是否删除
    is_deleted = models.BooleanField(default=False, help_text='是否删除')
    # 备注
    remark = models.TextField(blank=True, null=True, help_text='备注')
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
