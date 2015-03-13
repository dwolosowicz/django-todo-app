# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20150313_0648'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='finished',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
