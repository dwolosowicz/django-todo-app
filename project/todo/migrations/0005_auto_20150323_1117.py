# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_auto_20150323_0737'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='timezone',
            field=timezone_field.fields.TimeZoneField(default=b'Europe/Warsaw'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='content',
            field=models.TextField(default=b'', verbose_name=b'Task'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name=b'Finished?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(max_length=1, verbose_name=b'Importance', choices=[(b'', b'Choose the priority'), (b'L', b'Low'), (b'N', b'Normal'), (b'H', b'High')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.ForeignKey(verbose_name=b'Author', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
