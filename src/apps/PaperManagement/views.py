# -*- coding: utf-8 -*-
# @Time    : 2024/02/07 09:58:21
# @Author  : DannyDong
# @File    : views.py
# @Describe: Paper相关视图 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Paper
from .serializers import PaperSerializer
from src.utils.response_utils import ResponseCode, api_response


class PaperBaseView(APIView):
    pass


if __name__ == '__main__':
    pass
