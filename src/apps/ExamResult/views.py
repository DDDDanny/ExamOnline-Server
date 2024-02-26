# -*- coding: utf-8 -*-
# @Time    : 2024/02/24 20:05:21
# @Author  : DannyDong
# @File    : views.py
# @Describe: ExamResult应用视图层

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import ExamResult
from .serializers import ExamResultSerializer
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


class ExamResultDetailBaseView(APIView):
    pass


if __name__ == '__main__':
    pass
