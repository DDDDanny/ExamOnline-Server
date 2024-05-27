# -*- coding: utf-8 -*-
# @Time    : 2024/02/21 13:43:55
# @Author  : DannyDong
# @File    : views.py
# @Describe: Exam应用视图层

from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import Exam
from ..ExamResult.models import ExamResult
from .serializers import ExamSerializer
from src.utils.response_utils import ResponseCode, api_response


class ExamBaseView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """post 创建考试信息
        Args:
            request (Object): 请求参数
        """
        serializer = ExamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '创建成功', data.data)
        else:
            return api_response(ResponseCode.BAD_REQUEST, '创建失败', serializer.errors)

    def delete(self, _, **kwargs):
        """delete 删除考试信息（逻辑删除）
        Args:
            _ (-): 缺省参数
            id (Object): 考试ID
        """
        try:
            exam_instance = Exam.objects.get(id=kwargs['id'])
        except Exam.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '考试不存在，删除失败！')
        # 在这里添加逻辑删除的代码
        exam_instance.is_deleted = True
        exam_instance.save()
        # 返回成功响应
        return api_response(ResponseCode.SUCCESS, '删除成功！')

    def put(self, request, **kwargs):
        """put 编辑考试信息
        Args:
            id (str): 考试ID
            request (Object): 请求参数
        """
        try:
            # 获取需要编辑的试卷实例
            exam_instance = Exam.objects.get(id=kwargs['id'])
            # 删除不需要的参数
            del request.data['updated_at'], request.data['created_at'], request.data['id']
            del request.data['start_datetime'], request.data['end_datetime']
            del request.data['exam_date'], request.data['exam_status']
        except Exam.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '编辑失败！考试不存在，无法进行编辑！')
        serializer = ExamSerializer(exam_instance, request.data)
        # 检查更新后的数据是否符合规则校验
        if serializer.is_valid():
            # 保存验证过的数据以更新现有的 Paper 实例
            serializer.save()
            # 返回成功响应，包含序列化后的数据和 HTTP 200 OK 状态
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '编辑成功', data.data)
        else:
            # 返回错误响应，包含验证错误和 HTTP 400 Bad Request 状态
            return api_response(ResponseCode.BAD_REQUEST, '编辑失败！存在校验失败的字段', serializer.error_messages)

    def get(self, request):
        """get 查询考试信息列表信息
        Args:
            request (Object): 请求参数
        """
        # 定义查询参数和它们对应的模型字段
        query_params_mapping = {
            'title': 'title__icontains',  # 模糊查询
            'is_published': 'is_published',
            'is_deleted': 'is_deleted',
            'created_user': 'created_user',
            # 添加其他查询参数和字段的映射
        }
        # 构建查询条件的字典
        filters = {}
        for param, field in query_params_mapping.items():
            value = request.query_params.get(param, None)
            if value is not None and value != '':
                if field == 'is_published' or field == 'is_deleted':
                    filters[field] = True if value.lower() == 'true' else False
                else:
                    filters[field] = value
        current_time = request.query_params.get('current_time', None)
        if current_time is not None and current_time != '':
            # 执行查询（用于查询考试成绩）
            queryset = Exam.objects.filter(**filters).filter(end_time__lt=current_time).order_by('-created_at')
        else:
            # 执行查询
            queryset = Exam.objects.filter(**filters).order_by('-created_at')
        # 实例化分页器并配置参数
        paginator = PageNumberPagination()
        paginator.page_size = int(request.query_params.get('pageSize', 50))
        paginator.page_query_param = 'currentPage'
        # 进行分页处理
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        # 序列化考试数据
        serializer = ExamSerializer(paginated_queryset, many=True)
        resp = { 'total': len(queryset), 'data': serializer.data }
        return api_response(ResponseCode.SUCCESS, '查询成功', resp)


class ExamPublishView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]
    
    def post(self, _, **kwargs):
        """post 发布考试
        Args:
            id: 考试ID
        """
        try:
            exam_instance = Exam.objects.get(id=kwargs['id'])
        except Exception:
            return api_response(ResponseCode.BAD_REQUEST, '发布失败！考试不存在，请刷新后重新操作！')
        # 获取关联的考生信息
        associated_students = ExamResult.objects.filter(exam_id=kwargs['id'])
        if len(associated_students) == 0:
            return api_response(ResponseCode.BAD_REQUEST, '发布失败！未关联考生，请关联后重新操作！')
        # 更新字段
        exam_instance.is_published = True
        exam_instance.publish_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        exam_instance.save()
        return api_response(ResponseCode.SUCCESS, '取消发布成功')
    
    def delete(self, _, **kwargs):
        """delete 取消发布
        Args:
            id: 考试ID
        """
        try:
            exam_instance = Exam.objects.get(id=kwargs['id'])
        except Exception:
            return api_response(ResponseCode.BAD_REQUEST, '取消发布失败！考试不存在，请刷新后重新操作！')
        # 更新字段
        exam_instance.is_published = False
        exam_instance.publish_date = None
        exam_instance.save()
        return api_response(ResponseCode.SUCCESS, '取消发布成功')


class ExamScheduleView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """get 查询考试计划信息
        Args:
            request (Object): 请求参数
        """
        # 定义查询参数和它们对应的模型字段
        query_params_mapping = {
            'start_time': 'start_time__contains',  # 模糊查询
            'is_published': 'is_published',
            'is_deleted': 'is_deleted'
            # 添加其他查询参数和字段的映射
        }
        # 构建查询条件的字典
        filters = {}
        for param, field in query_params_mapping.items():
            value = request.query_params.get(param, None)
            if value is not None and value != '':
                if field == 'is_published' or field == 'is_deleted':
                    filters[field] = True if value.lower() == 'true' else False
                else:
                    filters[field] = value
        # 执行查询
        queryset = Exam.objects.filter(**filters).order_by('start_time')
        # 序列化考试数据
        serializer = ExamSerializer(queryset, many=True)
        resp = { 'total': len(queryset), 'data': serializer.data }
        return api_response(ResponseCode.SUCCESS, '查询成功', resp)


if __name__ == '__main__':
    pass
