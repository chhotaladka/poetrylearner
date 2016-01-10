# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0004_auto_20160111_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateField(help_text='The end date <YYYY-MM-DD> of the event.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(help_text='The start date <YYYY-MM-DD> of the event.', null=True, blank=True),
        ),
    ]
