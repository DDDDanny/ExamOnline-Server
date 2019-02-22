from django.contrib import admin
from .models import UserProfile, EmailVerifyRecord, StudentsInfo, TeacherInfo, SubjectInfo


# admin-用户信息注册
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # admin中表头
    list_display = ('username', 'nick_name', 'age', 'gender', 'mobile', 'image', 'user_type')
    # 搜索
    search_fields = ('nick_name', 'username')
    # 分页
    list_per_page = 20


# admin-邮箱验证码相关注册
@admin.register(EmailVerifyRecord)
class EmailVerifyRecordAdmin(admin.ModelAdmin):
    # admin中表头
    list_display = ('code', 'email', 'send_type', 'send_time')
    # 搜索
    search_fields = ('code', 'email')
    # 分页
    list_per_page = 20


# admin-科目信息注册
@admin.register(SubjectInfo)
class SubjectInfoAdmin(admin.ModelAdmin):
    # admin中表头
    list_display = ('subject_name', 'create_time')
    # 搜索
    search_fields = ('subject_name',)
    # 分页
    list_per_page = 20


# admin-学生信息注册
@admin.register(StudentsInfo)
class StudentsInfoAdmin(admin.ModelAdmin):
    # admin中表头
    list_display = ('student_name', 'student_id', 'student_class', 'student_school')
    # 搜索
    search_fields = ('student_name', 'student_id', 'student_class', 'student_school')
    # 分页
    list_per_page = 20


# admin-老师信息注册
@admin.register(TeacherInfo)
class TeacherInfoAdmin(admin.ModelAdmin):
    # admin中表头
    list_display = ('teacher_name', 'work_years', 'teacher_school', 'subject')
    # 搜索
    search_fields = ('teacher_name', 'teacher_school')
    # 分页
    list_per_page = 20
