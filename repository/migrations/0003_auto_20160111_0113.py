# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0002_auto_20160109_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='creator',
            field=models.ForeignKey(related_name='book_created', on_delete=django.db.models.deletion.SET_NULL, to='repository.Person', help_text='The creator/author of this content.', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(related_name='book_published', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='repository.Organization', help_text='The publisher(Person or Organization) of the creative work.', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='references',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='repository.Reference', help_text='Resource(s) used in the creation of this resource. A citation or reference to another creative work, such as another publication, web page, scholarly article, etc.', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='same_as',
            field=models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity.                               For example, the URL of the item's Wikipedia page or official website or the URL from where the crawler has collected the data.", null=True, verbose_name='Similar Item', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.ForeignKey(related_name='events', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='repository.Place', help_text='The location of for example where the event is happening, or where an action takes place.', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='same_as',
            field=models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity.                               For example, the URL of the item's Wikipedia page or official website or the URL from where the crawler has collected the data.", null=True, verbose_name='Similar Item', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='super_event',
            field=models.ForeignKey(related_name='sub_events', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='repository.Event', help_text='An event that this event is a part of. e.g. a collection of individual music performances might each have a music festival as their super event.', null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='same_as',
            field=models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity.                               For example, the URL of the item's Wikipedia page or official website or the URL from where the crawler has collected the data.", null=True, verbose_name='Similar Item', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='date_birth',
            field=models.DateField(help_text='yyyy-mm-dd', null=True, verbose_name='date of birth', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='date_death',
            field=models.DateField(help_text='yyyy-mm-dd', null=True, verbose_name='date of death', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='same_as',
            field=models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity.                               For example, the URL of the item's Wikipedia page or official website or the URL from where the crawler has collected the data.", null=True, verbose_name='Similar Item', blank=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='same_as',
            field=models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity.                               For example, the URL of the item's Wikipedia page or official website or the URL from where the crawler has collected the data.", null=True, verbose_name='Similar Item', blank=True),
        ),
        migrations.AlterField(
            model_name='poetry',
            name='creator',
            field=models.ForeignKey(related_name='poetry_created', on_delete=django.db.models.deletion.SET_NULL, to='repository.Person', help_text='The creator/author of this content.', null=True),
        ),
        migrations.AlterField(
            model_name='poetry',
            name='publisher',
            field=models.ForeignKey(related_name='poetry_published', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='repository.Organization', help_text='The publisher(Person or Organization) of the creative work.', null=True),
        ),
        migrations.AlterField(
            model_name='poetry',
            name='references',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='repository.Reference', help_text='Resource(s) used in the creation of this resource. A citation or reference to another creative work, such as another publication, web page, scholarly article, etc.', null=True),
        ),
        migrations.AlterField(
            model_name='poetry',
            name='same_as',
            field=models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity.                               For example, the URL of the item's Wikipedia page or official website or the URL from where the crawler has collected the data.", null=True, verbose_name='Similar Item', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='manufacturer',
            field=models.ForeignKey(related_name='owns', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='repository.Organization', help_text='The manufacturer of the product.', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='same_as',
            field=models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity.                               For example, the URL of the item's Wikipedia page or official website or the URL from where the crawler has collected the data.", null=True, verbose_name='Similar Item', blank=True),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='creator',
            field=models.ForeignKey(related_name='snippet_created', on_delete=django.db.models.deletion.SET_NULL, to='repository.Person', help_text='The creator/author of this content.', null=True),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='publisher',
            field=models.ForeignKey(related_name='snippet_published', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='repository.Organization', help_text='The publisher(Person or Organization) of the creative work.', null=True),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='references',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='repository.Reference', help_text='Resource(s) used in the creation of this resource. A citation or reference to another creative work, such as another publication, web page, scholarly article, etc.', null=True),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='same_as',
            field=models.URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity.                               For example, the URL of the item's Wikipedia page or official website or the URL from where the crawler has collected the data.", null=True, verbose_name='Similar Item', blank=True),
        ),
    ]
