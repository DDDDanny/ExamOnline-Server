# -*- coding: utf-8 -*-
# @Time    : 2024/02/05 19:32:17
# @Author  : DannyDong
# @File    : apps.py
# @Describe: Paper应用 


from django.apps import AppConfig


class PaperConfig(AppConfig):
    # 属性指定了应用程序的默认主键字段类型
    default_auto_field = 'django.db.models.BigAutoField'
    # 这个属性指定了应用程序的包路径。它告诉 Django 在应用程序启动时使用哪个配置类
    name = 'src.apps.PaperManagement'


if __name__ == '__main__':
    pass
