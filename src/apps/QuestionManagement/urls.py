# -*- coding: utf-8 -*-
# @Time    : 2024/01/20 22:05:25
# @Author  : DannyDong
# @File    : urls.py
# @Describe: Question应用URL 

from django.urls import path

from .views import QuestionBaseView
from .views import QuestionFavoriteView


urlpatterns = [
    path('question', QuestionBaseView.as_view(), name='QuestionsOpts'),
    path('question/<str:id>', QuestionBaseView.as_view(), name='QuestionsOpts'),
    path('q_favorite', QuestionFavoriteView.as_view(), name='QuestionsFavoriteOpts'),
    path('q_favorite/<str:id>', QuestionFavoriteView.as_view(), name='QuestionsFavoriteOpts'),
]


if __name__ == '__main__':
    pass
