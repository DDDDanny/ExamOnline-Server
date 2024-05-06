# -*- coding: utf-8 -*-
# @Time    : 2024/01/05 14:36:40
# @Author  : DannyDong
# @File    : request_response_logger.py
# @Describe: 用于拦截请求，打印请求&返回数据


from src.utils.response_utils import ResponseCode, api_response
from src.utils.logger_utils import log_request, log_response, log_common

class RequestInterceptorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 处理请求前的逻辑
        self.log_request_body(request)

        # 如果请求路径中包含 'upload'，则直接调用下一个中间件或视图函数
        if 'upload' in request.path:
            return self.get_response(request)

        response = self.get_response(request)
        
        # 处理响应后的逻辑
        if response.status_code == 200:
            if 'download' not in request.path:
                self.log_response_body(response)
        else:
            if response.status_code in [401, 403]:
                return api_response(ResponseCode.UNAUTHORIZED, '无权限或Token失效！请重新登录！')
            else:
                return api_response(ResponseCode.INTERNAL_SERVER_ERROR, '系统错误', response.reason_phrase)
        return response

    # 打印请求体日志信息
    def log_request_body(self, request):
        log_common(f'【{request.method}】 {request.path}')
        if request.method == 'GET':
            log_request(request.GET)
        elif request.body and not request.FILES:  # 检查请求体是否非空且不是文件上传
            try:
                # 尝试解码UTF-8编码的请求体
                log_request(request.body.decode('utf-8'))
            except UnicodeDecodeError:
                # 如果解码失败，说明请求体是二进制数据，直接打印字节串
                log_request(request.body)
        else:
            log_request('文件上传请求')

    # 打印响应体日志信息
    def log_response_body(self, response):
        log_response(response.content.decode('utf-8'))


if __name__ == '__main__':
    pass
