import json

from src.utils.logger_utils import log_request, log_response
from rest_framework.decorators import action
from src.utils.response_utils import ResponseCode, api_response


@action(detail=False, methods=['GET'])
def index(request):
    log_request(json.dumps({ 'userName': '007', 'password': '123456' }))
    data = api_response(ResponseCode.SUCCESS, '获取成功', data={ 'userName': '007', 'password': '123456' })
    log_response(data.content.decode('unicode_escape'))
    return data