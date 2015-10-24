# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='name_en',
            field=models.CharField(max_length=200, null=True, verbose_name='name in english', blank=True),
        ),
    ]
