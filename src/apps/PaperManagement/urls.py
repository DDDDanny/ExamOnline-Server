# -*- coding: utf-8 -*-
# @Time    : 2024/02/07 09:57:26
# @Author  : DannyDong
# @File    : urls.py
# @Describe: Paper应用URL

from django.urls import path

from .views import PaperBaseView

urlpatterns = [
    path('paper', PaperBaseView.as_view(), name='PaperOpts')
]
