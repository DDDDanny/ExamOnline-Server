# Generated by Django 4.2.8 on 2024-07-12 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0003_alter_student_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='teacher_id',
            field=models.CharField(help_text='教师编号', max_length=30, unique=True),
        ),
    ]
