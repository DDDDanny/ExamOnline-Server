# -*- coding: utf-8 -*-
# @Time    : 2024/01/17 22:42:58
# @Author  : DannyDong
# @File    : views.py
# @Describe: Question相关视图

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Questions
from .serializers import QuestionSerializer
from src.utils.response_utils import ResponseCode, api_response


class QuestionBaseView(APIView):
    
    # 创建试题信息
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '创建成功', data.data)
        else:
            return api_response(ResponseCode.BAD_REQUEST, '创建失败', serializer.errors)      
    
    # 修改试题信息
    def put(self, request, **kwargs):
        try:
            # 获取需要编辑的试题实例
            question_instance = Questions.objects.get(id=kwargs['id'])
        except Questions.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '编辑失败!试题不存在，无法进行修改！')
        serializer = QuestionSerializer(question_instance, request.data)
        # 检查数据是否根据序列化器的规则有效
        if serializer.is_valid():
            # 保存验证过的数据以更新现有的 Question 实例
            serializer.save()
            # 返回成功响应，包含序列化后的数据和 HTTP 200 OK 状态
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '编辑成功', data.data)
        else:
            # 返回错误响应，包含验证错误和 HTTP 400 Bad Request 状态
            return api_response(ResponseCode.BAD_REQUEST, '编辑失败! 存在校验失败的字段！', serializer.error_messages)
    
    # 删除试题信息
    def delete(self, _, **kwargs):
        try:
            # 获取需要编辑的试题实例
            question_instance = Questions.objects.get(id=kwargs['id'])
        except Questions.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '删除失败!试题不存在，无法进行删除！') 
        question_instance.is_deleted = True
        question_instance.save()
        # 返回成功响应和 HTTP 200 OK 状态
        return api_response(ResponseCode.SUCCESS, '删除成功')

    # 获取试题信息
    def get(self, request, **kwargs):
        try:
            # 获取指定试题实例
            question_instance = Questions.objects.get(id=kwargs['id'])
        except Questions.DoesNotExist:
            # 试题不存在，返回错误响应和 HTTP 404 Not Found 状态
            return api_response(ResponseCode.NOT_FOUND, '试题不存在！')
        # 序列化试题详情数据
        serializer = QuestionSerializer(question_instance)
        # 返回序列化后的试题详情数据
        data = Response(serializer.data)
        return api_response(ResponseCode.SUCCESS, '查询试题详情成功', data.data)


if __name__ == '__main__':
    pass
