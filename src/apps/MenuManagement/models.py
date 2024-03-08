# -*- coding: utf-8 -*-
# @Time    : 2024/03/08 16:35:42
# @Author  : DannyDong
# @File    : models.py
# @Describe: Menu应用模型

import uuid

from django.db import models


class Menu(models.Model):
    class Meta:
        db_table = 'menu'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 菜单Code
    code = models.CharField(max_length=255, help_text='菜单Code')
    # 菜单名称
    name = models.CharField(max_length=255, help_text='菜单名称')
    # 根据角色显示
    is_show = models.CharField(default='ALL', max_length=50, help_text='根据角色显示')
    # 菜单Path
    path = models.CharField(max_length=255, help_text='path')
    # 菜单排序
    order = models.PositiveIntegerField(default=0, help_text='菜单排序')
