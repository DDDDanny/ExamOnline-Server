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
    pass


if __name__ == '__main__':
    pass
