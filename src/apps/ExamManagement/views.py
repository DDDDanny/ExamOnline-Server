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


if __name__ == '__main__':
    pass
