# -*- coding: utf-8 -*-
# @Time    : 2024/03/08 16:37:22
# @Author  : DannyDong
# @File    : serializers.py
# @Describe: Menu应用-序列化

from rest_framework import serializers

from .models import Menu

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


if __name__ == '__main__':
    pass
