# -*- coding: utf-8 -*-
# @Time    : 2024/02/24 20:05:21
# @Author  : DannyDong
# @File    : views.py
# @Describe: ExamResult应用视图层

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import ExamResult, ExamResultDetail
from .serializers import ExamResultSerializer
from .serializers import ExamResultDetailSerializer
from src.utils.response_utils import ResponseCode, api_response


class ExamResultBaseView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """post 批量创建考试结果信息
        Args:
            request (Object): { "exam_id": 考试ID, "student_ids": 学生IDs }
        """
        student_ids = request.data['student_ids']
        exam_result_list = []
        if len(student_ids) == 0:
            return api_response(ResponseCode.SUCCESS, '考试关联的学生为空！')
        else:
            for s_id in student_ids:
                exam_result_list.append({
                    'exam_id': request.data['exam_id'],
                    'student_id': s_id
                })
            serializer = ExamResultSerializer(data=exam_result_list, many=True)
            if serializer.is_valid():
                # 如果新数据校验通过，对老数据进行删除操作
                old_data = ExamResult.objects.filter(exam_id=request.data['exam_id'])
                old_data_length = len(old_data)
                deleted_count, _ = old_data.delete()
                if deleted_count != old_data_length:
                    return api_response(ResponseCode.BAD_REQUEST, '创建失败！数据处理失败！', serializer.errors)
                # 老数据删除后，新数据存储
                serializer.save()
                data = Response(serializer.data)
                return api_response(ResponseCode.SUCCESS, '创建成功', data.data)
            else:
                return api_response(ResponseCode.BAD_REQUEST, '创建失败', serializer.errors)

    def delete(self, _, **kwargs):
        """delete 删除考试结果信息（物理删除）
        Args:
            _ (-): 缺省参数
            id (Object): 考试ID
        """
        try:
            exam_instance = ExamResult.objects.get(id=kwargs['id'])
        except ExamResult.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '考试结果不存在，删除失败！')
        if exam_instance.start_time is not None:
            return api_response(ResponseCode.BAD_REQUEST, '该学生已经参加考试，无法删除！')
        else:
            exam_instance.delete()
            # 返回成功响应
            return api_response(ResponseCode.SUCCESS, '删除成功！')

    def put(self, request, **kwargs):
        """put 编辑考试结果信息
        Args:
            id (str): 考试结果ID
            request (Object): 请求参数
        """
        try:
            # 获取需要编辑的考试结果实例
            exam_result_instance = ExamResult.objects.get(id=kwargs['id'])
        except ExamResult.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '编辑失败！考试结果不存在，无法进行编辑！')
        serializer = ExamResultSerializer(exam_result_instance, request.data)
        # 检查更新后的数据是否符合规则校验
        if serializer.is_valid():
            # 保存验证过的数据以更新现有的 ExamResult 实例
            serializer.save()
            # 返回成功响应，包含序列化后的数据和 HTTP 200 OK 状态
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '编辑成功', data.data)
        else:
            # 返回错误响应，包含验证错误和 HTTP 400 Bad Request 状态
            return api_response(ResponseCode.BAD_REQUEST, '编辑失败！存在校验失败的字段', serializer.error_messages)

    def get(self, request, **kwargs):
        """get 查询考试结果列表信息（根据考试结果ID获取考试结果详情）
        Args:
            request (Object): 请求参数
            kwargs[id] (str): 考试结果ID
        """
        if len(kwargs.items()) != 0:
            try:
                # 获取指定考试结果实例
                exam_result_instance = ExamResult.objects.get(id=kwargs['id'])
            except ExamResult.DoesNotExist:
                # 考试结果不存在，返回错误响应和 HTTP 404 Not Found 状态
                return api_response(ResponseCode.NOT_FOUND, '考试结果不存在！')
            # 序列化试题详情数据
            serializer = ExamResultSerializer(exam_result_instance)
            # 返回序列化后的试题详情数据
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '查询考试结果详情成功', data.data)
        else:
            # 定义查询参数和它们对应的模型字段
            query_params_mapping = {
                'exam_id': 'exam_id',
                'result_mark': 'result_mark'
                # 添加其他查询参数和字段的映射
            }
            # 构建查询条件的字典
            filters = {}
            for param, field in query_params_mapping.items():
                value = request.query_params.get(param, None)
                if value is not None and value != '':
                    filters[field] = value
            # 执行查询
            queryset = ExamResult.objects.filter(**filters).order_by('-result_mark')
            # 序列化试题数据
            serializer = ExamResultSerializer(queryset, many=True)
            serializer_data = serializer.data
            # 获取查询参数
            filter_stu_id = request.query_params.get('student_id', None)
            filter_stu_name = request.query_params.get('name', None)
            # 二次筛选
            if filter_stu_id is not None or filter_stu_name is not None:
                filter_stu_id = filter_stu_id.strip() if filter_stu_id else None
                filter_stu_name = filter_stu_name.strip() if filter_stu_name else None

                def filter_item(item):
                    if filter_stu_id and filter_stu_id not in item['student_info']['student_id']:
                        return False
                    if filter_stu_name and filter_stu_name not in item['student_info']['name']:
                        return False
                    return True

                serializer_data = [item for item in serializer_data if filter_item(item)]
            # 返回序列化后的数据
            data = Response(serializer_data)
            resp = { 'total': len(data.data), 'data': data.data }
            return api_response(ResponseCode.SUCCESS, '查询成功', resp)


class ExamResultDetailBaseView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """post 创建考试结果详情信息
        Args:
            request (Object): 请求参数
        """
        serializer = ExamResultDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '创建成功', data.data)
        else:
            return api_response(ResponseCode.BAD_REQUEST, '创建失败', serializer.errors)

    def get(self, _, **kwargs):
        """get 根据考试结果ID获取详情信息
        Args:
            _ (——): 缺省参数
            id：试卷ID
        Returns:
            list: 模块信息列表
        """
        # 获取考试结果ID为入参的详情实例
        exam_result_detal_instance = ExamResultDetail.objects.filter(exam_result_id=kwargs['id'])
        if len(exam_result_detal_instance) == 0:
            return api_response(ResponseCode.NOT_FOUND, '没有找到该考试结果的详情信息！')
        else:
            serializer = ExamResultDetailSerializer(exam_result_detal_instance, many=True)
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '获取考试结果详情成功', data.data)


if __name__ == '__main__':
    pass
