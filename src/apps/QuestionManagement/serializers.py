# -*- coding: utf-8 -*-
# @Time    : 2024/01/19 16:57:04
# @Author  : DannyDong
# @File    : serializers.py
# @Describe: 试题应用-序列化

from rest_framework import serializers

from .models import Questions, QuestionsFavorite
from src.apps.UserManagement.models import Teacher


class QuestionSerializer(serializers.ModelSerializer):
    created_user_info = serializers.SerializerMethodField()
    updated_user_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Questions
        # 指定在序列号中包含的字段
        fields = '__all__'
        # 添加额外的字段
        extra_field = ['created_user_info', 'updated_user_info']
        # 将 'password' 字段设置为只写，以在响应中隐藏它
        extra_kwargs = {
            'created_at': { 'format': '%Y-%m-%d %H:%M:%S' },
            'updated_at': { 'format': '%Y-%m-%d %H:%M:%S' },
        }
    
    # 获取创建人信息
    def get_created_user_info(self, obj):
        teacher_instance = Teacher.objects.filter(id=obj.created_user).first()
        if teacher_instance:
            return {
                'id': teacher_instance.id,
                'name': teacher_instance.name, 
                'username': teacher_instance.name,
                # 可以再加需要的数据
            }
        else:
            return None
    
    # 获取更新人信息
    def get_updated_user_info(self, obj):
        teacher_instance = Teacher.objects.filter(id=obj.updated_user).first()
        if teacher_instance:
            return {
                'id': teacher_instance.id,
                'name': teacher_instance.name, 
                'username': teacher_instance.name,
                # 可以再加需要的数据
            }
        else:
            return None


class QuestionFavoriteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuestionsFavorite
        fields = '__all__'
        # 将 'password' 字段设置为只写，以在响应中隐藏它
        extra_kwargs = {
            'created_at': { 'format': '%Y-%m-%d %H:%M:%S' },
        }


if __name__ == '__main__':
    pass
