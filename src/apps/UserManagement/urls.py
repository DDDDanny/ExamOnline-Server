from django.urls import path

from .views import CreateUserView

urlpatterns = [
    path('createUser/', CreateUserView.as_view(), name='create_user'),
]
