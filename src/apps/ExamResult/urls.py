# -*- coding: utf-8 -*-
# @Time    : 2024/02/23 13:09:25
# @Author  : DannyDong
# @File    : urls.py
# @Describe: ExamResult应用URL

from django.urls import path

from .views import ExamResultBaseView

urlpatterns = [
    path('examResult', ExamResultBaseView.as_view(), name='ExamResultOpts')
]
