# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestLog',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('ip', models.IPAddressField()),
                ('user_agent', models.TextField()),
                ('http_method', models.CharField(max_length=10)),
                ('body_length', models.IntegerField()),
                ('url', models.TextField()),
                ('status_code', models.IntegerField(null=True)),
                ('exception_name', models.TextField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(max_length=1, choices=[('', 'Choose the priority'), ('L', 'Low'), ('N', 'Normal'), ('H', 'High')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(related_name='user_profile', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
