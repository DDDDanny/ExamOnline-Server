# -*- coding: utf-8 -*-
# @Time    : 2024/01/10 18:20:03
# @Author  : DannyDong
# @File    : authentication.py
# @Describe: 自定义JWT验证 


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from src.apps.UserManagement.models import Student, Teacher

# 自定义获取&刷新Token
class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        # 在这里添加额外的信息到 token 中，比如 user_type
        token['user_type'] = user.role
        return token


# 自定义JWT验证（由于我们的ID是UUID，默认的只支持Number）
class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token.get('user_id')
        user_type = validated_token.get('user_type')
        try:
            if user_type == 'student':
                return Student.objects.get(id=user_id)
            else:
                return Teacher.objects.get(id=user_id)
        except Exception:
            return None


if __name__ == '__main__':
    pass
