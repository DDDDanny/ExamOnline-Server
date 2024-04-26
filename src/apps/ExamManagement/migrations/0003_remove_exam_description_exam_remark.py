# Generated by Django 4.2.8 on 2024-04-22 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ExamManagement', '0002_alter_exam_description_alter_exam_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='description',
        ),
        migrations.AddField(
            model_name='exam',
            name='remark',
            field=models.TextField(blank=True, help_text='备注', null=True),
        ),
    ]