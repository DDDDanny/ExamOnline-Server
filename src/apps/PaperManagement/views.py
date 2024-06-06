# -*- coding: utf-8 -*-
# @Time    : 2024/02/07 09:58:21
# @Author  : DannyDong
# @File    : views.py
# @Describe: Paper相关视图

from datetime import datetime

from django.db.models import Sum, Q
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from .models import Paper, PaperModule, PaperQuestions
from .serializers import PaperQuestionsSerializer
from .serializers import PaperSerializer, PaperModuleSerializer
from src.utils.response_utils import ResponseCode, api_response


class PaperBaseView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """post 创建试卷信息
        Args:
            request (Object): 请求参数
        """
        serializer = PaperSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '创建成功', data.data)
        else:
            return api_response(ResponseCode.BAD_REQUEST, '创建失败', serializer.errors)

    def delete(self, _, **kwargs):
        """delete 删除试卷信息（逻辑删除）
        Args:
            kwargs (Object): id: 试卷ID
        """
        try:
            paper_instance = Paper.objects.get(id=kwargs['id'])
        except Paper.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '试卷不存在，删除失败！')
        # 在这里添加逻辑删除的代码
        paper_instance.is_deleted = True
        paper_instance.save()
        # 返回成功响应
        return api_response(ResponseCode.SUCCESS, '删除成功！')

    def put(self, request, **kwargs):
        """put 编辑试卷信息
        Args:
            id (str): 试卷ID
            request (Object): 请求参数
        """
        try:
            # 获取需要编辑的试卷实例
            paper_instance = Paper.objects.get(id=kwargs['id'])
            # 删除不需要的参数
            del request.data['updated_at'], request.data['created_at'], request.data['id']
        except Paper.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '编辑失败！试卷不存在，无法进行编辑！')
        serializer = PaperSerializer(paper_instance, request.data)
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

    def get(self, request, **kwargs):
        """get 查询试卷列表信息（根据试卷ID获取试卷信息）
        Args:
            request (Object): 请求参数
            kwargs[id] (str): 试卷ID
        """
        if len(kwargs.items()) != 0:
            try:
                # 获取指定试卷实例
                paper_instance = Paper.objects.get(id=kwargs['id'])
            except Paper.DoesNotExist:
                # 试卷不存在，返回错误响应和 HTTP 404 Not Found 状态
                return api_response(ResponseCode.NOT_FOUND, '试卷不存在！')
            # 序列化试题详情数据
            serializer = PaperSerializer(paper_instance)
            # 返回序列化后的试题详情数据
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '查询试卷详情成功', data.data)
        else:
            # 定义查询参数和它们对应的模型字段
            query_params_mapping = {
                'title': 'title__icontains',  # 模糊查询
                'duration_minutes': 'duration_minutes',
                'is_published': 'is_published',
                'is_deleted': 'is_deleted',
                'is_public': 'is_public',
                'created_user': 'created_user',
                # 添加其他查询参数和字段的映射
            }
            # 构建查询条件的字典
            filters = {}
            for param, field in query_params_mapping.items():
                value = request.query_params.get(param, None)
                if value is not None and value != '':
                    if field == 'is_published' or field == 'is_deleted' or field == 'is_public':
                        filters[field] = True if value.lower(
                        ) == 'true' else False
                    else:
                        filters[field] = value
            # 执行查询
            queryset = Paper.objects.filter(**filters).order_by('-created_at')
            # 实例化分页器并配置参数
            paginator = PageNumberPagination()
            paginator.page_size = int(request.query_params.get('pageSize', 50))
            paginator.page_query_param = 'currentPage'
            # 进行分页处理
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            # 序列化试题数据
            serializer = PaperSerializer(paginated_queryset, many=True)
            # 计算实际总分
            for item in serializer.data:
                result = PaperQuestions.objects.filter(
                    paper_id=item['id']).aggregate(actual_total=Sum('marks'))
                item['actual_total'] = result['actual_total']
            resp = {'total': len(queryset), 'data': serializer.data}
            return api_response(ResponseCode.SUCCESS, '查询成功', resp)


