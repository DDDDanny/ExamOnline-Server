# Generated by Django 4.2.8 on 2024-03-15 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MenuManagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='parent_code',
            field=models.CharField(default='0', help_text='菜单父节点', max_length=255),
        ),
    ]
