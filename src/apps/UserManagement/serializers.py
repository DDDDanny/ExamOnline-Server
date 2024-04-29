# -*- coding: utf-8 -*-
# @Time    : 2024/01/04 10:26:19
# @Author  : DannyDong
# @File    : serializers.py
# @Describe: 用户应用-序列化 

from .models import Student, Teacher
from rest_framework import serializers


# 用户基础序列化（抽象类）
class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        # 指定在序列化器中包含的字段
        fields = [
            'id', 'username', 'password', 'name', 'role', 'phone', 'gender',
            'email', 'is_active', 'created_at', 'updated_at', 'is_deleted'
        ]
        # 将 'password' 字段设置为只写，以在响应中隐藏它
        extra_kwargs = {
            'password': { 'write_only': True },
            'created_at': { 'format': '%Y-%m-%d %H:%M:%S' },
            'updated_at': { 'format': '%Y-%m-%d %H:%M:%S' },
        }


# 学生序列化
class StudentSerializer(UserBaseSerializer):
    class Meta(UserBaseSerializer.Meta):
        model = Student
        fields = UserBaseSerializer.Meta.fields + ['student_id', 'grade']


# 教师序列化
class TeacherSerializer(UserBaseSerializer):
    class Meta(UserBaseSerializer.Meta):
        model = Teacher
        fields = UserBaseSerializer.Meta.fields + ['teacher_id']


if __name__ == '__main__':
    pass
