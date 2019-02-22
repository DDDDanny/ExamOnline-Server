from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


# 用户基本信息
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=100, default='', verbose_name='登录名')
    gender = models.CharField(
        choices=(('male', '男'), ('female', '女')), default='female', max_length=6, verbose_name='性别'
    )
    mobile = models.CharField(max_length=11, default='', null=True, blank=True, verbose_name='电话号码')
    user_type = models.CharField(
        choices=(('student', '学生'), ('teacher', '老师')), default='student', max_length=7, verbose_name='用户类型'
    )
    age = models.IntegerField(default=18, verbose_name='年龄')
    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png', max_length=200, verbose_name='头像')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


# 验证码相关
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=100, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(
        choices=(
            ('active', '激活'), ('forget', '找回密码'), ('update_email', '修改邮箱'), ('special_exam', '特殊考试')
        ),
        max_length=50,
        verbose_name='发生方式',
    )
    send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


# 科目信息
class SubjectInfo(models.Model):
    subject_name = models.CharField(max_length=20, default='', verbose_name='科目名称')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta:
        verbose_name = '科目信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject_name


# 学生信息
class StudentsInfo(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=20, default='', verbose_name='学生姓名')
    student_id = models.CharField(max_length=20, default='', verbose_name='学号')
    student_class = models.CharField(max_length=10, default='', verbose_name='学生班级')
    student_school = models.CharField(max_length=100, default='', verbose_name='学生所在学校')

    class Meta:
        verbose_name = '学生信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.student_name


# 老师信息
class TeacherInfo(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    teacher_name = models.CharField(max_length=20, default='', verbose_name='老师姓名')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    subject = models.ForeignKey(SubjectInfo, on_delete=models.CASCADE, verbose_name='所属科目')
    teacher_school = models.CharField(max_length=100, default='', verbose_name='老师所在学校')

    class Meta:
        verbose_name = '老师信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.teacher_name
