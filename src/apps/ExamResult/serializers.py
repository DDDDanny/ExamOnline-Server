# -*- coding: utf-8 -*-
# @Time    : 2024/02/23 13:09:19
# @Author  : DannyDong
# @File    : serializers.py
# @Describe: ExamResult应用-序列化

from rest_framework import serializers

from .models import ExamResult, ExamResultDetail

class ExamResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExamResult
        fields = '__all__'
        # 格式化日期时间
        extra_kwargs = {
            'created_at': { 'format': '%Y-%m-%d %H:%M:%S' },
            'updated_at': { 'format': '%Y-%m-%d %H:%M:%S' },
        }


class ExamResultDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExamResultDetail
        fields = '__all__'
        # 格式化日期时间
        extra_kwargs = {
            'created_at': { 'format': '%Y-%m-%d %H:%M:%S' },
        } 


if __name__ == '__main__':
    pass
