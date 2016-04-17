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
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(help_text='Feedback URL.', max_length=2000)),
                ('text', models.TextField(help_text='Feedback text.', blank=True)),
                ('action', models.TextField(help_text='Action taken on the feedback.', max_length=1000, null=True, blank=True)),
                ('email', models.EmailField(help_text="Email field, if user isn't logged in and wants to send her email.", max_length=254, null=True, blank=True)),
                ('date_added', models.DateTimeField(help_text='The date time on which the item was created or the item was added to a DataFeed.', auto_now_add=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('added_by', models.ForeignKey(related_name='feedback_feedback_added', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('content_type', models.ForeignKey(related_name='feedback_content_objects', blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
    ]
