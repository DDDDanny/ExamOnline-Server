# -*- coding: utf-8 -*-
# @Time    : 2024/01/03 16:34:34
# @Author  : DannyDong
# @File    : apps.py
# @Describe: User应用apps

from django.apps import AppConfig


class UserConfig(AppConfig):
    # 属性指定了应用程序的默认主键字段类型
    default_auto_field = 'django.db.models.BigAutoField'
    # 这个属性指定了应用程序的包路径。它告诉 Django 在应用程序启动时使用哪个配置类
    name = 'src.apps.UserManagement'


if __name__ == '__main__':
    pass
