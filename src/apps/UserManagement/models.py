# -*- coding: utf-8 -*-
# @Time    : 2024/01/03 16:35:01
# @Author  : DannyDong
# @File    : models.py
# @Describe: User应用的模型 

import uuid
from django.db import models
from django.utils import timezone


# 用户模型（抽象模型）
class User(models.Model):
    class Meta:
        abstract = True
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 用户名
    username = models.CharField(max_length=30, unique=True, help_text='用户名')
    # 密码
    password = models.CharField(max_length=30, help_text='用户密码')
    # 用户姓名
    name = models.CharField(max_length=30, help_text='用户姓名')
    # 角色
    ROLE_CHOICES = [('student', 'Student'),('teacher', 'Teacher'),('admin', 'Admin'),]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student', help_text='角色名')
    # 性别
    GENDER_CHOICES = [('male', 'Male'),('female', 'Female')]
    gender = models.CharField(max_length=10,  choices=GENDER_CHOICES, default='male', help_text='性别')
    # 是否活跃
    is_active = models.BooleanField(default=True, help_text='是否激活')
    # 是否删除
    is_deleted = models.BooleanField(default=False, help_text='是否删除')
    # 电话
    phone = models.CharField(max_length=20, null=True, blank=True, help_text='电话号码')
    # Email
    email = models.CharField(max_length=255, null=True, blank=True, help_text='邮箱账号')
    # 创建时间
    created_at = models.DateTimeField(default=timezone.now, help_text='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, help_text='更新时间')


# 学生用户模型（实例模型）
class Student(User):
    class Meta:
        db_table = 'student'
    
    # 学号
    student_id = models.CharField(max_length=30, unique=True, help_text='学号')
    # 年级
    grade = models.CharField(max_length=30, null=True, blank=True, help_text='年级')
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'student_id', 'username', 'name', 'gender', 
        'role', 'is_active', 'is_deleted'
    ]

    def __str__(self):
        return 'Student: ' + self.username
    
    # 根据你的身份验证逻辑返回相应的布尔值
    @property
    def is_authenticated(self):
        return True


# 教师用户模型（实例模型）
class Teacher(User):
    class Meta:
        db_table = 'teacher'
    
    # 教师编号
    teacher_id = models.CharField(max_length=30, unique=True, help_text='教师编号')
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'teacher_id', 'username', 'name', 'gender', 
        'role', 'is_active', 'is_deleted'
    ]
     
    def __str__(self):
        return 'Teacher: ' + self.username
    
    # 根据你的身份验证逻辑返回相应的布尔值
    @property
    def is_authenticated(self):
        return True


if __name__ == '__main__':
    pass
