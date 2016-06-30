# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0012_auto_20160425_2256'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='date_birth',
        ),
        migrations.RemoveField(
            model_name='person',
            name='date_death',
        ),
        migrations.AddField(
            model_name='person',
            name='year_birth',
            field=models.SmallIntegerField(help_text='For years like 500 BC, use -500.', null=True, verbose_name='year of birth', blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='year_death',
            field=models.SmallIntegerField(help_text='For years like 500 BC, use -500.', null=True, verbose_name='year of death', blank=True),
        ),
    ]
