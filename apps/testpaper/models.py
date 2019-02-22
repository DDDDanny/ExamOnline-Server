from django.db import models
from datetime import datetime

from testquestion.models import TestQuestionInfo
from user.models import UserProfile, StudentsInfo, SubjectInfo


# 试卷信息
class TestPaperInfo(models.Model):
    name = models.CharField(max_length=50, default='', verbose_name='试卷名称')
    subject = models.ForeignKey(SubjectInfo, on_delete=models.CASCADE, verbose_name='试卷所属科目', default='')
    tp_degree = models.CharField(
        choices=(('jd', '简单'), ('zd', '中等'), ('kn', '困难')), max_length=2, verbose_name='试卷难度', default='jd'
    )
    total_score = models.IntegerField(default=100, verbose_name='总分')
    passing_score = models.IntegerField(default=60, verbose_name='及格分')
    create_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='创建人')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    edit_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        verbose_name = '试卷信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 试卷试题
class TestPaperTestQ(models.Model):
    test_paper = models.ForeignKey(TestPaperInfo, on_delete=models.CASCADE, verbose_name='试卷')
    test_question = models.ForeignKey(TestQuestionInfo, on_delete=models.CASCADE, verbose_name='试题')

    class Meta:
        verbose_name = '试卷试题信息'
        verbose_name_plural = verbose_name


# 学生成绩信息
class TestScores(models.Model):
    user = models.ForeignKey(StudentsInfo, on_delete=models.Model, verbose_name='学生信息')
    test_paper = models.ForeignKey(TestPaperInfo, on_delete=models.CASCADE, verbose_name='试卷信息')
    test_score = models.IntegerField(default=0, verbose_name='考试成绩')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '学生成绩信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.student_name
