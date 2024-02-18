# -*- coding: utf-8 -*-
# @Time    : 2024/02/07 09:58:21
# @Author  : DannyDong
# @File    : views.py
# @Describe: Paper相关视图 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Paper, PaperModule, PaperQuestions
from .serializers import PaperQuestionsSerializer
from .serializers import PaperSerializer, PaperModuleSerializer
from src.utils.response_utils import ResponseCode, api_response


class PaperBaseView(APIView):
    
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

    def delete(self, request):
        """delete 删除试卷信息（逻辑删除）
        Args:
            request (Object): 请求参数
        """
        # 获取要删除的试卷
        paper_id = request.data.get('id')
        try:
            paper_instance = Paper.objects.get(id=paper_id)
        except Paper.DoesNotExist:
            return api_response(ResponseCode.NOT_FOUND, '试卷不存在，删除失败！')
        # 在这里添加逻辑删除的代码
        paper_instance.is_deleted = True
        paper_instance.save()
        # 返回成功响应
        return api_response(ResponseCode.SUCCESS, '删除成功！')


class PaperModuleView(APIView):
    
    def post(self, request):
        """post 创建试卷-模块信息
        Args:
            request (Object): 请求参数
        """
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
        paper_questions = PaperQuestions.objects.filter(paper_id=paper_id, module=module_id)
        if len(paper_questions) > 0:
            return api_response(ResponseCode.BAD_REQUEST, '该模块存在绑定的试题，无法删除！')
        else:
            module_instance.delete()
            return api_response(ResponseCode.SUCCESS, '删除模块成功！')


class PaperQuetionsView(APIView):
    
    def post(self, request):
        """post 创建试卷-试题信息
        Args:
            request (Object): 请求参数
        """
        serializer = PaperQuestionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '创建成功', data.data)
        else:
            return api_response(ResponseCode.BAD_REQUEST, '创建失败', serializer.errors)

    def delete(self, request):
        """delete 批量删除试卷-试题信息
        Args:
            request (Object): ids试题IDs，列表类型
        """
        questions_ids = request.data.get('ids')
        # 存放即将删除的试题IDs
        to_delete_ids = []
        # 存放不存在的试题IDs
        not_exists_ids = []
        # 循环遍历试题ID，判断是否存在
        for q_id in questions_ids:
            if PaperQuestions.objects.filter(id=q_id).exists():
                to_delete_ids.append(q_id)
            else:
                not_exists_ids.append(q_id)
        if len(to_delete_ids) == 0:
            return api_response(ResponseCode.SUCCESS, '没有可以删除试题！', { 'notExistsQuestions': not_exists_ids })
        else:
            # 根据试题ID获取试题实体
            to_delete_instance = PaperQuestions.objects.filter(id__in=to_delete_ids)
            to_delete_instance.delete()
            if len(not_exists_ids) > 0:
                return api_response(ResponseCode.SUCCESS, '删除试题成功！但有不存在的试题ID', { 'notExistsQuestions': not_exists_ids })
            else:
                return api_response(ResponseCode.SUCCESS, '删除试题成功!')


if __name__ == '__main__':
    pass
