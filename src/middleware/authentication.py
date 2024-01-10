# -*- coding: utf-8 -*-
# @Time    : 2024/01/10 18:20:03
# @Author  : DannyDong
# @File    : authentication.py
# @Describe: 自定义JWT验证 


from src.apps.UserManagement.models import Student
from rest_framework_simplejwt.authentication import JWTAuthentication

# 自定义JWT验证（由于我们的ID是UUID，默认的只支持Number）
class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get('user_id')
        try:
            return Student.objects.get(id=user_id)
        except Exception:
            return None


if __name__ == '__main__':
    pass
