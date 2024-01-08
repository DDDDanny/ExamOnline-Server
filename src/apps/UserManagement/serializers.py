# -*- coding: utf-8 -*-
# @Time    : 2024/01/04 10:26:19
# @Author  : DannyDong
# @File    : serializers.py
# @Describe: 用户应用-序列化 

from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 指定在序列化器中包含的字段
        fields = [
            'username', 'password', 'role', 'phone', 
            'email', 'is_active', 'created_at', 'updated_at', 'is_deleted'
        ]
        # 将 'password' 字段设置为只写，以在响应中隐藏它
        extra_kwargs = {
            'password': { 'write_only': True },
            'created_at': { 'format': '%Y-%m-%d %H:%M:%S' },
            'updated_at': { 'format': '%Y-%m-%d %H:%M:%S' },
        }


if __name__ == '__main__':
    pass
