# -*- coding: utf-8 -*-
# @Time    : 2023/12/29 15:45:21
# @Author  : DannyDong
# @File    : response_utils.py
# @Describe: 请求响应状态码及结构 

from enum import Enum
from django.http import JsonResponse

class ResponseCode(Enum):
    SUCCESS = 200  # 操作成功
    CREATED = 201  # 资源创建成功
    ACCEPTED = 202  # 请求已被接受，但尚未处理
    NO_CONTENT = 204  # 请求成功，但没有响应体内容
    BAD_REQUEST = 400  # 请求错误，可能由于缺少必需的参数或参数格式不正确
    UNAUTHORIZED = 401  # 未授权，需要提供有效的身份验证凭证
    FORBIDDEN = 403  # 禁止访问，权限不足
    NOT_FOUND = 404  # 请求的资源不存在
    METHOD_NOT_ALLOWED = 405  # 不允许使用该HTTP方法
    CONFLICT = 409  # 资源冲突，通常发生在创建资源时
    INTERNAL_SERVER_ERROR = 500  # 服务器内部错误
    # ··· 状态码可以自定义

def api_response(code, msg, data=None):
    if data is None:
        return JsonResponse({ 'code': code.value,'msg': msg })
    else:
        return JsonResponse({ 'code': code.value, 'msg': msg,'data': data })


if __name__ == '__main__':
    pass
