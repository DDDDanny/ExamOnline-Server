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


class ExamResultDetailBaseView(APIView):
    pass


if __name__ == '__main__':
    pass
