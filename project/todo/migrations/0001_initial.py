# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('content', models.TextField(default='')),
                ('priority', models.CharField(default='N', choices=[('', 'Choose the priority'), ('L', 'Low'), ('N', 'Normal'), ('H', 'High')], max_length=5)),
                ('created', django_extensions.db.fields.CreationDateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('added_tasks_count', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
