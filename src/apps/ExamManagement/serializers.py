# -*- coding: utf-8 -*-
# @Time    : 2024/02/21 13:40:18
# @Author  : DannyDong
# @File    : serializers.py
# @Describe: Exam应用-序列化

from rest_framework import serializers

from .models import Exam


class ExamSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Exam
        fields = '__all__'
        # 添加额外的字段
        # extra_field = ['created_user_info', 'updated_user_info']
        # 格式化日期时间
        extra_kwargs = {
            'created_at': { 'format': '%Y-%m-%d %H:%M:%S' },
            'updated_at': { 'format': '%Y-%m-%d %H:%M:%S' },
        }


if __name__ == '__main__':
    pass
