# -*- coding: utf-8 -*-
# @Time    : 2024/02/07 09:58:21
# @Author  : DannyDong
# @File    : views.py
# @Describe: Paper相关视图 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Paper
from .serializers import PaperSerializer, PaperModuleSerializer
from src.utils.response_utils import ResponseCode, api_response


class PaperBaseView(APIView):
    
    def post(self, request):
        """post 创建试卷信息
        Args:
            request (Object): 请求参数
        """
        serializer = PaperSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '创建成功', data.data)
        else:
            return api_response(ResponseCode.BAD_REQUEST, '创建失败', serializer.errors)


class PaperModuleView(APIView):
    
    def post(self, request):
        """post 创建试卷-模块信息
        Args:
            request (Object): 请求参数
        """
        serializer = PaperModuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '创建成功', data.data)
        else:
            return api_response(ResponseCode.BAD_REQUEST, '创建失败', serializer.errors)


if __name__ == '__main__':
    pass
