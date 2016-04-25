# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0011_auto_20160425_2252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='contributor',
        ),
        migrations.RemoveField(
            model_name='snippet',
            name='contributor',
        ),
        migrations.AddField(
            model_name='book',
            name='contributors',
            field=models.ManyToManyField(help_text='Secondary contributors to the creative work.', related_name='book_contributed', to='repository.Person', blank=True),
        ),
        migrations.AddField(
            model_name='snippet',
            name='contributors',
            field=models.ManyToManyField(help_text='Secondary contributors to the creative work.', related_name='snippet_contributed', to='repository.Person', blank=True),
        ),
    ]