class PaperModuleView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """post 创建试卷-模块信息
        Args:
            request (Object): 请求参数
        """
        # 获取该试卷的模块
        paper_id = request.data['paper_id']
        queryset = PaperModule.objects.filter(paper_id=paper_id)
        # 根据模块，配置顺序
        request.data['sequence_number'] = len(queryset) + 1
        serializer = PaperModuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '创建成功', data.data)
        else:
            return api_response(ResponseCode.BAD_REQUEST, '创建失败', serializer.errors)

    def delete(self, request):
        """delete 删除试卷-模块信息（物理删除）
        Args:
            request (Object): 模块ID和试卷ID
        """
        # 模块ID
        module_id = request.data.get('id')
        # 试卷ID
        paper_id = request.data.get('paper_id')
        try:
            module_instance = PaperModule.objects.get(id=module_id)
        except PaperModule.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '模块不存在，删除失败')
        paper_questions = PaperQuestions.objects.filter(
            paper_id=paper_id, module=module_id)
        if len(paper_questions) > 0:
            return api_response(ResponseCode.BAD_REQUEST, '该模块已关联试题，无法删除！')
        else:
            module_instance.delete()
            return api_response(ResponseCode.SUCCESS, '删除模块成功！')

    def put(self, request, **kwargs):
        """put 编辑试卷-模块信息
        Args:
            id (str): 试卷-模块表主键ID
            request (Object): 请求参数
        """
        try:
            # 获取需要编辑的试卷-模块实例
            paper_module_instance = PaperModule.objects.get(id=kwargs['id'])
            # 删除不需要的参数
            del request.data['updated_at'], request.data['created_at'], request.data['id']
        except PaperModule.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '编辑失败！模块不存在，无法进行编辑！')
        serializer = PaperModuleSerializer(paper_module_instance, request.data)
        # 检查更新后的数据是否符合规则校验
        if serializer.is_valid():
            # 保存验证过的数据以更新现有的 PaperModule 实例
            serializer.save()
            # 返回成功响应，包含序列化后的数据和 HTTP 200 OK 状态
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '编辑成功', data.data)
        else:
            # 返回错误响应，包含验证错误和 HTTP 400 Bad Request 状态
            return api_response(ResponseCode.BAD_REQUEST, '编辑失败！存在校验失败的字段', serializer.error_messages)

    def get(self, _, **kwargs):
        """get 根据试卷ID获取模块信息
        Args:
            _ (——): 缺省参数
            id：试卷ID
        Returns:
            list: 模块信息列表
        """
        try:
            Paper.objects.get(id=kwargs['id'])
        except Exception:
            return api_response(ResponseCode.BAD_REQUEST, '没有找到该试卷相关信息！')
        # 获取需要编辑的试卷-模块实例（进行排序）
        paper_module_instance = PaperModule.objects.filter(paper_id=kwargs['id']).order_by('sequence_number')
        serializer = PaperModuleSerializer(paper_module_instance, many=True)
        data = Response(serializer.data)
        return api_response(ResponseCode.SUCCESS, '获取试卷模块详情成功', data.data)


class PaperModuleSortView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """put 更新试卷-模块顺序
        Args:
            request (Object): 请求参数：modules: []
        """
        instance_suites = []
        for item in request.data['modules']:
            try:
                paper_module_instance = PaperModule.objects.get(id=item['id'])
                paper_module_instance.sequence_number = item['index']
                paper_module_instance.updated_user = item['updated_user']
                instance_suites.append(paper_module_instance)
            except Exception:
                return api_response(ResponseCode.NOT_FOUND, '调整顺序失败！模块不存在，无法进行调整！')
        # 批量更新
        PaperModule.objects.bulk_update(
            instance_suites, ['sequence_number', 'updated_user'])
        return api_response(ResponseCode.SUCCESS, '模块重新排序成功！')


