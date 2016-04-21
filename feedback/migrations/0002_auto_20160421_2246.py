# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='date_responded',
            field=models.DateTimeField(help_text='Date time of last response/action on the feedback.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='feedback',
            name='rating',
            field=models.IntegerField(default=0, help_text='Rating given by user as feedback OR given by us on feedback.', null=True, blank=True, choices=[(-10, -10), (-9, -9), (-8, -8), (-7, -7), (-6, -6), (-5, -5), (-4, -4), (-3, -3), (-2, -2), (-1, -1), (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]),
        ),
    ]
