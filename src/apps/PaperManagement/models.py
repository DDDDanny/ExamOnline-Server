# -*- coding: utf-8 -*-
# @Time    : 2024/02/06 10:07:03
# @Author  : DannyDong
# @File    : models.py
# @Describe: Paper应用模型 

import uuid

from django.db import models
from django.utils import timezone


class Paper(models.Model):
    class Meta:
        db_table = 'paper'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 试卷名称
    title = models.CharField(max_length=100, help_text='试卷标题')
    # 试卷描述
    description = models.TextField(blank=True, null=True, help_text='试卷描述')
    # 答题建议时长
    duration_minutes = models.PositiveIntegerField(default=60, help_text='答题建议时长')
    # 总分数
    total_marks = models.PositiveIntegerField(default=0, help_text='总分数')
    # 是否发布
    is_published = models.BooleanField(default=False, help_text='是否发布')
    # 发布时间
    publish_date = models.DateTimeField(null=True, blank=True, verbose_name='发布时间')
    # 是否属于公共试卷库
    is_public = models.BooleanField(default=False, help_text='是否属于公共试卷库')
    # 是否删除
    is_deleted = models.BooleanField(default=False, help_text='是否删除')
    # 创建人
    created_user = models.CharField(max_length=255, help_text='创建人')
    # 创建时间
    created_at = models.DateTimeField(default=timezone.now, help_text='创建时间')
    # 更新人
    updated_user = models.CharField(max_length=255, null=True, help_text='更新人')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, null=True, help_text='更新时间')


class PaperQuestions(models.Model):
    class Meta:
        db_table = 'paper_questions'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 试卷名称
    paper_id = models.CharField(max_length=50, help_text='试卷ID')
    # 试题ID
    question_id = models.CharField(max_length=50, help_text='试题ID')
    # 试题顺序
    sequence_number = models.PositiveIntegerField(default=1, help_text='试题顺序')
    # 试题分数
    marks = models.FloatField(default=5, help_text='试题分数')
    # 所属模块
    module = models.CharField(max_length=255, help_text='所属模块')
    # 创建时间
    created_at = models.DateTimeField(default=timezone.now, help_text='创建时间')


class PaperModule(models.Model):
    class Meta:
        db_table = 'paper_module'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 试卷名称
    paper_id = models.CharField(max_length=50, help_text='试卷ID')
    # 模块名称
    title = models.CharField(max_length=100, help_text='模块名称')
    # 模块描述
    description = models.TextField(blank=True, null=True, help_text='模块描述')
    # 试题顺序
    sequence_number = models.PositiveIntegerField(default=1, help_text='模块顺序')
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
