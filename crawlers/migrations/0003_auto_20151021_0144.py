# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0002_auto_20151017_0111'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawarticle',
            name='author',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='rawarticle',
            name='title',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
