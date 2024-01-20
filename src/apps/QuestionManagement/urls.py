# -*- coding: utf-8 -*-
# @Time    : 2024/01/20 22:05:25
# @Author  : DannyDong
# @File    : urls.py
# @Describe: Question应用URL 

from django.urls import path

from .views import QuestionBaseView


urlpatterns = [
    path('question', QuestionBaseView.as_view(), name='QuestionsOpts'),
]


if __name__ == '__main__':
    pass