class PaperQuetionsView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """post 试卷批量关联试题信息
        Args:
            request (Object): 请求参数
        """
        link_questions = request.data['questions_info']
        # 已经关联的试题
        linked_questions = PaperQuestions.objects.filter(
            paper_id=link_questions[0]['paper_id'], module=link_questions[0]['module'])
        # 进行排序
        for (index, item) in enumerate(link_questions):
            item['sequence_number'] = len(linked_questions) + index + 1
        serializers = [PaperQuestionsSerializer(
            data=item) for item in link_questions]
        # 如果有任何一个序列化器的数据无效，则收集错误，并返回部分创建失败的响应。
        errors = []
        # 如果所有序列化器的数据都有效，则返回成功的响应，并包含创建成功的数据列表。
        saved_data = []
        for serializer in serializers:
            if serializer.is_valid():
                serializer.save()
                saved_data.append(serializer.data)
            else:
                errors.append(serializer.errors)
        if errors:
            return api_response(ResponseCode.BAD_REQUEST, '部分关联失败', errors)
        else:
            return api_response(ResponseCode.SUCCESS, '批量关联成功', saved_data)

    def delete(self, _, **kwargs):
        """delete 试卷取消关联试题信息
        Args:
            id (String): 试题关联id
        """
        try:
            paper_question_instance = PaperQuestions.objects.get(
                id=kwargs['id'])
            # 获取试卷ID和模块ID
            paper_id = paper_question_instance.paper_id
            module = paper_question_instance.module
        except PaperQuestions.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '关联关系不存在，取消关联失败！')
        # 在这里添加逻辑删除的代码
        paper_question_instance.delete()
        # 重新排序
        linked_questions_instance = list(PaperQuestions.objects.filter(
            paper_id=paper_id, module=module).order_by('sequence_number'))
        # 进行排序
        for (index, item) in enumerate(linked_questions_instance):
            item.sequence_number = index + 1
            item.save()
        # 返回成功响应
        return api_response(ResponseCode.SUCCESS, '取消关联成功！')

    def put(self, request, **kwargs):
        """put 编辑试卷-试题信息
        Args:
            id (str): 试卷-试题表主键ID
            request (Object): 请求参数
        """
        try:
            # 获取需要编辑的试卷-试题实例
            paper_question_instance = PaperQuestions.objects.get(id=kwargs['id'])
        except PaperQuestions.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '编辑失败！试题绑定信息不存在，无法进行编辑！')
        serializer = PaperQuestionsSerializer(
            paper_question_instance, request.data)
        # 检查更新后的数据是否符合规则校验
        if serializer.is_valid():
            # 保存验证过的数据以更新现有的 PaperModule 实例
            serializer.save()
            # 返回成功响应，包含序列化后的数据和 HTTP 200 OK 状态
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '编辑成功', data.data)
        else:
            # 返回错误响应，包含验证错误和 HTTP 400 Bad Request 状态
            return api_response(ResponseCode.BAD_REQUEST, '编辑失败！存在校验失败的字段', serializer.error_messages)

    def get(self, _, **kwargs):
        """get 根据试卷ID获取关联信息
        Args:
            _ (——): 缺省参数
            id：试卷ID
        Returns:
            list: 试题信息列表
        """
        try:
            Paper.objects.get(id=kwargs['id'])
        except Exception:
            return api_response(ResponseCode.BAD_REQUEST, '没有找到该试卷相关信息！')
        # 获取需要编辑的试卷-试题实例（进行排序）
        paper_question_instance = PaperQuestions.objects.filter(
            paper_id=kwargs['id']).order_by('sequence_number')
        serializer = PaperQuestionsSerializer(
            paper_question_instance, many=True)
        data = Response(serializer.data)
        return api_response(ResponseCode.SUCCESS, '获取试卷关联的试题信息成功', data.data)


class PaperQuestionsSortView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """put 更新试卷-试题顺序
        Args:
            request (Object): link_questions: []
        """
        instance_suites = []
        for item in request.data['link_questions']:
            try:
                paper_question_instance = PaperQuestions.objects.get(
                    id=item['id'])
                paper_question_instance.sequence_number = item['index']
                instance_suites.append(paper_question_instance)
            except Exception:
                return api_response(ResponseCode.NOT_FOUND, '调整顺序失败！试卷不存在，无法进行调整！')
        # 批量更新
        PaperQuestions.objects.bulk_update(
            instance_suites, ['sequence_number'])
        return api_response(ResponseCode.SUCCESS, '试卷重新排序成功！')


class PaperCopyView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]

    def __remove_fields(self, fields_to_remove, instance_dict):
        """__remove_fields
        用于删除不需要的字段
        Args:
            fields_to_remove (list): 需要移除的字段
            instance_dict (dict): 操作的实体字典
        """
        for field in fields_to_remove:
            if field in instance_dict:
                del instance_dict[field]

    def post(self, request):
        """post 
            复制试卷信息（复制试卷本身信息以及试卷模块信息）
        Args:
            request (object): { id: 被复制试卷ID, created_user: 创建人 } 
        """
        try:
            # 获取需要复制的试卷实例
            paper_instance = model_to_dict(
                Paper.objects.get(id=request.data['id']))
        except Paper.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '复制失败！试卷不存在，无法进行复制！')
        # ----- 复制 Paper -----
        # 更新创建人（为复制的操作人）
        paper_instance['created_user'] = request.data['created_user']
        # 更新试卷Title
        paper_instance['title'] = '复制 - ' + paper_instance['title']
        # 删除指定字段
        fields_to_remove = ['updated_at', 'created_at',
                            'updated_user', 'id', 'is_published', 'publish_date']
        self.__remove_fields(fields_to_remove, paper_instance)
        # 序列化数据
        serializer = PaperSerializer(data=paper_instance)
        if serializer.is_valid():
            serializer.save()
            data = Response(serializer.data)
            paper_copy_id = data.data['id']
        else:
            return api_response(ResponseCode.BAD_REQUEST, '复制失败', serializer.errors)
        # ----- 复制 Paper Module -----
        paper_module_instance = PaperModule.objects.filter(paper_id=request.data['id'])
        if len(paper_module_instance) > 0:
            for instance in paper_module_instance:
                module_info = model_to_dict(instance)
                # 更新创建人（为复制的操作人）
                module_info['paper_id'] = paper_copy_id
                module_info['created_user'] = request.data['created_user']
                # 删除指定字段
                fields_to_remove = ['updated_at', 'created_at', 'updated_user', 'id']
                self.__remove_fields(fields_to_remove, module_info)
                # 序列化数据
                serializer = PaperModuleSerializer(data=module_info)
                if serializer.is_valid():
                    serializer.save()
                    data = Response(serializer.data)
                else:
                    return api_response(ResponseCode.BAD_REQUEST, '复制失败', serializer.errors)
        return api_response(ResponseCode.SUCCESS, '复制成功')


