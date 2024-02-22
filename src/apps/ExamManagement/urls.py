# -*- coding: utf-8 -*-
# @Time    : 2024/02/21 13:39:21
# @Author  : DannyDong
# @File    : urls.py
# @Describe: Exam应用URL

from django.urls import path

from .views import ExamBaseView


urlpatterns = [
     path('exam', ExamBaseView.as_view(), name='ExamOpts')
]
