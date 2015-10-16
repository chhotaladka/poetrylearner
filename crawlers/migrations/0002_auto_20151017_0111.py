# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_url', models.URLField(max_length=1000)),
                ('name', models.CharField(max_length=200)),
                ('birth', models.CharField(max_length=100, null=True, blank=True)),
                ('death', models.CharField(max_length=100, null=True, blank=True)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('valid', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-added_at'],
            },
        ),
        migrations.AlterModelOptions(
            name='rawarticle',
            options={'ordering': ['-added_at']},
        ),
    ]
