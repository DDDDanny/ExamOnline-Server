# -*- coding: utf-8 -*-
# @Time    : 2024/01/05 14:36:40
# @Author  : DannyDong
# @File    : request_response_logger.py
# @Describe: 用于拦截请求，打印请求&返回数据

from src.utils.logger_utils import log_request, log_response, log_common

class RequestInterceptorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 处理请求前的逻辑
        self.log_request_body(request)

        response = self.get_response(request)
        
        # 处理响应后的逻辑
        if response.status_code == 200:
            self.log_response_body(response)
        
        return response

    # 打印请求体日志信息
    def log_request_body(self, request):
        log_common(f'【{request.method}】 {request.path}')
        if request.method == 'GET':
            log_request(request.GET)
        else:
            log_request(request.body.decode('utf-8'))

    # 打印响应体日志信息
    def log_response_body(self, response):
        log_response(response.content.decode('utf-8'))


if __name__ == '__main__':
    pass
