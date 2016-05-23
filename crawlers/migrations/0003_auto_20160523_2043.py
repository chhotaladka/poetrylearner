# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0002_rawarticle_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawarticle',
            name='source_url',
            field=models.URLField(max_length=1000, db_index=True),
        ),
        migrations.AlterField(
            model_name='rawauthor',
            name='source_url',
            field=models.URLField(max_length=1000, db_index=True),
        ),
    ]
