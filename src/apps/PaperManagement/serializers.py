# -*- coding: utf-8 -*-
# @Time    : 2024/02/06 18:07:08
# @Author  : DannyDong
# @File    : serializers.py
# @Describe: 试卷应用-序列化

from rest_framework import serializers

from .models import Paper, PaperModule, PaperQuestions


class PaperSerializer(serializers.Serializer):
    class Meta:
        model = Paper
        # 指定在序列号中包含的字段
        fields = '__all__'
        # 添加额外的字段
        # extra_field = ['created_user_info', 'updated_user_info']
        # 格式化日期时间
        extra_kwargs = {
            'created_at': { 'format': '%Y-%m-%d %H:%M:%S' },
            'updated_at': { 'format': '%Y-%m-%d %H:%M:%S' },
        }


class PaperModuleSerializer(serializers.Serializer):
    class Meta:
        model = PaperModule
        # 指定在序列号中包含的字段
        fields = '__all__'
        # 添加额外的字段
        # extra_field = ['created_user_info', 'updated_user_info']
        # 格式化日期时间
        extra_kwargs = {
            'created_at': { 'format': '%Y-%m-%d %H:%M:%S' },
            'updated_at': { 'format': '%Y-%m-%d %H:%M:%S' },
        }


class PaperQuestionsSerializer(serializers.Serializer):
    class Meta:
        model = PaperQuestions
        # 指定在序列号中包含的字段
        fields = '__all__'
        # 添加额外的字段
        # extra_field = ['created_user_info', 'updated_user_info']
        # 格式化日期时间
        extra_kwargs = {
            'created_at': { 'format': '%Y-%m-%d %H:%M:%S' },
        }


if __name__ == '__main__':
    pass
