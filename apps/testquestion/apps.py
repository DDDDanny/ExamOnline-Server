from django.apps import AppConfig


class TestquestionConfig(AppConfig):
    name = 'testquestion'
    # 修改admin中app名称
    verbose_name = '试题信息（TQ_Info）'
