# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import projects.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('sobriquet', models.CharField(max_length=200, null=True, verbose_name='also known as', blank=True)),
                ('date_birth', models.DateField(null=True, verbose_name='date of birth', blank=True)),
                ('date_death', models.DateField(null=True, verbose_name='date of death', blank=True)),
                ('image', models.ImageField(upload_to=projects.models.user_directory_path, null=True, verbose_name='profile picture', blank=True)),
                ('summary', models.TextField(null=True, verbose_name='short introduction', blank=True)),
                ('source_url', models.URLField(null=True, verbose_name='Reference URL', blank=True)),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='last modified on')),
                ('modified_by', models.ForeignKey(related_name='updated_authors', verbose_name='last modified by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='original title')),
                ('pid', models.CharField(max_length=255, null=True, verbose_name='Published IDs', blank=True)),
                ('publisher', models.CharField(max_length=200, null=True, verbose_name='publisher', blank=True)),
                ('year_published', models.PositiveIntegerField(null=True, verbose_name='year of publication', blank=True)),
                ('language', models.CharField(default=b'hi', max_length=32, verbose_name='language', choices=[(b'af', b'Afrikaans'), (b'ar', b'Arabic'), (b'ast', b'Asturian'), (b'az', b'Azerbaijani'), (b'bg', b'Bulgarian'), (b'be', b'Belarusian'), (b'bn', b'Bengali'), (b'br', b'Breton'), (b'bs', b'Bosnian'), (b'ca', b'Catalan'), (b'cs', b'Czech'), (b'cy', b'Welsh'), (b'da', b'Danish'), (b'de', b'German'), (b'el', b'Greek'), (b'en', b'English'), (b'en-au', b'Australian English'), (b'en-gb', b'British English'), (b'eo', b'Esperanto'), (b'es', b'Spanish'), (b'es-ar', b'Argentinian Spanish'), (b'es-mx', b'Mexican Spanish'), (b'es-ni', b'Nicaraguan Spanish'), (b'es-ve', b'Venezuelan Spanish'), (b'et', b'Estonian'), (b'eu', b'Basque'), (b'fa', b'Persian'), (b'fi', b'Finnish'), (b'fr', b'French'), (b'fy', b'Frisian'), (b'ga', b'Irish'), (b'gl', b'Galician'), (b'he', b'Hebrew'), (b'hi', b'Hindi'), (b'hr', b'Croatian'), (b'hu', b'Hungarian'), (b'ia', b'Interlingua'), (b'id', b'Indonesian'), (b'io', b'Ido'), (b'is', b'Icelandic'), (b'it', b'Italian'), (b'ja', b'Japanese'), (b'ka', b'Georgian'), (b'kk', b'Kazakh'), (b'km', b'Khmer'), (b'kn', b'Kannada'), (b'ko', b'Korean'), (b'lb', b'Luxembourgish'), (b'lt', b'Lithuanian'), (b'lv', b'Latvian'), (b'mk', b'Macedonian'), (b'ml', b'Malayalam'), (b'mn', b'Mongolian'), (b'mr', b'Marathi'), (b'my', b'Burmese'), (b'nb', b'Norwegian Bokmal'), (b'ne', b'Nepali'), (b'nl', b'Dutch'), (b'nn', b'Norwegian Nynorsk'), (b'os', b'Ossetic'), (b'pa', b'Punjabi'), (b'pl', b'Polish'), (b'pt', b'Portuguese'), (b'pt-br', b'Brazilian Portuguese'), (b'ro', b'Romanian'), (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'sl', b'Slovenian'), (b'sq', b'Albanian'), (b'sr', b'Serbian'), (b'sr-latn', b'Serbian Latin'), (b'sv', b'Swedish'), (b'sw', b'Swahili'), (b'ta', b'Tamil'), (b'te', b'Telugu'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'tt', b'Tatar'), (b'udm', b'Udmurt'), (b'uk', b'Ukrainian'), (b'ur', b'Urdu'), (b'vi', b'Vietnamese'), (b'zh-cn', b'Simplified Chinese'), (b'zh-hans', b'Simplified Chinese'), (b'zh-hant', b'Traditional Chinese'), (b'zh-tw', b'Traditional Chinese')])),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='last modified on')),
                ('authors', models.ManyToManyField(related_name='books', verbose_name='authors name', to='projects.Author')),
                ('modified_by', models.ForeignKey(related_name='updated_books', verbose_name='last modified by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ImageSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_num', models.PositiveIntegerField(default=0, verbose_name='page number')),
                ('url', models.URLField(max_length=1000, null=True, blank=True)),
                ('note', models.CharField(max_length=140, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField()),
                ('page_num', models.PositiveIntegerField(default=0, verbose_name=b'page number')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('proofread_level', models.PositiveIntegerField(default=0)),
                ('verified', models.BooleanField(default=False)),
                ('verified_at', models.DateTimeField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('added_by', models.ForeignKey(related_name='added_pages', to=settings.AUTH_USER_MODEL)),
                ('author', models.ForeignKey(related_name='pages', to='projects.Author')),
                ('book', models.ForeignKey(related_name='pages', to='projects.Book')),
                ('updated_by', models.ForeignKey(related_name='updated_pages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.CharField(default=b'offline', max_length=32, choices=[(b'offline', b'Scanned by ourself'), (b'online', b'Online digital library')])),
                ('source_url', models.URLField(max_length=1000, null=True, blank=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('pages', models.PositiveIntegerField(default=0, verbose_name='total pages')),
                ('scanned_pages', models.PositiveIntegerField(default=0, verbose_name='number of scanned pages')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='last modified on')),
                ('note', models.TextField(null=True, verbose_name='Leave a note', blank=True)),
                ('state', models.PositiveIntegerField(default=1, verbose_name='project state', choices=[(1, b'Project Initiation'), (2, b'Adding Scanned Data'), (3, b'Adding OCR Data'), (4, b'In Proofreading Rounds'), (5, b'In Formatting Rounds'), (6, b'Project Published')])),
                ('book', models.ForeignKey(related_name='project', to='projects.Book')),
                ('contributors', models.ManyToManyField(related_name='projects', to=settings.AUTH_USER_MODEL, blank=True)),
                ('manager', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='imagesource',
            name='project',
            field=models.ForeignKey(related_name='image_source', to='projects.Project'),
        ),
    ]
