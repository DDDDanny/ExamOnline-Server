# -*- coding: utf-8 -*-
# @Time    : 2024/02/23 13:09:25
# @Author  : DannyDong
# @File    : urls.py
# @Describe: ExamResult应用URL

from django.urls import path

from .views import ExamResultBaseView
from .views import ExamResultDetailBaseView

urlpatterns = [
    path('examResult', ExamResultBaseView.as_view(), name='ExamResultOpts'),
    path('examResult/<str:id>', ExamResultBaseView.as_view(), name='ExamResultOpts'),
    path('examResultDetail', ExamResultDetailBaseView.as_view(), name='ExamResultDetailOpts'),
    path('examResultDetail/<str:id>', ExamResultDetailBaseView.as_view(), name='ExamResultDetailOpts'),
]
