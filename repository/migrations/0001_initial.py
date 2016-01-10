# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import repository.models.utils
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The name/headline of the item.', max_length=300)),
                ('description', models.TextField(help_text='A short description of the item.', null=True, blank=True)),
                ('same_as', models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity. For example, the URL of the item's Wikipedia page or official website.", null=True, verbose_name='Similar Item', blank=True)),
                ('date_added', models.DateTimeField(help_text='The date time on which the item was created or the item was added to a DataFeed.', auto_now_add=True)),
                ('date_modified', models.DateTimeField(help_text="The date time on which the item was most recently modified or when the item's entry was modified within a DataFeed.", auto_now=True)),
                ('media', models.FileField(help_text='A media for this creative work.', null=True, upload_to=b'uploads/%Y/%m/%d/', blank=True)),
                ('date_published', models.DateTimeField(help_text='Date of first broadcast/publication.', auto_now=True)),
                ('license', models.CharField(help_text='A license document that applies to this content, typically indicated by URL.', max_length=300, null=True, blank=True)),
                ('language', models.CharField(default=b'en', help_text='The language of the content.', max_length=8, choices=[(b'af', b'Afrikaans'), (b'ar', b'Arabic'), (b'ast', b'Asturian'), (b'az', b'Azerbaijani'), (b'bg', b'Bulgarian'), (b'be', b'Belarusian'), (b'bn', b'Bengali'), (b'br', b'Breton'), (b'bs', b'Bosnian'), (b'ca', b'Catalan'), (b'cs', b'Czech'), (b'cy', b'Welsh'), (b'da', b'Danish'), (b'de', b'German'), (b'el', b'Greek'), (b'en', b'English'), (b'en-au', b'Australian English'), (b'en-gb', b'British English'), (b'eo', b'Esperanto'), (b'es', b'Spanish'), (b'es-ar', b'Argentinian Spanish'), (b'es-mx', b'Mexican Spanish'), (b'es-ni', b'Nicaraguan Spanish'), (b'es-ve', b'Venezuelan Spanish'), (b'et', b'Estonian'), (b'eu', b'Basque'), (b'fa', b'Persian'), (b'fi', b'Finnish'), (b'fr', b'French'), (b'fy', b'Frisian'), (b'ga', b'Irish'), (b'gl', b'Galician'), (b'he', b'Hebrew'), (b'hi', b'Hindi'), (b'hr', b'Croatian'), (b'hu', b'Hungarian'), (b'ia', b'Interlingua'), (b'id', b'Indonesian'), (b'io', b'Ido'), (b'is', b'Icelandic'), (b'it', b'Italian'), (b'ja', b'Japanese'), (b'ka', b'Georgian'), (b'kk', b'Kazakh'), (b'km', b'Khmer'), (b'kn', b'Kannada'), (b'ko', b'Korean'), (b'lb', b'Luxembourgish'), (b'lt', b'Lithuanian'), (b'lv', b'Latvian'), (b'mk', b'Macedonian'), (b'ml', b'Malayalam'), (b'mn', b'Mongolian'), (b'mr', b'Marathi'), (b'my', b'Burmese'), (b'nb', b'Norwegian Bokmal'), (b'ne', b'Nepali'), (b'nl', b'Dutch'), (b'nn', b'Norwegian Nynorsk'), (b'os', b'Ossetic'), (b'pa', b'Punjabi'), (b'pl', b'Polish'), (b'pt', b'Portuguese'), (b'pt-br', b'Brazilian Portuguese'), (b'ro', b'Romanian'), (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'sl', b'Slovenian'), (b'sq', b'Albanian'), (b'sr', b'Serbian'), (b'sr-latn', b'Serbian Latin'), (b'sv', b'Swedish'), (b'sw', b'Swahili'), (b'ta', b'Tamil'), (b'te', b'Telugu'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'tt', b'Tatar'), (b'udm', b'Udmurt'), (b'uk', b'Ukrainian'), (b'ur', b'Urdu'), (b'vi', b'Vietnamese'), (b'zh-cn', b'Simplified Chinese'), (b'zh-hans', b'Simplified Chinese'), (b'zh-hant', b'Traditional Chinese'), (b'zh-tw', b'Traditional Chinese')])),
                ('isbn', models.CharField(help_text='The ISBN of the book.', max_length=32, null=True, blank=True)),
                ('added_by', models.ForeignKey(related_name='repository_book_added', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The name/headline of the item.', max_length=300)),
                ('description', models.TextField(help_text='A short description of the item.', null=True, blank=True)),
                ('same_as', models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity. For example, the URL of the item's Wikipedia page or official website.", null=True, verbose_name='Similar Item', blank=True)),
                ('date_added', models.DateTimeField(help_text='The date time on which the item was created or the item was added to a DataFeed.', auto_now_add=True)),
                ('date_modified', models.DateTimeField(help_text="The date time on which the item was most recently modified or when the item's entry was modified within a DataFeed.", auto_now=True)),
                ('start_date', models.DateField(help_text='The start date of the event.', blank=True)),
                ('end_date', models.DateField(help_text='The end date of the event.', blank=True)),
                ('image', models.ImageField(help_text='An image of the item.', null=True, upload_to=repository.models.utils.image_upload_path, blank=True)),
                ('added_by', models.ForeignKey(related_name='repository_event_added', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The name/headline of the item.', max_length=300)),
                ('description', models.TextField(help_text='A short description of the item.', null=True, blank=True)),
                ('same_as', models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity. For example, the URL of the item's Wikipedia page or official website.", null=True, verbose_name='Similar Item', blank=True)),
                ('date_added', models.DateTimeField(help_text='The date time on which the item was created or the item was added to a DataFeed.', auto_now_add=True)),
                ('date_modified', models.DateTimeField(help_text="The date time on which the item was most recently modified or when the item's entry was modified within a DataFeed.", auto_now=True)),
                ('address', models.CharField(help_text='Physical address of the item.', max_length=300, null=True, blank=True)),
                ('type', models.CharField(default=b'corp', help_text='Type of the organization.', max_length=8, choices=[(b'air', b'Airline'), (b'corp', b'Corporation'), (b'edu', b'EducationalOrganization'), (b'govt', b'GovernmentOrganization'), (b'locl', b'LocalBusiness'), (b'ngo', b'NGO'), (b'perf', b'PerformingGroup'), (b'sport', b'SportsOrganization')])),
                ('added_by', models.ForeignKey(related_name='repository_organization_added', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='repository_organization_modified', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(related_name='subsidiaries', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='repository.Organization', help_text='The larger organization that this organization is a branch of, if any.', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The name/headline of the item.', max_length=300)),
                ('description', models.TextField(help_text='A short description of the item.', null=True, blank=True)),
                ('same_as', models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity. For example, the URL of the item's Wikipedia page or official website.", null=True, verbose_name='Similar Item', blank=True)),
                ('date_added', models.DateTimeField(help_text='The date time on which the item was created or the item was added to a DataFeed.', auto_now_add=True)),
                ('date_modified', models.DateTimeField(help_text="The date time on which the item was most recently modified or when the item's entry was modified within a DataFeed.", auto_now=True)),
                ('additional_name', models.CharField(help_text='An additional name for a Person, can be used for a middle name.', max_length=200, null=True, blank=True)),
                ('date_birth', models.DateField(null=True, verbose_name='date of birth', blank=True)),
                ('date_death', models.DateField(null=True, verbose_name='date of death', blank=True)),
                ('gender', models.CharField(default=b'm', help_text='Gender of the person.', max_length=2, choices=[(b'f', b'Female'), (b'm', b'Male'), (b'o', b'Other')])),
                ('image', models.ImageField(help_text='An image of the item.', null=True, upload_to=repository.models.utils.image_upload_path, blank=True)),
                ('added_by', models.ForeignKey(related_name='repository_person_added', to=settings.AUTH_USER_MODEL)),
                ('affiliation', models.ManyToManyField(help_text='Organization(s) that this person is affiliated with. For example, a school/university, a club, or a team.', related_name='members', to='repository.Organization', blank=True)),
                ('modified_by', models.ForeignKey(related_name='repository_person_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The name/headline of the item.', max_length=300)),
                ('description', models.TextField(help_text='A short description of the item.', null=True, blank=True)),
                ('same_as', models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity. For example, the URL of the item's Wikipedia page or official website.", null=True, verbose_name='Similar Item', blank=True)),
                ('date_added', models.DateTimeField(help_text='The date time on which the item was created or the item was added to a DataFeed.', auto_now_add=True)),
                ('date_modified', models.DateTimeField(help_text="The date time on which the item was most recently modified or when the item's entry was modified within a DataFeed.", auto_now=True)),
                ('address', models.CharField(help_text='Physical address of the item.', max_length=300, null=True, blank=True)),
                ('has_map', models.URLField(help_text='A URL to a map of the place.', null=True, blank=True)),
                ('added_by', models.ForeignKey(related_name='repository_place_added', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name='repository_place_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Poetry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The name/headline of the item.', max_length=300)),
                ('description', models.TextField(help_text='A short description of the item.', null=True, blank=True)),
                ('same_as', models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity. For example, the URL of the item's Wikipedia page or official website.", null=True, verbose_name='Similar Item', blank=True)),
                ('date_added', models.DateTimeField(help_text='The date time on which the item was created or the item was added to a DataFeed.', auto_now_add=True)),
                ('date_modified', models.DateTimeField(help_text="The date time on which the item was most recently modified or when the item's entry was modified within a DataFeed.", auto_now=True)),
                ('media', models.FileField(help_text='A media for this creative work.', null=True, upload_to=b'uploads/%Y/%m/%d/', blank=True)),
                ('date_published', models.DateTimeField(help_text='Date of first broadcast/publication.', auto_now=True)),
                ('license', models.CharField(help_text='A license document that applies to this content, typically indicated by URL.', max_length=300, null=True, blank=True)),
                ('language', models.CharField(default=b'en', help_text='The language of the content.', max_length=8, choices=[(b'af', b'Afrikaans'), (b'ar', b'Arabic'), (b'ast', b'Asturian'), (b'az', b'Azerbaijani'), (b'bg', b'Bulgarian'), (b'be', b'Belarusian'), (b'bn', b'Bengali'), (b'br', b'Breton'), (b'bs', b'Bosnian'), (b'ca', b'Catalan'), (b'cs', b'Czech'), (b'cy', b'Welsh'), (b'da', b'Danish'), (b'de', b'German'), (b'el', b'Greek'), (b'en', b'English'), (b'en-au', b'Australian English'), (b'en-gb', b'British English'), (b'eo', b'Esperanto'), (b'es', b'Spanish'), (b'es-ar', b'Argentinian Spanish'), (b'es-mx', b'Mexican Spanish'), (b'es-ni', b'Nicaraguan Spanish'), (b'es-ve', b'Venezuelan Spanish'), (b'et', b'Estonian'), (b'eu', b'Basque'), (b'fa', b'Persian'), (b'fi', b'Finnish'), (b'fr', b'French'), (b'fy', b'Frisian'), (b'ga', b'Irish'), (b'gl', b'Galician'), (b'he', b'Hebrew'), (b'hi', b'Hindi'), (b'hr', b'Croatian'), (b'hu', b'Hungarian'), (b'ia', b'Interlingua'), (b'id', b'Indonesian'), (b'io', b'Ido'), (b'is', b'Icelandic'), (b'it', b'Italian'), (b'ja', b'Japanese'), (b'ka', b'Georgian'), (b'kk', b'Kazakh'), (b'km', b'Khmer'), (b'kn', b'Kannada'), (b'ko', b'Korean'), (b'lb', b'Luxembourgish'), (b'lt', b'Lithuanian'), (b'lv', b'Latvian'), (b'mk', b'Macedonian'), (b'ml', b'Malayalam'), (b'mn', b'Mongolian'), (b'mr', b'Marathi'), (b'my', b'Burmese'), (b'nb', b'Norwegian Bokmal'), (b'ne', b'Nepali'), (b'nl', b'Dutch'), (b'nn', b'Norwegian Nynorsk'), (b'os', b'Ossetic'), (b'pa', b'Punjabi'), (b'pl', b'Polish'), (b'pt', b'Portuguese'), (b'pt-br', b'Brazilian Portuguese'), (b'ro', b'Romanian'), (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'sl', b'Slovenian'), (b'sq', b'Albanian'), (b'sr', b'Serbian'), (b'sr-latn', b'Serbian Latin'), (b'sv', b'Swedish'), (b'sw', b'Swahili'), (b'ta', b'Tamil'), (b'te', b'Telugu'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'tt', b'Tatar'), (b'udm', b'Udmurt'), (b'uk', b'Ukrainian'), (b'ur', b'Urdu'), (b'vi', b'Vietnamese'), (b'zh-cn', b'Simplified Chinese'), (b'zh-hans', b'Simplified Chinese'), (b'zh-hant', b'Traditional Chinese'), (b'zh-tw', b'Traditional Chinese')])),
                ('body', models.TextField(help_text='The actual body of the article.')),
                ('added_by', models.ForeignKey(related_name='repository_poetry_added', to=settings.AUTH_USER_MODEL)),
                ('contributor', models.ManyToManyField(help_text='A secondary contributor to the creative work.', related_name='poetry_contributed', to='repository.Person', blank=True)),
                ('creator', models.ForeignKey(related_name='poetry_created', to='repository.Person', help_text='The creator/author of this content.')),
            ],
            options={
                'verbose_name': 'Poetry',
                'verbose_name_plural': 'Poetries',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The name/headline of the item.', max_length=300)),
                ('description', models.TextField(help_text='A short description of the item.', null=True, blank=True)),
                ('same_as', models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity. For example, the URL of the item's Wikipedia page or official website.", null=True, verbose_name='Similar Item', blank=True)),
                ('date_added', models.DateTimeField(help_text='The date time on which the item was created or the item was added to a DataFeed.', auto_now_add=True)),
                ('date_modified', models.DateTimeField(help_text="The date time on which the item was most recently modified or when the item's entry was modified within a DataFeed.", auto_now=True)),
                ('image', models.ImageField(help_text='An image of the item.', null=True, upload_to=repository.models.utils.image_upload_path, blank=True)),
                ('added_by', models.ForeignKey(related_name='repository_product_added', to=settings.AUTH_USER_MODEL)),
                ('is_related_to', models.ManyToManyField(help_text='A pointer to another, somehow related product (or multiple products).', related_name='is_related_to_rel_+', to='repository.Product', blank=True)),
                ('is_similar_to', models.ManyToManyField(help_text='A pointer to another, functionally similar product (or multiple products).', related_name='is_similar_to_rel_+', to='repository.Product', blank=True)),
                ('manufacturer', models.ForeignKey(related_name='owns', blank=True, to='repository.Organization', help_text='The manufacturer of the product.', null=True)),
                ('modified_by', models.ForeignKey(related_name='repository_product_modified', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField(help_text='List of references.')),
            ],
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The name/headline of the item.', max_length=300)),
                ('description', models.TextField(help_text='A short description of the item.', null=True, blank=True)),
                ('same_as', models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity. For example, the URL of the item's Wikipedia page or official website.", null=True, verbose_name='Similar Item', blank=True)),
                ('date_added', models.DateTimeField(help_text='The date time on which the item was created or the item was added to a DataFeed.', auto_now_add=True)),
                ('date_modified', models.DateTimeField(help_text="The date time on which the item was most recently modified or when the item's entry was modified within a DataFeed.", auto_now=True)),
                ('media', models.FileField(help_text='A media for this creative work.', null=True, upload_to=b'uploads/%Y/%m/%d/', blank=True)),
                ('date_published', models.DateTimeField(help_text='Date of first broadcast/publication.', auto_now=True)),
                ('license', models.CharField(help_text='A license document that applies to this content, typically indicated by URL.', max_length=300, null=True, blank=True)),
                ('language', models.CharField(default=b'en', help_text='The language of the content.', max_length=8, choices=[(b'af', b'Afrikaans'), (b'ar', b'Arabic'), (b'ast', b'Asturian'), (b'az', b'Azerbaijani'), (b'bg', b'Bulgarian'), (b'be', b'Belarusian'), (b'bn', b'Bengali'), (b'br', b'Breton'), (b'bs', b'Bosnian'), (b'ca', b'Catalan'), (b'cs', b'Czech'), (b'cy', b'Welsh'), (b'da', b'Danish'), (b'de', b'German'), (b'el', b'Greek'), (b'en', b'English'), (b'en-au', b'Australian English'), (b'en-gb', b'British English'), (b'eo', b'Esperanto'), (b'es', b'Spanish'), (b'es-ar', b'Argentinian Spanish'), (b'es-mx', b'Mexican Spanish'), (b'es-ni', b'Nicaraguan Spanish'), (b'es-ve', b'Venezuelan Spanish'), (b'et', b'Estonian'), (b'eu', b'Basque'), (b'fa', b'Persian'), (b'fi', b'Finnish'), (b'fr', b'French'), (b'fy', b'Frisian'), (b'ga', b'Irish'), (b'gl', b'Galician'), (b'he', b'Hebrew'), (b'hi', b'Hindi'), (b'hr', b'Croatian'), (b'hu', b'Hungarian'), (b'ia', b'Interlingua'), (b'id', b'Indonesian'), (b'io', b'Ido'), (b'is', b'Icelandic'), (b'it', b'Italian'), (b'ja', b'Japanese'), (b'ka', b'Georgian'), (b'kk', b'Kazakh'), (b'km', b'Khmer'), (b'kn', b'Kannada'), (b'ko', b'Korean'), (b'lb', b'Luxembourgish'), (b'lt', b'Lithuanian'), (b'lv', b'Latvian'), (b'mk', b'Macedonian'), (b'ml', b'Malayalam'), (b'mn', b'Mongolian'), (b'mr', b'Marathi'), (b'my', b'Burmese'), (b'nb', b'Norwegian Bokmal'), (b'ne', b'Nepali'), (b'nl', b'Dutch'), (b'nn', b'Norwegian Nynorsk'), (b'os', b'Ossetic'), (b'pa', b'Punjabi'), (b'pl', b'Polish'), (b'pt', b'Portuguese'), (b'pt-br', b'Brazilian Portuguese'), (b'ro', b'Romanian'), (b'ru', b'Russian'), (b'sk', b'Slovak'), (b'sl', b'Slovenian'), (b'sq', b'Albanian'), (b'sr', b'Serbian'), (b'sr-latn', b'Serbian Latin'), (b'sv', b'Swedish'), (b'sw', b'Swahili'), (b'ta', b'Tamil'), (b'te', b'Telugu'), (b'th', b'Thai'), (b'tr', b'Turkish'), (b'tt', b'Tatar'), (b'udm', b'Udmurt'), (b'uk', b'Ukrainian'), (b'ur', b'Urdu'), (b'vi', b'Vietnamese'), (b'zh-cn', b'Simplified Chinese'), (b'zh-hans', b'Simplified Chinese'), (b'zh-hant', b'Traditional Chinese'), (b'zh-tw', b'Traditional Chinese')])),
                ('body', models.TextField(help_text='The actual body of the article.')),
                ('added_by', models.ForeignKey(related_name='repository_snippet_added', to=settings.AUTH_USER_MODEL)),
                ('contributor', models.ManyToManyField(help_text='A secondary contributor to the creative work.', related_name='snippet_contributed', to='repository.Person', blank=True)),
                ('creator', models.ForeignKey(related_name='snippet_created', to='repository.Person', help_text='The creator/author of this content.')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='TaggedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField(verbose_name='Object id', db_index=True)),
                ('content_type', models.ForeignKey(related_name='repository_taggeditem_tagged_items', verbose_name='Content type', to='contenttypes.ContentType')),
                ('tag', models.ForeignKey(related_name='repository_taggeditem_items', to='repository.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='snippet',
            name='keywords',
            field=taggit.managers.TaggableManager(to='repository.Tag', through='repository.TaggedItem', blank=True, help_text='Keywords or tags used to describe this content. Multiple entries in a keywords list are typically delimited by commas.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='snippet',
            name='modified_by',
            field=models.ForeignKey(related_name='repository_snippet_modified', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='snippet',
            name='publisher',
            field=models.ForeignKey(related_name='snippet_published', blank=True, to='repository.Organization', help_text='The publisher(Person or Organization) of the creative work.', null=True),
        ),
        migrations.AddField(
            model_name='snippet',
            name='references',
            field=models.ForeignKey(blank=True, to='repository.Reference', help_text='Resource(s) used in the creation of this resource. A citation or reference to another creative work, such as another publication, web page, scholarly article, etc.', null=True),
        ),
        migrations.AddField(
            model_name='poetry',
            name='keywords',
            field=taggit.managers.TaggableManager(to='repository.Tag', through='repository.TaggedItem', blank=True, help_text='Keywords or tags used to describe this content. Multiple entries in a keywords list are typically delimited by commas.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='poetry',
            name='modified_by',
            field=models.ForeignKey(related_name='repository_poetry_modified', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='poetry',
            name='publisher',
            field=models.ForeignKey(related_name='poetry_published', blank=True, to='repository.Organization', help_text='The publisher(Person or Organization) of the creative work.', null=True),
        ),
        migrations.AddField(
            model_name='poetry',
            name='references',
            field=models.ForeignKey(blank=True, to='repository.Reference', help_text='Resource(s) used in the creation of this resource. A citation or reference to another creative work, such as another publication, web page, scholarly article, etc.', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(related_name='events', to='repository.Place', help_text='The location of for example where the event is happening, or where an action takes place.'),
        ),
        migrations.AddField(
            model_name='event',
            name='modified_by',
            field=models.ForeignKey(related_name='repository_event_modified', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='super_event',
            field=models.ForeignKey(related_name='sub_events', to='repository.Event', help_text='An event that this event is a part of. e.g. a collection of individual music performances might each have a music festival as their super event.', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='contributor',
            field=models.ManyToManyField(help_text='A secondary contributor to the creative work.', related_name='book_contributed', to='repository.Person', blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='creator',
            field=models.ForeignKey(related_name='book_created', to='repository.Person', help_text='The creator/author of this content.'),
        ),
        migrations.AddField(
            model_name='book',
            name='keywords',
            field=taggit.managers.TaggableManager(to='repository.Tag', through='repository.TaggedItem', blank=True, help_text='Keywords or tags used to describe this content. Multiple entries in a keywords list are typically delimited by commas.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='book',
            name='modified_by',
            field=models.ForeignKey(related_name='repository_book_modified', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(related_name='book_published', blank=True, to='repository.Organization', help_text='The publisher(Person or Organization) of the creative work.', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='references',
            field=models.ForeignKey(blank=True, to='repository.Reference', help_text='Resource(s) used in the creation of this resource. A citation or reference to another creative work, such as another publication, web page, scholarly article, etc.', null=True),
        ),
    ]
