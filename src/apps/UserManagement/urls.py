# -*- coding: utf-8 -*-
# @Time    : 2024/01/04 16:54:25
# @Author  : DannyDong
# @File    : urls.py
# @Describe: Users应用URL

from django.urls import path

from .views import StudentUserView, TeacherUserView
from .views import StudentLoginView, TeacherLoginView
from .views import StudentBatchActivation

urlpatterns = [
    path('student', StudentUserView.as_view(), name='StudentOpts'),
    path('student/<str:user_id>', StudentUserView.as_view(), name='StudentDetail'),
    path('teacher', TeacherUserView.as_view(), name='TeacherOpts'),
    path('teacher/<str:user_id>', TeacherUserView.as_view(), name='TeacherDetail'),
    path('teacherLogin', TeacherLoginView.as_view(), name='TeacherLogin'),
    path('studentLogin', StudentLoginView.as_view(), name='StudentLogin'),
    path('studentBatchActivation', StudentBatchActivation.as_view(), name='StudentBatchActivation')
]


if __name__ == '__main__':
    pass
