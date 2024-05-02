# -*- coding: utf-8 -*-
# @Time    : 2024/05/02 19:46:00
# @Author  : DannyDong
# @File    : views.py
# @Describe: 公共模块视图

import os

from django.http import FileResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from src.utils.response_utils import ResponseCode, api_response


class DownloadFileView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]
    
    def get(self, _, filename):
        file_path = os.path.join(os.getcwd(), settings.TEMPLATES_ROOT, filename).replace('\\', '/')
        if os.path.exists(file_path):
            return FileResponse(open(file_path, "rb"), as_attachment=True)
        else:
            return api_response(ResponseCode.NOT_FOUND, '没有找到文件！')


if __name__ == '__main__':
    pass
