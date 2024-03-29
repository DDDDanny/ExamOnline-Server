# Generated by Django 4.2.8 on 2024-02-18 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PaperManagement', '0004_alter_paper_total_marks'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='is_deleted',
            field=models.BooleanField(default=False, help_text='是否删除'),
        ),
        migrations.AlterField(
            model_name='paperquestions',
            name='marks',
            field=models.PositiveIntegerField(default=5, help_text='试题分数'),
        ),
    ]
