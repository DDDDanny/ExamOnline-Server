# -*- coding: utf-8 -*-
# @Time    : 2024/01/17 22:42:58
# @Author  : DannyDong
# @File    : views.py
# @Describe: Question相关视图

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Questions
from .serializers import QuestionSerializer
from src.utils.response_utils import ResponseCode, api_response


class QuestionBaseView(APIView):
    
    # 创建试题信息
    def post(self, request):
        pass
    
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
