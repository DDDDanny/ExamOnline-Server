# -*- coding: utf-8 -*-
# @Time    : 2024/01/17 22:42:58
# @Author  : DannyDong
# @File    : views.py
# @Describe: Question相关视图

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import Questions, QuestionsFavorite, ErrorArchive
from .serializers import QuestionSerializer, QuestionFavoriteSerializer
from .serializers import ErrorArchiveSerializer
from src.utils.response_utils import ResponseCode, api_response


class QuestionBaseView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """post 创建试题信息
        Args:
            request (Object): 请求参数
        """
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '创建成功', data.data)
        else:
            return api_response(ResponseCode.BAD_REQUEST, '创建失败', serializer.errors)

    def put(self, request, **kwargs):
        """put 修改试题信息
        Args:
            request (Object): 请求参数
        """
        try:
            # 获取需要编辑的试题实例
            question_instance = Questions.objects.get(id=kwargs['id'])
            # 删除不需要的参数
            del request.data['updated_at'], request.data['created_at'], request.data['id']
        except Questions.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '编辑失败!试题不存在，无法进行修改！')
        serializer = QuestionSerializer(question_instance, request.data)
        # 检查数据是否根据序列化器的规则有效
        if serializer.is_valid():
            # 保存验证过的数据以更新现有的 Question 实例
            serializer.save()
            # 返回成功响应，包含序列化后的数据和 HTTP 200 OK 状态
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '编辑成功', data.data)
        else:
            # 返回错误响应，包含验证错误和 HTTP 400 Bad Request 状态
            return api_response(ResponseCode.BAD_REQUEST, '编辑失败! 存在校验失败的字段！', serializer.error_messages)

    def delete(self, _, **kwargs):
        """delete 删除试题信息
        Args:
            _ (any): 缺省参数
        """
        try:
            # 获取需要编辑的试题实例
            question_instance = Questions.objects.get(id=kwargs['id'])
        except Questions.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '删除失败!试题不存在，无法进行删除！')
        question_instance.is_deleted = True
        question_instance.save()
        # 返回成功响应和 HTTP 200 OK 状态
        return api_response(ResponseCode.SUCCESS, '删除成功')

    def get(self, request, **kwargs):
        """get 获取试题信息
        Args:
            request (Object): 请求参数
        """
        if len(kwargs.items()) != 0:
            try:
                # 获取指定试题实例
                question_instance = Questions.objects.get(id=kwargs['id'])
            except Questions.DoesNotExist:
                # 试题不存在，返回错误响应和 HTTP 404 Not Found 状态
                return api_response(ResponseCode.NOT_FOUND, '试题不存在！')
            # 序列化试题详情数据
            serializer = QuestionSerializer(question_instance)
            # 返回序列化后的试题详情数据
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '查询试题详情成功', data.data)
        else:
            # 定义查询参数和它们对应的模型字段
            query_params_mapping = {
                'topic': 'topic__icontains',
                'type': 'type',
                'is_deleted': 'is_deleted',
                'status': 'status',
                'trial_type': 'trial_type',
                'created_user': 'created_user'
                # 添加其他查询参数和字段的映射
            }
            # 构建查询条件的字典
            filters = {}
            for param, field in query_params_mapping.items():
                value = request.query_params.get(param, None)
                if value is not None and value != '':
                    if field == 'status' or field == 'is_deleted':
                        filters[field] = True if value.lower() == 'true' else False
                    else:
                        filters[field] = value
            # 执行查询
            queryset = Questions.objects.filter(**filters).order_by('-created_at')
            # 实例化分页器并配置参数
            paginator = PageNumberPagination()
            paginator.page_size = int(request.query_params.get('pageSize', 50))
            paginator.page_query_param = 'currentPage'
            # 进行分页处理
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            # 序列化分页后的试题数据
            serializer = QuestionSerializer(paginated_queryset, many=True)
            # 若有收藏者信息，就新增「favorite」字段
            collector = request.query_params.get('collector', None)
            if collector is not None and collector != '':
                # 获取该收藏者收藏的试题ID
                questions_ids = list(QuestionsFavorite.objects.filter(collector=collector).values_list('question_id', flat=True))
                for item in serializer.data:
                    item['favorite'] = True if item['id'] in questions_ids else False
            resp = {'total': len(queryset), 'data': serializer.data}
            return api_response(ResponseCode.SUCCESS, '查询成功', resp)


