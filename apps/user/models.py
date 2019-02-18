from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png', max_length=200, verbose_name='头像')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
