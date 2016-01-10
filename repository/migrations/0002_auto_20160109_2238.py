# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='media',
            field=models.FileField(help_text='A media for this creative work.', null=True, upload_to=b'repository/uploads/%Y/%m/', blank=True),
        ),
        migrations.AlterField(
            model_name='poetry',
            name='media',
            field=models.FileField(help_text='A media for this creative work.', null=True, upload_to=b'repository/uploads/%Y/%m/', blank=True),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='media',
            field=models.FileField(help_text='A media for this creative work.', null=True, upload_to=b'repository/uploads/%Y/%m/', blank=True),
        ),
    ]
