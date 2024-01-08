# -*- coding: utf-8 -*-
# @Time    : 2024/01/04 16:54:25
# @Author  : DannyDong
# @File    : urls.py
# @Describe: Users应用URL

from django.urls import path

from .views import CreateUserView, ListUsersView, LoginView

urlpatterns = [
    path('user', CreateUserView.as_view(), name='userOpts'),
    path('listUsers', ListUsersView.as_view(), name='listUsers'),
    path('login', LoginView.as_view(), name='login'),
]


if __name__ == '__main__':
    pass