class QuestionFavoriteView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]

    def __get_favorite_count(self, user_id, q_id):
        """__get_favorite_count 获取收藏信息数量
        Args:
            user_id (UUID): 收藏者ID
            q_id (UUID): 试题ID
        """
        return QuestionsFavorite.objects.filter(collector=user_id, question_id=q_id).count()

    def post(self, request):
        """post 收藏试题接口
        Args:
            request (Object): 请求参数
        """
        # 获取收藏信息数量
        favorite_count = self.__get_favorite_count(
            request.data['collector'], request.data['question_id'])
        if favorite_count > 0:
            return api_response(ResponseCode.BAD_REQUEST, '收藏失败！已有收藏记录，无需再次收藏！')
        else:
            serializer = QuestionFavoriteSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = Response(serializer.data)
                return api_response(ResponseCode.SUCCESS, '收藏成功！', data.data)
            else:
                return api_response(ResponseCode.BAD_REQUEST, '收藏失败！', serializer.errors)

    def delete(self, request):
        """delete 取消收藏试题接口
        Args:
            request (Object): 请求参数
        """
        # 获取收藏信息数量
        favorite_count = self.__get_favorite_count(
            request.data['collector'], request.data['question_id'])
        if favorite_count <= 0:
            return api_response(ResponseCode.SUCCESS, '取消收藏失败！没有收藏记录，无需取消收藏！')
        else:
            # 查询收藏记录
            favorite_entry = QuestionsFavorite.objects.filter(
                collector=request.data['collector'], question_id=request.data['question_id'])
            if favorite_entry:
                # 如果存在收藏记录，删除它
                favorite_entry.delete()
                return api_response(ResponseCode.SUCCESS, '取消收藏成功！')
            else:
                return api_response(ResponseCode.BAD_REQUEST, '取消收藏失败！没有找到相关的收藏记录！')

    def get(self, request, **kwargs):
        """get 根据收藏者ID获取收藏的试题列表
        Args:
            _ (any): 缺省参数
            id (str): 收藏者ID
        """
        # 定义查询参数和它们对应的模型字段
        query_params_mapping = {
            'topic': 'topic__icontains',
            'type': 'type',
            'status': 'status',
            'trial_type': 'trial_type',
            # 添加其他查询参数和字段的映射
        }
        # 构建查询条件的字典
        filters = {}
        for param, field in query_params_mapping.items():
            value = request.query_params.get(param, None)
            if value is not None and value != '':
                if field == 'status' or field == 'is_deleted':
                    filters[field] = True if value.lower() == 'true' else False
                else:
                    filters[field] = value
        # 首先获取符合条件的 Question 的主键列表
        question_ids = Questions.objects.filter(**filters).values_list('id', flat=True)
        # 数据转换
        question_ids_str = [str(item) for item in list(question_ids)]
        # 使用二次查询过滤 QuestionsFavorite
        queryset = QuestionsFavorite.objects.filter(collector=kwargs['id']).filter(question_id__in=question_ids_str).order_by('-created_at')
        # 实例化分页器并配置参数
        paginator = PageNumberPagination()
        paginator.page_size = int(request.query_params.get('pageSize', 50))
        paginator.page_query_param = 'currentPage'
        # 进行分页处理
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        # 序列化分页后的试题数据
        serializer = QuestionFavoriteSerializer(paginated_queryset, many=True)
        resp = {'total': len(queryset), 'data': serializer.data}
        return api_response(ResponseCode.SUCCESS, '查询成功', resp)


