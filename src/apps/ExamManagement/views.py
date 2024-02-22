# -*- coding: utf-8 -*-
# @Time    : 2024/02/21 13:43:55
# @Author  : DannyDong
# @File    : views.py
# @Describe: Exam应用视图层

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Exam
from .serializers import ExamSerializer
from src.utils.response_utils import ResponseCode, api_response


class ExamBaseView(APIView):
    
    def post(self, request):
        """post 创建考试信息
        Args:
            request (Object): 请求参数
        """
        serializer = ExamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '创建成功', data.data)
        else:
            return api_response(ResponseCode.BAD_REQUEST, '创建失败', serializer.errors)

    def delete(self, _, **kwargs):
        """delete 删除考试信息（逻辑删除）
        Args:
            _ (-): 缺省参数
            id (Object): 考试ID
        """
        try:
            exam_instance = Exam.objects.get(id=kwargs['id'])
        except Exam.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '开始不存在，删除失败！')
        # 在这里添加逻辑删除的代码
        exam_instance.is_deleted = True
        exam_instance.save()
        # 返回成功响应
        return api_response(ResponseCode.SUCCESS, '删除成功！')


if __name__ == '__main__':
    pass
