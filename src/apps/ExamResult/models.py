# -*- coding: utf-8 -*-
# @Time    : 2024/02/23 13:14:56
# @Author  : DannyDong
# @File    : models.py
# @Describe: ExamResult应用模型 

import uuid

from django.db import models
from django.utils import timezone


class ExamResult(models.Model):
    class Meta:
        db_table = 'exam_result'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 考试ID
    exam_id = models.CharField(max_length=255, help_text='考试ID')
    # 学生ID
    student_id = models.CharField(max_length=255, help_text='学生ID')
    # 总得分
    result_mark = models.PositiveIntegerField(default=0, help_text='学生考试得分')
    # 学生开始考试的时间
    start_time = models.DateTimeField(blank=True, null=True, verbose_name='学生开始考试的时间')
    # 学生结束考试的时间
    end_time = models.DateTimeField(blank=True, null=True, verbose_name='学生结束考试的时间')
    # 创建时间
    created_at = models.DateTimeField(default=timezone.now, help_text='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, null=True, help_text='更新时间')


class ExamResultDetail(models.Model):
    class Meta:
        db_table = 'exam_result_detail'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 考试结果ID
    exam_result_id = models.CharField(max_length=255, help_text='考试结果ID')
    # 试题ID
    question_id = models.CharField(max_length=255, help_text='试题ID')
    # 试题得分
    mark = models.PositiveIntegerField(default=0, help_text='试题得分')
    # 学生作答结果
    solution = models.TextField(max_length=500, default=None, help_text='学生作答结果')
    # 创建时间
    created_at = models.DateTimeField(default=timezone.now, help_text='创建时间')


if __name__ == '__main__':
    pass
