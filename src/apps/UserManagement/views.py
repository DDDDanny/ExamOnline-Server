# -*- coding: utf-8 -*-
# @Time    : 2024/01/04 16:56:59
# @Author  : DannyDong
# @File    : views.py
# @Describe: User相关视图 

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer
from src.utils.logger_utils import log_request, log_response
from src.utils.response_utils import ResponseCode, api_response


class CreateUserView(APIView):
    # 创建用户信息
    def post(self, request):
        # 使用请求数据创建 UserSerializer 的实例
        serializer = UserSerializer(data=request.data)
        log_request(request.data)
        # 检查数据是否根据序列化器的规则有效
        if serializer.is_valid():
            # 保存验证过的数据以创建新的 User 实例
            serializer.save()
            # 返回成功响应，包含序列化后的数据和 HTTP 201 Created 状态
            data = Response(serializer.data)
            log_response(data.data)
            return api_response(ResponseCode.SUCCESS, '创建成功', data.data)
        else:
            # 返回错误响应，包含验证错误和 HTTP 400 Bad Request 状态
            log_response(serializer.errors)
            return api_response(ResponseCode.BAD_REQUEST, '创建失败', serializer.errors)


if __name__ == '__main__':
    pass
