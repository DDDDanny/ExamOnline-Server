# -*- coding: utf-8 -*-
# @Time    : 2024/02/07 09:57:26
# @Author  : DannyDong
# @File    : urls.py
# @Describe: Paper应用URL

from django.urls import path

from .views import PaperBaseView
from .views import PaperModuleView, PaperModuleSortView
from .views import PaperQuetionsView, PaperQuestionsSortView
from .views import PaperCopyView, PaperPublishView, PaperForSelectorView
from .views import PaperModuleQuestionView

urlpatterns = [
    path('paper', PaperBaseView.as_view(), name='PaperOpts'),
    path('paper/<str:id>', PaperBaseView.as_view(), name='PaperOpts'),
    path('paperModule', PaperModuleView.as_view(), name='PaperModuleOpts'),
    path('paperModule/<str:id>', PaperModuleView.as_view(), name='PaperModuleOpts'),
    path('paperQuestion', PaperQuetionsView.as_view(), name='PaperQuestionOpts'),
    path('paperQuestion/<str:id>', PaperQuetionsView.as_view(), name='PaperQuestionOpts'),
    path('paperCopy', PaperCopyView.as_view(), name='PaperCopyOpts'),
    path('paperPublish', PaperPublishView.as_view(), name='PaperPublishOpts'),
    path('paperModuleSort', PaperModuleSortView.as_view(), name='PaperModuleSortOpts'),
    path('paperQuestionsSort', PaperQuestionsSortView.as_view(), name='PaperQuestionsSortOpts'),
    path('paperForSelector', PaperForSelectorView.as_view(), name='PaperForSelectorOpts'),
    path('paperView/<str:id>', PaperModuleQuestionView.as_view(), name='PaperViewOpts'),
]
