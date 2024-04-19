# -*- coding: utf-8 -*-
# @Time    : 2024/02/21 13:40:18
# @Author  : DannyDong
# @File    : serializers.py
# @Describe: Exam应用-序列化

from rest_framework import serializers

from .models import Exam
from ..PaperManagement.models import Paper


class ExamSerializer(serializers.ModelSerializer):
    paper_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = '__all__'
        # 添加额外的字段
        extra_field = ['paper_info']
        # 格式化日期时间
        extra_kwargs = {
            'created_at': { 'format': '%Y-%m-%d %H:%M:%S' },
            'updated_at': { 'format': '%Y-%m-%d %H:%M:%S' },
            'publish_date': { 'format': '%Y-%m-%d %H:%M:%S' },
            'start_time': { 'format': '%Y-%m-%d %H:%M:%S' },
            'end_time': { 'format': '%Y-%m-%d %H:%M:%S' },
        }
    
    # 获取试卷信息
    def get_paper_info(self, obj):
        paper_instance = Paper.objects.filter(id=obj.paper_id).first()
        if paper_instance:
            return {
                'id': paper_instance.id,
                'title': paper_instance.title, 
                # 可以再加需要的数据
            }
        else:
            return None


if __name__ == '__main__':
    pass
