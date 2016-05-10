# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateTimeField(help_text='The date time on which the item was created or the item was added to a DataFeed.', auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(related_name='bookmark_content_objects', to='contenttypes.ContentType')),
                ('user', models.ForeignKey(related_name='saved_bookmarks', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
