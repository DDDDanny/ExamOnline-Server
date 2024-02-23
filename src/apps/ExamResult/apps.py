# -*- coding: utf-8 -*-
# @Time    : 2024/02/23 13:13:44
# @Author  : DannyDong
# @File    : apps.py
# @Describe: ExamResult应用apps 

from django.apps import AppConfig


class ExamResultConfig(AppConfig):
    # 属性指定了应用程序的默认主键字段类型
    default_auto_field = 'django.db.models.BigAutoField'
    # 这个属性指定了应用程序的包路径。它告诉 Django 在应用程序启动时使用哪个配置类
    name = 'src.apps.ExamResult'
