# -*- coding: utf-8 -*-
# @Time    : 2024/01/04 16:54:25
# @Author  : DannyDong
# @File    : urls.py
# @Describe: Users应用URL

from django.urls import path

from .views import StudentUserView, TeacherUserView
from .views import StudentLoginView, TeacherLoginView

urlpatterns = [
    path('student', StudentUserView.as_view(), name='StudentOpts'),
    path('teacher', TeacherUserView.as_view(), name='TeacherOpts'),
    path('teacherLogin', TeacherLoginView.as_view(), name='teacherLogin'),
    path('studentLogin', StudentLoginView.as_view(), name='studentLogin'),
]


if __name__ == '__main__':
    pass
