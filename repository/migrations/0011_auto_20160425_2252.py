# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0010_auto_20160203_0038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='media',
        ),
        migrations.RemoveField(
            model_name='book',
            name='references',
        ),
        migrations.RemoveField(
            model_name='poetry',
            name='contributor',
        ),
        migrations.RemoveField(
            model_name='poetry',
            name='media',
        ),
        migrations.RemoveField(
            model_name='poetry',
            name='references',
        ),
        migrations.RemoveField(
            model_name='snippet',
            name='references',
        ),
    ]
