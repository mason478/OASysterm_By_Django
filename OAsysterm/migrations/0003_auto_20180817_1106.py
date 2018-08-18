# Generated by Django 2.1 on 2018-08-17 03:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('OAsysterm', '0002_auto_20180816_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processcomments',
            name='comments_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 17, 3, 6, 29, 20105, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='processes',
            name='initial_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 17, 3, 6, 29, 19338, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='processes',
            name='next_approver',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='processes',
            name='process_serial_num',
            field=models.CharField(default='20180817030629', max_length=128),
        ),
        migrations.AlterField(
            model_name='processes',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 17, 3, 6, 29, 19377, tzinfo=utc)),
        ),
    ]