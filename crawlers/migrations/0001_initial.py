# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RawArticle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_url', models.URLField(max_length=1000)),
                ('content', models.TextField()),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('valid', models.BooleanField(default=False)),
                ('snippet', models.ForeignKey(related_name='ref_articles', verbose_name=b'related entry in article table', blank=True, to='snippets.Snippet', null=True)),
            ],
        ),
    ]
