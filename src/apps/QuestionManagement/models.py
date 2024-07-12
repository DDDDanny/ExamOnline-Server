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
    # 试题选项
    options = models.TextField(default='T&F', max_length=500, help_text='试题选项')
    # 试题答案
    answer = models.CharField(max_length=50, help_text='试题参考答案')
    # 试题类型
    TYPE_CHOICES = [('select', 'Select'),('judge', 'Judge')]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='select', help_text='试题类型')
    # 试库类型
    TRIAL_TYPE_CHOICES = [('public', 'Public'),('private', 'Private')]
    trial_type = models.CharField(max_length=10, choices=TRIAL_TYPE_CHOICES, default='private', help_text='所属题库类型')
    # 试题状态
    status = models.BooleanField(default=True, help_text='试题状态')
    # 试题是否被删除
    is_deleted = models.BooleanField(default=False, help_text='是否删除')
    # 创建人
    created_user = models.CharField(max_length=255, help_text='创建人')
    # 创建时间
    created_at = models.DateTimeField(default=timezone.now, help_text='创建时间')
    # 更新人
    updated_user = models.CharField(max_length=255, null=True, help_text='更新人')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, null=True, help_text='更新时间')


class QuestionsFavorite(models.Model):
    class Meta:
        db_table = 'questions_favorite'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 试题ID
    question_id = models.CharField(max_length=50, help_text='试题ID')
    # 收藏者ID
    collector = models.CharField(max_length=50, help_text='收藏者ID')
    # 创建时间
    created_at = models.DateTimeField(default=timezone.now, help_text='创建时间')


class ErrorArchive(models.Model):
    class Meta:
        db_table = 'error_archive'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 错误试题ID
    question_id = models.CharField(max_length=50, help_text='试题ID')
    # 错题解析
    explanation = models.TextField(max_length=500, help_text='错题解析')
    # 错题难度
    DIFFICULTY_CHOICES = (('E', 'Easy'), ('M', 'Medium'), ('H', 'Hard'))
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='M', help_text='错题难度')
    # 收藏者ID
    collector = models.CharField(max_length=50, help_text='收藏者ID')
    # 创建时间
    created_at = models.DateTimeField(default=timezone.now, help_text='创建时间')


if __name__ == '__main__':
    pass
