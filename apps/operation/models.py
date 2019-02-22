from django.db import models
from datetime import datetime

from user.models import UserProfile
from examination.models import ExaminationInfo


# 考试评论
class ExamComments(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    exam = models.ForeignKey(ExaminationInfo, on_delete=models.CASCADE, verbose_name="课程")
    comments = models.CharField(max_length=200, verbose_name="评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "考试评论"
        verbose_name_plural = verbose_name


# 用户消息
class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name="接收用户")
    message = models.CharField(max_length=500, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name


# 用户收藏
class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    fav_id = models.IntegerField(default=0, verbose_name="数据id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name
