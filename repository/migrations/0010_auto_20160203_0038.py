# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0009_auto_20160117_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='same_as',
            field=models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity.                               For example, the URL of the item's Wikipedia page or official website or the URL from where the crawler has collected the data.", max_length=2000, null=True, verbose_name='Similar Item', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='same_as',
            field=models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity.                               For example, the URL of the item's Wikipedia page or official website or the URL from where the crawler has collected the data.", max_length=2000, null=True, verbose_name='Similar Item', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='same_as',
            field=models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity.                               For example, the URL of the item's Wikipedia page or official website or the URL from where the crawler has collected the data.", max_length=2000, null=True, verbose_name='Similar Item', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='type',
            field=models.CharField(default=b'corp', help_text='Type of the organization.', max_length=8, choices=[(b'corp', b'Corporation'), (b'edu', b'Educational Organization'), (b'govt', b'Government Organization'), (b'locl', b'Local Business'), (b'ngo', b'NGO'), (b'perf', b'Performing Group'), (b'sport', b'Sports Organization')]),
        ),
        migrations.AlterField(
            model_name='person',
            name='same_as',
            field=models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity.                               For example, the URL of the item's Wikipedia page or official website or the URL from where the crawler has collected the data.", max_length=2000, null=True, verbose_name='Similar Item', blank=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='same_as',
            field=models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity.                               For example, the URL of the item's Wikipedia page or official website or the URL from where the crawler has collected the data.", max_length=2000, null=True, verbose_name='Similar Item', blank=True),
        ),
        migrations.AlterField(
            model_name='poetry',
            name='same_as',
            field=models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity.                               For example, the URL of the item's Wikipedia page or official website or the URL from where the crawler has collected the data.", max_length=2000, null=True, verbose_name='Similar Item', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='same_as',
            field=models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity.                               For example, the URL of the item's Wikipedia page or official website or the URL from where the crawler has collected the data.", max_length=2000, null=True, verbose_name='Similar Item', blank=True),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='same_as',
            field=models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity.                               For example, the URL of the item's Wikipedia page or official website or the URL from where the crawler has collected the data.", max_length=2000, null=True, verbose_name='Similar Item', blank=True),
        ),
    ]
