# -*- coding: utf-8 -*-
# @Time    : 2024/01/04 16:54:25
# @Author  : DannyDong
# @File    : urls.py
# @Describe: Users应用URL

from django.urls import path

from .views import StudentBatchActivationView
from .views import StudentUserView, TeacherUserView
from .views import StudentLoginView, TeacherLoginView
from .views import StudentChangePasswordView, TeacherChangePasswordView
from .views import UploadFileForStudentView

urlpatterns = [
    path('student', StudentUserView.as_view(), name='StudentOpts'),
    path('student/<str:id>', StudentUserView.as_view(), name='StudentDetail'),
    path('teacher', TeacherUserView.as_view(), name='TeacherOpts'),
    path('teacher/<str:id>', TeacherUserView.as_view(), name='TeacherDetail'),
    path('teacherLogin', TeacherLoginView.as_view(), name='TeacherLogin'),
    path('studentLogin', StudentLoginView.as_view(), name='StudentLogin'),
    path('studentBatchActivation', StudentBatchActivationView.as_view(), name='StudentBatchActivation'),
    path('studentChangePassword/<str:user_id>', StudentChangePasswordView.as_view(), name='StudentChangePassword'),
    path('teacherChangePassword/<str:user_id>', TeacherChangePasswordView.as_view(), name='TeacherChangePassword'),
    path('uploadFileForStudent', UploadFileForStudentView.as_view(), name='UploadFileForStudent'),
]


if __name__ == '__main__':
    pass
