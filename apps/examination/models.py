from django.db import models
from datetime import datetime

from user.models import UserProfile, StudentsInfo, SubjectInfo
from testpaper.models import TestPaperInfo


# 考试信息
class ExaminationInfo(models.Model):
    name = models.CharField(max_length=50, default='', verbose_name='考试名称')
    subject = models.ForeignKey(SubjectInfo, on_delete=models.CASCADE, verbose_name='所属科目')
    start_time = models.DateTimeField(default=datetime.now, verbose_name='开始时间')
    end_time = models.DateTimeField(default=datetime.now, verbose_name='结束时间')
    student_num = models.IntegerField(default=0, verbose_name='应参加人数')
    actual_num = models.IntegerField(default=0, verbose_name='实际参加人数')
    exam_state = models.CharField(
        choices=(('0', '考试未开始'), ('1', '考试进行中'), ('2', '考试已结束')),
        default='0',
        max_length=1,
        verbose_name='考试状态',
    )
    exam_type = models.CharField(choices=(('pt', '普通'), ('ts', '特殊')), max_length=2, default='pt', verbose_name='类型')
    create_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='创建人')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '考试信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 考试试卷信息
class ExamPaperInfo(models.Model):
    exam = models.ForeignKey(ExaminationInfo, on_delete=models.CASCADE, verbose_name='考试信息')
    paper = models.ForeignKey(TestPaperInfo, on_delete=models.CASCADE, verbose_name='试卷信息')

    class Meta:
        verbose_name = '考试试卷信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.exam.name


# 考试人员信息
class ExamStudentsInfo(models.Model):
    exam = models.ForeignKey(ExaminationInfo, on_delete=models.CASCADE, verbose_name='考试信息')
    student = models.ForeignKey(StudentsInfo, on_delete=models.CASCADE, verbose_name='考生信息')

    class Meta:
        verbose_name = '考试考生信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.exam.name
