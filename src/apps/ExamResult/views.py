# -*- coding: utf-8 -*-
# @Time    : 2024/02/24 20:05:21
# @Author  : DannyDong
# @File    : views.py
# @Describe: ExamResult应用视图层

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import ExamResult, ExamResultDetail
from .serializers import ExamResultSerializer
from .serializers import ExamResultDetailSerializer
from src.utils.response_utils import ResponseCode, api_response


class ExamResultBaseView(APIView):
    
    def post(self, request):
        """post 创建考试结果信息
        Args:
            request (Object): 请求参数
        """
        serializer = ExamResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '创建成功', data.data)
        else:
            return api_response(ResponseCode.BAD_REQUEST, '创建失败', serializer.errors)

    def delete(self, _, **kwargs):
        """delete 删除考试结果信息（物理删除）
        Args:
            _ (-): 缺省参数
            id (Object): 考试ID
        """
        try:
            exam_instance = ExamResult.objects.get(id=kwargs['id'])
        except ExamResult.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '考试结果不存在，删除失败！')
        if exam_instance.start_time is not None:
            return api_response(ResponseCode.BAD_REQUEST, '该学生已经参加考试，无法删除！')
        else:
            exam_instance.delete()
            # 返回成功响应
            return api_response(ResponseCode.SUCCESS, '删除成功！')

    def put(self, request, **kwargs):
        """put 编辑考试结果信息
        Args:
            id (str): 考试结果ID
            request (Object): 请求参数
        """
        try:
            # 获取需要编辑的考试结果实例
            exam_result_instance = ExamResult.objects.get(id=kwargs['id'])
        except ExamResult.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '编辑失败！考试结果不存在，无法进行编辑！')
        serializer = ExamResultSerializer(exam_result_instance, request.data)
        # 检查更新后的数据是否符合规则校验
        if serializer.is_valid():
            # 保存验证过的数据以更新现有的 ExamResult 实例
            serializer.save()
            # 返回成功响应，包含序列化后的数据和 HTTP 200 OK 状态
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '编辑成功', data.data)
        else:
            # 返回错误响应，包含验证错误和 HTTP 400 Bad Request 状态
            return api_response(ResponseCode.BAD_REQUEST, '编辑失败！存在校验失败的字段', serializer.error_messages)

    def get(self, request, **kwargs):
        """get 查询考试结果列表信息（根据考试结果ID获取考试结果详情）
        Args:
            request (Object): 请求参数
            kwargs[id] (str): 考试结果ID
        """
        if len(kwargs.items()) != 0:
            try:
                # 获取指定考试结果实例
                exam_result_instance = ExamResult.objects.get(id=kwargs['id'])
            except ExamResult.DoesNotExist:
                # 考试结果不存在，返回错误响应和 HTTP 404 Not Found 状态
                return api_response(ResponseCode.NOT_FOUND, '考试结果不存在！')
            # 序列化试题详情数据
            serializer = ExamResultSerializer(exam_result_instance)
            # 返回序列化后的试题详情数据
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '查询考试结果详情成功', data.data)
        else:
            # 定义查询参数和它们对应的模型字段
            query_params_mapping = {
                'exam_id': 'exam_id',
                'student_id': 'student_id',
                # 添加其他查询参数和字段的映射
            }
            # 构建查询条件的字典
            filters = {}
            for param, field in query_params_mapping.items():
                value = request.query_params.get(param, None)
                if value is not None:
                    filters[field] = value
            # 执行查询
            queryset = ExamResult.objects.filter(**filters)
            # 序列化试题数据
            serializer = ExamResultSerializer(queryset, many=True)
            # 返回序列化后的数据
            data = Response(serializer.data)
            resp = { 'total': len(data.data), 'data': data.data }
            return api_response(ResponseCode.SUCCESS, '查询成功', resp)


class ExamResultDetailBaseView(APIView):
    
    def post(self, request):
        """post 创建考试结果详情信息
        Args:
            request (Object): 请求参数
        """
        serializer = ExamResultDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '创建成功', data.data)
        else:
            return api_response(ResponseCode.BAD_REQUEST, '创建失败', serializer.errors)


if __name__ == '__main__':
    pass
