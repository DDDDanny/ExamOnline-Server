# Generated by Django 4.2.8 on 2024-10-18 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ExamResult', '0007_alter_examresult_result_mark'),
    ]

    operations = [
        migrations.AddField(
            model_name='examresult',
            name='ending_status',
            field=models.BooleanField(default=True, help_text='是否是正常结束考试'),
        ),
    ]
