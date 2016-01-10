# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_auto_20160111_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateField(help_text='The end date <YYYY-MM-DD> of the event.', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(help_text='The start date <YYYY-MM-DD> of the event.', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='date_birth',
            field=models.DateField(help_text='YYYY-MM-DD', null=True, verbose_name='date of birth', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='date_death',
            field=models.DateField(help_text='YYYY-MM-DD', null=True, verbose_name='date of death', blank=True),
        ),
    ]
