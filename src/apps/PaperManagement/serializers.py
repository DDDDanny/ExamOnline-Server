# -*- coding: utf-8 -*-
# @Time    : 2024/02/06 18:07:08
# @Author  : DannyDong
# @File    : serializers.py
# @Describe: 试卷应用-序列化

from rest_framework import serializers

from src.apps.UserManagement.models import Teacher
from src.apps.QuestionManagement.models import Questions
from .models import Paper, PaperModule, PaperQuestions

# 创建一个公共的 Serializer Mixin
class UserInfoMixin:
    def get_user_info(self, user_id):
        """get_user_info 
        根据给定的用户ID查询数据库获取用户信息，并返回包含用户信息的字典。
        Args:
            user_id (str): 用户的ID
        Returns:
            如果找到用户，则返回包含用户信息的字典，否则返回None。
        """
        teacher_instance = Teacher.objects.filter(id=user_id).first()
        if teacher_instance:
            return {
                'id': teacher_instance.id,
                'name': teacher_instance.name, 
                'username': teacher_instance.username,
                # 可以再加需要的数据
            }
        else:
            return None


class PaperSerializer(serializers.ModelSerializer, UserInfoMixin):
    created_user_info = serializers.SerializerMethodField()
    updated_user_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Paper
        # 指定在序列号中包含的字段
        fields = '__all__'
        # 添加额外的字段
        extra_field = ['created_user_info', 'updated_user_info']
        # 格式化日期时间
        extra_kwargs = {
            'created_at': { 'format': '%Y-%m-%d %H:%M:%S' },
            'updated_at': { 'format': '%Y-%m-%d %H:%M:%S' },
            'publish_date': { 'format': '%Y-%m-%d %H:%M:%S' },
        }
    
    # 获取创建人信息
    def get_created_user_info(self, obj):
        return self.get_user_info(obj.created_user)
    
    # 获取更新人信息
    def get_updated_user_info(self, obj):
        return self.get_user_info(obj.updated_user)


class PaperModuleSerializer(serializers.ModelSerializer, UserInfoMixin):
    created_user_info = serializers.SerializerMethodField()
    updated_user_info = serializers.SerializerMethodField()

    class Meta:
        model = PaperModule
        # 指定在序列号中包含的字段
        fields = '__all__'
        # 添加额外的字段
        extra_field = ['created_user_info', 'updated_user_info']
        # 格式化日期时间
        extra_kwargs = {
            'created_at': { 'format': '%Y-%m-%d %H:%M:%S' },
            'updated_at': { 'format': '%Y-%m-%d %H:%M:%S' },
        }
        
    # 获取创建人信息
    def get_created_user_info(self, obj):
        return self.get_user_info(obj.created_user)
    
    # 获取更新人信息
    def get_updated_user_info(self, obj):
        return self.get_user_info(obj.updated_user)


class PaperQuestionsSerializer(serializers.ModelSerializer):
    question_detail = serializers.SerializerMethodField()

    class Meta:
        model = PaperQuestions
        # 指定在序列号中包含的字段
        fields = '__all__'
        # 添加额外的字段
        extra_field = ['question_detail']
        # 格式化日期时间
        extra_kwargs = {
            'created_at': { 'format': '%Y-%m-%d %H:%M:%S' },
        }

    def get_question_detail(self, obj):
        """get_question_detail 
        根据给定的试题ID查询数据库获取试题信息，并返回包含试题信息的字典。
        Args:
            user_id (str): 试题的ID
        Returns:
            如果找到试题，则返回包含试题信息的字典，否则返回None。
        """
        question_instance = Questions.objects.filter(id=obj.question_id).first()
        if question_instance:
            return {
                'id': question_instance.id,
                'topic': question_instance.topic, 
                'type': question_instance.type,
                'options': question_instance.options
                # 可以再加需要的数据
            }
        else:
            return None


if __name__ == '__main__':
    pass
