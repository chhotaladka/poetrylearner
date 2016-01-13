# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0007_auto_20160112_0113'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='name',
            field=models.CharField(default=None, help_text='The name/title of the item.', max_length=300),
            preserve_default=False,
        ),
    ]
