# -*- coding: utf-8 -*-
# @Time    : 2024/01/04 16:56:59
# @Author  : DannyDong
# @File    : views.py
# @Describe: User相关视图 


from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from .models import User
from .serializers import UserSerializer
from src.utils.response_utils import ResponseCode, api_response


class CreateUserView(APIView):
    # 创建用户信息
    def post(self, request):
        # 使用请求数据创建 UserSerializer 的实例
        serializer = UserSerializer(data=request.data)
        # 检查数据是否根据序列化器的规则有效
        if serializer.is_valid():
            # 保存验证过的数据以创建新的 User 实例
            serializer.save()
            # 返回成功响应，包含序列化后的数据和 HTTP 201 Created 状态
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '创建成功', data.data)
        else:
            # 返回错误响应，包含验证错误和 HTTP 400 Bad Request 状态
            return api_response(ResponseCode.BAD_REQUEST, '创建失败', serializer.errors)
        
    # 编辑用户信息
    def put(self, request):
        # 获取要编辑的用户实例
        user_instance = User.objects.filter(id=request.data['id']).first()
        if user_instance is None:
             # 返回错误响应，包含验证错误和 HTTP 400 Bad Request 状态
            return api_response(ResponseCode.BAD_REQUEST, '编辑失败!用户不存在，无法进行修改！')
        # 使用请求数据和用户实例创建 UserSerializer 的实例，传入实例表示执行更新操作
        serializer = UserSerializer(user_instance, data=request.data)
        # 检查数据是否根据序列化器的规则有效
        if serializer.is_valid():
            # 保存验证过的数据以更新现有的 User 实例
            serializer.save()
            # 返回成功响应，包含序列化后的数据和 HTTP 200 OK 状态
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '编辑成功', data.data)
        else:
            # 返回错误响应，包含验证错误和 HTTP 400 Bad Request 状态
            return api_response(ResponseCode.BAD_REQUEST, '编辑失败', serializer.error_messages)


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
        return api_response(ResponseCode.SUCCESS, '查询成功', data.data)


class LoginView(APIView):
    # 用户登录
    def post(self, request):
        user = authenticate(request, username=request.data['username'], password=request.data['password'])
        if user is not None:
            return api_response(ResponseCode.SUCCESS, '登录成功')
        else:
            return api_response(ResponseCode.BAD_REQUEST, '登录失败！账号或密码错误！', request.data)


if __name__ == '__main__':
    pass