class PaperPublishView(APIView):
    # JWT校验
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """post 发布试卷
        Args:
            request (Object): 请求参数
        """
        try:
            paper = Paper.objects.get(id=request.data['id'])
        except Exception:
            return api_response(ResponseCode.BAD_REQUEST, '发布失败！试卷不存在，请重新操作！')
        # 校验：是否关联试题，若没有关联，不允许发布
        paper_question = PaperQuestions.objects.filter(paper_id=request.data['id'])
        if len(paper_question) == 0:
            return api_response(ResponseCode.BAD_REQUEST, '发布失败！试卷未关联试题，请关联试题后重新操作！')
        # 更新字段
        paper.is_published = True
        paper.publish_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        paper.save()
        return api_response(ResponseCode.SUCCESS, '试卷发布成功')

    def delete(self, request):
        """delete 取消发布
        Args:
            request (Object): 请求参数
        """
        try:
            paper = Paper.objects.get(id=request.data['id'])
        except Exception:
            return api_response(ResponseCode.BAD_REQUEST, '取消发布失败！试卷不存在，请重新操作！')
        # 更新字段
        paper.is_published = False
        paper.publish_date = None
        paper.save()
        return api_response(ResponseCode.SUCCESS, '取消发布成功')


class PaperForSelectorView(APIView):

    def get(self, request):
        """get 查询试卷列表信息（用于选择器）
        Args:
            request (Object): 请求参数
        """
        user_id = request.query_params.get('user_id', None)
        # 执行查询
        queryset = Paper.objects.filter(is_published=True).filter(
            Q(created_user=user_id) | Q(is_public=True)).order_by('-created_at')
        # 序列化试题数据
        serializer = PaperSerializer(queryset, many=True)
        # 计算实际总分
        for item in serializer.data:
            result = PaperQuestions.objects.filter(paper_id=item['id']).aggregate(actual_total=Sum('marks'))
            item['actual_total'] = result['actual_total']
        resp = {'total': len(queryset), 'data': serializer.data}
        return api_response(ResponseCode.SUCCESS, '查询成功', resp)


class PaperModuleQuestionView(APIView):

    def get(self, _, **kwargs):
        """get 根据ID查询试卷完整信息（用于查看试卷）
        Args:
            request (Object): 请求参数
        """
        try:
            Paper.objects.get(id=kwargs['id'])
        except Exception:
            return api_response(ResponseCode.BAD_REQUEST, '没有找到该试卷相关信息！')

        # 获取需要编辑的试卷-模块实例（进行排序）
        paper_module_instance = PaperModule.objects.filter(paper_id=kwargs['id']).order_by('sequence_number')
        module_serializer = PaperModuleSerializer(paper_module_instance, many=True)
        modules_data = Response(module_serializer.data)

        # 获取需要编辑的试卷-试题实例（进行排序）
        paper_question_instance = PaperQuestions.objects.filter(paper_id=kwargs['id']).order_by('sequence_number')
        questions_serializer = PaperQuestionsSerializer(paper_question_instance, many=True)
        questions_data = Response(questions_serializer.data)

        # 数据处理结果
        paper_modules_questions = []
        for module in modules_data.data:
            result_q = [
                item for item in questions_data.data if item['module'] == module['id']]
            paper_modules_questions.append({
                'id':               module['id'],
                'paper_id':         module['paper_id'],
                'title':            module['title'],
                'description':      module['description'],
                'sequence_number':  module['sequence_number'],
                'questions':        result_q
            })
        return api_response(ResponseCode.SUCCESS, '获取试卷详情成功', paper_modules_questions)


if __name__ == '__main__':
    pass
