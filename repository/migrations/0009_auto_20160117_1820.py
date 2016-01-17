# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0008_reference_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='creator',
            field=models.ForeignKey(related_name='book_created', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='repository.Person', help_text='The creator/author of this content.', null=True),
        ),
        migrations.AlterField(
            model_name='poetry',
            name='creator',
            field=models.ForeignKey(related_name='poetry_created', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='repository.Person', help_text='The creator/author of this content.', null=True),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='creator',
            field=models.ForeignKey(related_name='snippet_created', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='repository.Person', help_text='The creator/author of this content.', null=True),
        ),
    ]
