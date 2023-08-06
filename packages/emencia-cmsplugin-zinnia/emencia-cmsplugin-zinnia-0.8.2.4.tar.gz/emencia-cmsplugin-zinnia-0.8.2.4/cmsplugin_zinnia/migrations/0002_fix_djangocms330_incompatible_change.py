# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


from cmsplugin_zinnia.choices_helpers import get_template_choices


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_zinnia', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarentriesplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(related_name='cmsplugin_zinnia_calendarentriesplugin', primary_key=True,
                                       serialize=False, auto_created=True, to='cms.CMSPlugin', parent_link=True, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='latestentriesplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(related_name='cmsplugin_zinnia_latestentriesplugin', primary_key=True,
                                       serialize=False, auto_created=True, to='cms.CMSPlugin', parent_link=True, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='latestentriesplugin',
            name='template_to_render',
            field=models.CharField(choices=get_template_choices(),
                                   blank=True, verbose_name='template', max_length=250,
                                   help_text='template used to display the plugin'),
        ),
        migrations.AlterField(
            model_name='queryentriesplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(related_name='cmsplugin_zinnia_queryentriesplugin', primary_key=True,
                                       serialize=False, auto_created=True, to='cms.CMSPlugin', parent_link=True, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='queryentriesplugin',
            name='template_to_render',
            field=models.CharField(choices=get_template_choices(),
                                   blank=True, verbose_name='template', max_length=250,
                                   help_text='template used to display the plugin'),
        ),
        migrations.AlterField(
            model_name='randomentriesplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(related_name='cmsplugin_zinnia_randomentriesplugin', primary_key=True,
                                       serialize=False, auto_created=True, to='cms.CMSPlugin', parent_link=True, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='randomentriesplugin',
            name='template_to_render',
            field=models.CharField(choices=get_template_choices(),
                                   blank=True, verbose_name='template', max_length=250,
                                   help_text='template used to display the plugin'),
        ),
        migrations.AlterField(
            model_name='selectedentriesplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(related_name='cmsplugin_zinnia_selectedentriesplugin', primary_key=True,
                                       serialize=False, auto_created=True, to='cms.CMSPlugin', parent_link=True, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='selectedentriesplugin',
            name='template_to_render',
            field=models.CharField(choices=get_template_choices(),
                                   blank=True, verbose_name='template', max_length=250,
                                   help_text='template used to display the plugin'),
        ),
    ]
