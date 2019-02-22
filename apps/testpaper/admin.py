from django.contrib import admin

from .models import TestPaperInfo, TestPaperTestQ, TestScores


# admin-试卷信息注册
@admin.register(TestPaperInfo)
class TestPaperInfoAdmin(admin.ModelAdmin):
    # admin中表头
    list_display = (
        'name',
        'subject',
        'tp_degree',
        'total_score',
        'passing_score',
        'create_user',
        'create_time',
        'edit_time',
    )
    # 搜索
    search_fields = ('name',)
    # 分页
    list_per_page = 20


# admin-试卷试题信息注册
@admin.register(TestPaperTestQ)
class TestPaperTestQAdmin(admin.ModelAdmin):
    # admin中表头
    list_display = ('test_paper', 'test_question')
    # 搜索
    search_fields = ('test_paper',)
    # 分页
    list_per_page = 20


# admin-学生成绩信息注册
@admin.register(TestScores)
class TestScoresAdmin(admin.ModelAdmin):
    # admin中表头
    list_display = ('user', 'test_paper', 'test_score', 'create_time')
    # 搜索
    search_fields = ('user',)
    # 分页
    list_per_page = 20
