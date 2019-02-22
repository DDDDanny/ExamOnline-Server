from django.contrib import admin

from .models import ExaminationInfo, ExamPaperInfo, ExamStudentsInfo


# admin-考试信息注册
@admin.register(ExaminationInfo)
class ExaminationInfoAdmin(admin.ModelAdmin):
    # admin中表头
    list_display = (
        'name',
        'subject',
        'start_time',
        'end_time',
        'student_num',
        'actual_num',
        'exam_state',
        'exam_type',
        'create_user',
        'create_time',
    )
    # 搜索
    search_fields = ('name',)
    # 分页
    list_per_page = 20


# admin-考试试卷信息注册
@admin.register(ExamPaperInfo)
class ExamPaperInfoAdmin(admin.ModelAdmin):
    # admin中表头
    list_display = (
        'exam',
        'paper',
    )
    # 搜索
    search_fields = ('exam',)
    # 分页
    list_per_page = 20


# admin-考试人员信息注册
@admin.register(ExamStudentsInfo)
class ExamStudentsInfoAdmin(admin.ModelAdmin):
    # admin中表头
    list_display = (
        'exam',
        'student',
    )
    # 搜索
    search_fields = ('exam',)
    # 分页
    list_per_page = 20
