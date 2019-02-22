from django.apps import AppConfig


class OperationConfig(AppConfig):
    name = 'operation'
    # 修改admin中app名称
    verbose_name = '用户操作（Operation）'
