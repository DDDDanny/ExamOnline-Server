# Generated by Django 4.2.8 on 2024-10-16 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ExamResult', '0006_alter_examresultdetail_mark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examresult',
            name='result_mark',
            field=models.FloatField(default=0, help_text='学生考试得分'),
        ),
    ]
