# -*- coding: utf-8 -*-
# @Time    : 2024/03/08 16:36:24
# @Author  : DannyDong
# @File    : views.py
# @Describe: Menu应用视图层

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Menu
from .serializers import MenuSerializer
from src.utils.response_utils import ResponseCode, api_response


class MenuBaseView(APIView):
    
    def post(self, request):
        """post 创建菜单
        Args:
            request (Object): 新增菜单必填参数
        """
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = Response(serializer.data)
            return api_response(ResponseCode.SUCCESS, '创建成功', data.data)
        else:
            return api_response(ResponseCode.BAD_REQUEST, '创建失败', serializer.errors)
    
    def get(self, request):
        """get 获取菜单信息
        Args:
            request (Object): 请求参数
        """
        is_show_value = request.query_params.get('is_show', None)
        # 执行查询
        if is_show_value is None:
            return api_response(ResponseCode.BAD_REQUEST, '获取菜单失败！角色错误！')
        elif is_show_value == 'Admin':
            queryset = Menu.objects.filter(parent_code='0').order_by('order')
        else:
            if is_show_value == 'Teacher' or is_show_value == 'Student':
                queryset = Menu.objects.filter(Q(is_show=is_show_value) | Q(
                    is_show='ALL')).filter(parent_code='0').order_by('order')
            else:
                return api_response(ResponseCode.BAD_REQUEST, '获取菜单失败！角色错误！')
        # 序列化试题数据
        serializer = MenuSerializer(queryset, many=True)
        # 获取二级菜单
        for item in serializer.data:
            child_menu_queryset = Menu.objects.filter(parent_code=item['code']).order_by('order')
            child_serializer = MenuSerializer(child_menu_queryset, many=True)
            item['child_menu'] = child_serializer.data
        # 返回序列化后的数据
        data = Response(serializer.data)
        resp = {'total': len(data.data), 'data': data.data}
        return api_response(ResponseCode.SUCCESS, '查询成功', resp)


if __name__ == '__main__':
    pass
