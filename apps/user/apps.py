from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'
    # 修改admin中app名称
    verbose_name = '用户信息（UserInfo）'
