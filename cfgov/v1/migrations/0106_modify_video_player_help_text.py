# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0105_add_eyebrow_to_text_introduction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='live_stream_url',
            field=models.URLField(help_text=b'Format: https://www.youtube.com/embed/video_id.', verbose_name=b'URL', blank=True),
        ),
    ]
