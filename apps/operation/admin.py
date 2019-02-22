from django.contrib import admin

from .models import ExamComments, UserMessage, UserFavorite


# admin-考试评论注册
@admin.register(ExamComments)
class ExamCommentsAdmin(admin.ModelAdmin):
    # admin中表头
    list_display = ('user', 'exam', 'comments', 'add_time')
    # 搜索
    search_fields = ('user',)
    # 分页
    list_per_page = 20


# admin-用户消息注册
@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    # admin中表头
    list_display = ('user', 'message', 'has_read', 'add_time')
    # 搜索
    search_fields = ('user',)
    # 分页
    list_per_page = 20


# admin-用户收藏注册
@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    # admin中表头
    list_display = ('user', 'fav_id', 'add_time')
    # 搜索
    search_fields = ('user',)
    # 分页
    list_per_page = 20
