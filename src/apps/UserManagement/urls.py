# -*- coding: utf-8 -*-
# @Time    : 2024/01/04 16:54:25
# @Author  : DannyDong
# @File    : urls.py
# @Describe: Users应用URL

from django.urls import path

from .views import CreateUserView, ListUsersView

urlpatterns = [
    path('createUser', CreateUserView.as_view(), name='create_user'),
    path('listUsers', ListUsersView.as_view(), name='list_users'),
]


if __name__ == '__main__':
    pass
