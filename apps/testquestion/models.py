from django.db import models
from datetime import datetime

from user.models import UserProfile, SubjectInfo


# 试题信息
class TestQuestionInfo(models.Model):
    name = models.CharField(max_length=500, default='', verbose_name='试题题目')
    subject = models.ForeignKey(SubjectInfo, on_delete=models.CASCADE, verbose_name='所属科目', default='')
    score = models.IntegerField(default=0, verbose_name='分值')
    tq_type = models.CharField(
        choices=(('xz', '选择'), ('pd', '判断'), ('tk', '填空')), max_length=2, verbose_name='试题类型', default='xz'
    )
    tq_degree = models.CharField(
        choices=(('jd', '简单'), ('zd', '中等'), ('kn', '困难')), max_length=2, verbose_name='试题难度', default='jd'
    )
    image = models.ImageField(upload_to='test_question/%Y/%m', max_length=200, verbose_name='试题图片')
    is_del = models.BooleanField(default=False, verbose_name='是否删除')
    is_share = models.BooleanField(default=False, verbose_name='是否分享')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    creat_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='创建人')
    edit_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '试题信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 试题选项表
class OptionInfo(models.Model):
    test_question = models.ForeignKey(TestQuestionInfo, on_delete=models.CASCADE, verbose_name='试题信息')
    option = models.CharField(max_length=100, default='', verbose_name='选项')
    is_right = models.BooleanField(default=True, verbose_name='是否为正确答案')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '试题选项信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.test_question.name
