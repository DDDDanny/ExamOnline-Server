# -*- coding: utf-8 -*-
# @Time    : 2024/01/04 16:56:59
# @Author  : DannyDong
# @File    : views.py
# @Describe: User相关视图 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from .models import User
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


class ListUsersView(ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self, request):
        # 获取查询参数
        username_query = request.query_params.get('username', None)
        # 构建查询集
        queryset = User.objects.all()
        # 如果有用户名参数，添加过滤条件
        if username_query:
            queryset = queryset.filter(username=username_query)
        return queryset

    # 获取用户列表信息
    def list(self, request):
        # 获取过滤后的用户数据
        queryset = self.get_queryset(request)
        # 序列化用户数据
        serializer = UserSerializer(queryset, many=True)
        # 返回序列化后的数据
        data = Response(serializer.data)
        log_response(data.data)
        return api_response(ResponseCode.SUCCESS, '查询成功', data.data)


if __name__ == '__main__':
    pass
