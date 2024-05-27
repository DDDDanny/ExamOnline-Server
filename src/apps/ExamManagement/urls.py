# -*- coding: utf-8 -*-
# @Time    : 2024/02/21 13:39:21
# @Author  : DannyDong
# @File    : urls.py
# @Describe: Exam应用URL

from django.urls import path

from .views import ExamBaseView, ExamPublishView, ExamScheduleView


urlpatterns = [
     path('exam', ExamBaseView.as_view(), name='ExamOpts'),
     path('exam/<str:id>', ExamBaseView.as_view(), name='ExamOpts'),
     path('examPublish/<str:id>', ExamPublishView.as_view(), name='ExamPublishOpts'),
     path('examSchedule', ExamScheduleView.as_view(), name='ExamOpts'),
]
