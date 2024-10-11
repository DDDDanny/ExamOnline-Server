# Generated by Django 4.2.8 on 2024-10-11 09:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ExamResult', '0003_alter_examresultdetail_solution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examresult',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='examresultdetail',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=255, primary_key=True, serialize=False),
        ),
    ]