class ErrorArchiveView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]

    def __get_error_question_count(self, user_id, q_id):
        """__get_error_question_count 获取收藏错题数量
        Args:
            user_id (UUID): 收藏者ID
            q_id (UUID): 试题ID
        Returns:
            number: 错题数量
        """
        return ErrorArchive.objects.filter(collector=user_id, question_id=q_id).count()

    def post(self, request):
        """post 错题收藏接口
        Args:
            request (object): 请求参数
        """
        # 获取收藏错题信息数量
        archive_count = self.__get_error_question_count(
            request.data['collector'], request.data['question_id'])
        if archive_count > 0:
            return api_response(ResponseCode.SUCCESS, '加入错题集失败！已有错题记录，无需再次收藏！')
        else:
            serializer = ErrorArchiveSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = Response(serializer.data)
                return api_response(ResponseCode.SUCCESS, '收藏错题成功！', data.data)
            else:
                return api_response(ResponseCode.BAD_REQUEST, '收藏错题失败！', serializer.errors)

    def delete(self, request):
        """delete 取消收藏错题接口
        Args:
            request (Object): 请求参数
        """
        # 获取收藏错题信息数量
        archive_count = self.__get_error_question_count(
            request.data['collector'], request.data['question_id'])
        if archive_count <= 0:
            return api_response(ResponseCode.SUCCESS, '取消收藏错题失败！没有收藏记录，无需取消收藏！')
        else:
            # 查询收藏记录
            archive_entry = ErrorArchive.objects.filter(
                collector=request.data['collector'], question_id=request.data['question_id'])
            if archive_entry:
                # 如果存在收藏记录，删除它
                archive_entry.delete()
                return api_response(ResponseCode.SUCCESS, '取消收藏错题成功！')
            else:
                return api_response(ResponseCode.BAD_REQUEST, '取消收藏失败！没有找到相关的收藏记录！')

    def get(self, request, **kwargs):
        """get 根据收藏者ID获取错题集的试题列表
        Args:
            request (any): 请求参数
            id (str): 收藏者ID
        """
        # 定义查询参数和它们对应的模型字段
        query_params_mapping = {
            'topic': 'topic__icontains',
            'type': 'type',
            # 添加其他查询参数和字段的映射
        }
        # 构建查询条件的字典
        filters = {}
        for param, field in query_params_mapping.items():
            value = request.query_params.get(param, None)
            if value is not None and value != '':
                if field == 'status' or field == 'is_deleted':
                    filters[field] = True if value.lower() == 'true' else False
                else:
                    filters[field] = value
        # 首先获取符合条件的 Question 的主键列表
        question_ids = Questions.objects.filter(**filters).values_list('id', flat=True)
        # 数据转换
        question_ids_str = [str(item) for item in list(question_ids)]
        # 对试题难度进行筛选
        difficulty = request.query_params.get('difficulty', None)
        if difficulty is not None and difficulty != '':
            queryset = ErrorArchive.objects.filter(difficulty=difficulty, collector=kwargs['id']).filter(question_id__in=question_ids_str).order_by('-created_at')
        else:
            queryset = ErrorArchive.objects.filter(collector=kwargs['id']).filter(question_id__in=question_ids_str).order_by('-created_at')
        # 实例化分页器并配置参数
        paginator = PageNumberPagination()
        paginator.page_size = int(request.query_params.get('pageSize', 50))
        paginator.page_query_param = 'currentPage'
        # 进行分页处理
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        # 序列化分页后的试题数据
        serializer = ErrorArchiveSerializer(paginated_queryset, many=True)
        # 返回序列化后的数据
        data = Response(serializer.data)
        resp = {'total': len(queryset), 'data': data.data}
        return api_response(ResponseCode.SUCCESS, '查询成功', resp)

    def put(self, request, **kwargs):
        """put 修改错题集中的试题信息
        Args:
            request (Object): 请求参数
            kwargs[id] (str): 错误集试题ID（主键ID）
        """
        try:
            # 获取需要编辑的试题实例
            question_instance = ErrorArchive.objects.get(id=kwargs['id'])
        except Questions.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '编辑失败!收藏记录不存在，无法进行修改！')
        serializer = ErrorArchiveSerializer(question_instance, request.data)
        # 检查数据是否根据序列化器的规则有效
        if serializer.is_valid():
            # 保存验证过的数据以更新现有的 Question 实例
            serializer.save()
            # 返回成功响应，包含序列化后的数据和 HTTP 200 OK 状态
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '编辑成功', data.data)
        else:
            # 返回错误响应，包含验证错误和 HTTP 400 Bad Request 状态
            return api_response(ResponseCode.BAD_REQUEST, '编辑失败! 存在校验失败的字段！', serializer.error_messages)


class QuestionsWarehouseForPaper(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """get 获取试题信息（ 用于试卷题库 ）
        Args:
            request (Object): 请求参数
        Desc:
            返回个人题库中有效且未被删除的试题以及收藏的公共试题
        """
        user_id = request.query_params.get('user_id', None)
        # 获取操作者的收藏试题
        favorite_questions_instance = QuestionsFavorite.objects.filter(collector=user_id).values_list('question_id', flat=True)
        favorite_questions_ids = [str(item) for item in list(favorite_questions_instance)]
        # 获取操作者相关题库实例
        questions_instance = Questions.objects.filter(
            status=True, is_deleted=False).filter(
                Q(created_user=user_id) | Q(id__in = favorite_questions_ids)).order_by('created_at')
        serializer = QuestionSerializer(questions_instance, many=True)
        data = Response(serializer.data)
        return api_response(ResponseCode.SUCCESS, '获取题库试题成功！', data.data)


if __name__ == '__main__':
    pass
