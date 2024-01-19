# -*- coding: utf-8 -*-
# @Time    : 2024/01/19 16:57:04
# @Author  : DannyDong
# @File    : serializers.py
# @Describe: 试题应用-序列化

from .models import Questions
from rest_framework import serializers


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        # 指定在序列号中包含的字段
        fields = '__all__'
        # 将 'password' 字段设置为只写，以在响应中隐藏它
        extra_kwargs = {
            'password': { 'write_only': True },
            'created_at': { 'format': '%Y-%m-%d %H:%M:%S' },
            'updated_at': { 'format': '%Y-%m-%d %H:%M:%S' },
        }
        
if __name__ == '__main__':
    pass
