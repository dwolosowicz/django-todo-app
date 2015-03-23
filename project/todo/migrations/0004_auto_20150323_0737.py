# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_task_finished'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='finished',
            new_name='is_completed',
        ),
    ]
