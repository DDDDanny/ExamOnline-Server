from django.apps import AppConfig


class TestpaperConfig(AppConfig):
    name = 'testpaper'
    # 修改admin中app名称
    verbose_name = '试卷信息（TP_Info）'
