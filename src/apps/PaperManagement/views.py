# -*- coding: utf-8 -*-
# @Time    : 2024/02/07 09:58:21
# @Author  : DannyDong
# @File    : views.py
# @Describe: Paper相关视图 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Paper
from .serializers import PaperQuestionsSerializer
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

    def delete(self, request):
        # 获取要删除的试卷
        paper_id = request.data.get('id')
        try:
            paper_instance = Paper.objects.get(id=paper_id)
        except Paper.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '试卷不存在，删除失败！')
        # 在这里添加逻辑删除的代码
        paper_instance.is_deleted = True
        paper_instance.save()
        # 返回成功响应
        return api_response(ResponseCode.SUCCESS, '删除成功！')


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


class PaperQuetionsView(APIView):
    
    def post(self, request):
        """post 创建试卷-试题信息
        Args:
            request (Object): 请求参数
        """
        serializer = PaperQuestionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '创建成功', data.data)
        else:
            return api_response(ResponseCode.BAD_REQUEST, '创建失败', serializer.errors)


if __name__ == '__main__':
    pass
