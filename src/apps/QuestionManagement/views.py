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
    def put(self, request):
        pass
    
    # 获取试题信息
    def get(self, request, *args, **kwargs):
        pass
    
    # 删除试题信息
    def delete(self, request):
        pass 


if __name__ == '__main__':
    pass
