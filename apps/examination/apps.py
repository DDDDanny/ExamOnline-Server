from django.apps import AppConfig


class ExaminationConfig(AppConfig):
    name = 'examination'
    # 修改admin中app名称
    verbose_name = '考试信息（Exam_Info）'
