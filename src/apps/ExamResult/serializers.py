# -*- coding: utf-8 -*-
# @Time    : 2024/02/23 13:09:19
# @Author  : DannyDong
# @File    : serializers.py
# @Describe: ExamResult应用-序列化

from rest_framework import serializers

from .models import ExamResult, ExamResultDetail
from ..UserManagement.models import Student


class ExamResultSerializer(serializers.ModelSerializer):
    student_info = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamResult
        fields = '__all__'
        # 添加额外的字段
        extra_field = ['student_info']
        # 格式化日期时间
        extra_kwargs = {
            'created_at': { 'format': '%Y-%m-%d %H:%M:%S' },
            'updated_at': { 'format': '%Y-%m-%d %H:%M:%S' },
            'start_time': { 'format': '%Y-%m-%d %H:%M:%S' },
            'end_time': { 'format': '%Y-%m-%d %H:%M:%S' },
        }

    # 获取学生信息
    def get_student_info(self, obj):
        student_instance = Student.objects.filter(id=obj.student_id).first()
        if student_instance:
            return {
                'id': student_instance.id,
                'name': student_instance.name, 
                'student_id': student_instance.student_id
                # 可以再加需要的数据
            }
        else:
            return None


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
