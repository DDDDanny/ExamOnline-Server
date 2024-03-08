# -*- coding: utf-8 -*-
# @Time    : 2024/03/08 16:38:10
# @Author  : DannyDong
# @File    : urls.py
# @Describe: Menu应用URL

from django.urls import path

from .views import MenuBaseView

urlpatterns = [
    path('menu', MenuBaseView.as_view(), name='MenuOpts'),
]