# -*- coding: utf-8 -*-
# @Time    : 2024/01/04 16:56:59
# @Author  : DannyDong
# @File    : views.py
# @Describe: User相关视图 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Student, Teacher
from .serializers import StudentSerializer, TeacherSerializer
from src.utils.response_utils import ResponseCode, api_response


class StudentLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = Student.objects.get(username=username)
        except Exception:
            return api_response(ResponseCode.BAD_REQUEST, '登录失败！用户不存在！')
        if user.password == password:
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return api_response(ResponseCode.SUCCESS, '登录成功', data)
        else:
            return api_response(ResponseCode.UNAUTHORIZED, '登录失败！用户名或密码错误！')


class BaseUserView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]
    # 需要在子类中设置具体的序列化器
    model_serializer = None 
    # 需要在子类中设置具体的Model
    model = None
    # 创建用户信息
    def post(self, request):
        # 使用请求数据创建实例
        serializer = self.model_serializer(data=request.data)
        # 检查数据是否根据序列化器的规则有效
        if serializer.is_valid():
            # 保存验证过的数据以创建新的实例
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
        user_id = request.data.get('id')
        try:
            user_instance = self.model.objects.get(id=user_id)
        except self.model.DoesNotExist:
            # 用户不存在，返回错误响应和 HTTP 404 Not Found 状态
            return api_response(ResponseCode.NOT_FOUND, '编辑失败!用户不存在，无法进行修改！')
        # 使用请求数据和用户实例创建实例，传入实例表示执行更新操作
        serializer = self.model_serializer(user_instance, data=request.data)
        # 检查数据是否根据序列化器的规则有效
        if serializer.is_valid():
            # 保存验证过的数据以更新现有的 User 实例
            serializer.save()
            # 返回成功响应，包含序列化后的数据和 HTTP 200 OK 状态
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '编辑成功', data.data)
        else:
            # 返回错误响应，包含验证错误和 HTTP 400 Bad Request 状态
            return api_response(ResponseCode.BAD_REQUEST, '编辑失败! 存在校验失败的字段！', serializer.error_messages)

    # 删除用户信息
    def delete(self, request):
        # 获取要删除的用户实例
        user_id = request.data.get('id')
        try:
            user_instance = self.model.objects.get(id=user_id)
        except self.model.DoesNotExist:
            # 用户不存在，返回错误响应和 HTTP 404 Not Found 状态
            return api_response(ResponseCode.NOT_FOUND, '用户不存在，无法删除！')
        # 在这里添加逻辑删除的代码，例如将用户状态标记为已删除
        user_instance.is_deleted = True
        user_instance.save()
        # 返回成功响应和 HTTP 200 OK 状态
        return api_response(ResponseCode.SUCCESS, '删除成功')

    # 查询用户信息
    def get(self, request):
        # 定义查询参数和它们对应的模型字段
        query_params_mapping = {
            'username': 'username',
            'name': 'name',
            'gender': 'gender',
            'is_deleted': 'is_deleted',
            'is_active': 'is_active'
            # 添加其他查询参数和字段的映射
        }
        # 构建查询条件的字典
        filters = {}
        for param, field in query_params_mapping.items():
            value = request.query_params.get(param, None)
            if value is not None:
                filters[field] = value
        # 执行查询
        queryset = self.model.objects.filter(**filters)
        # 序列化用户数据
        serializer = self.model_serializer(queryset, many=True)
        # 返回序列化后的数据
        data = Response(serializer.data)
        return api_response(ResponseCode.SUCCESS, '查询成功', data.data)


class StudentUserView(BaseUserView):
    model_serializer = StudentSerializer
    model = Student
    

class TeacherUserView(BaseUserView):
    model_serializer = TeacherSerializer
    model = Teacher


if __name__ == '__main__':
    pass
