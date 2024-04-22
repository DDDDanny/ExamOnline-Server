# Generated by Django 4.2.8 on 2024-04-18 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ExamManagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='description',
            field=models.TextField(blank=True, help_text='考试描述', null=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='title',
            field=models.CharField(help_text='考试名称', max_length=100),
        ),
    ]