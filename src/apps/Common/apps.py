# -*- coding: utf-8 -*-
# @Time    : 2024/05/02 19:46:54
# @Author  : DannyDong
# @File    : apps.py
# @Describe: 公共App配置 

from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # 这个属性指定了应用程序的包路径。它告诉 Django 在应用程序启动时使用哪个配置类
    name = 'src.apps.Common'
