from django.contrib import admin

from .models import TestQuestionInfo, OptionInfo


# admin-试题信息注册
@admin.register(TestQuestionInfo)
class TestQuestionInfoAdmin(admin.ModelAdmin):
    # admin中表头
    list_display = (
        'name',
        'subject',
        'score',
        'tq_type',
        'tq_degree',
        'image',
        'is_del',
        'is_share',
        'create_time',
        'creat_user',
        'edit_time',
    )
    # 搜索
    search_fields = ('name', 'subject')
    # 分页
    list_per_page = 20


# admin-选项信息注册
@admin.register(OptionInfo)
class OptionInfoAdmin(admin.ModelAdmin):
    # admin中表头
    list_display = ('test_question', 'option', 'is_right', 'create_time')
    # 搜索
    search_fields = ('test_question',)
    # 分页
    list_per_page = 20
