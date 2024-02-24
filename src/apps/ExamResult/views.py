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
    pass


if __name__ == '__main__':
    pass
