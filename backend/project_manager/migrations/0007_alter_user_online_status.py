# Generated by Django 3.2.6 on 2021-09-06 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0006_auto_20210905_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='online_status',
            field=models.BooleanField(default=False),
        ),
    ]
