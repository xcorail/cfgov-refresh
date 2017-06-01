# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from wagtail.wagtailimages.utils import get_fill_filter_spec_migrations


# See https://github.com/wagtail/wagtail/issues/3259 for why this is necessary.
wforward, wreverse = get_fill_filter_spec_migrations('v1', 'CFGOVRendition')


def forward(apps, schema_migration):
    return wforward(apps, schema_migration)


def reverse(apps, schema_migration):
    return wreverse(apps, schema_migration)


class Migration(migrations.Migration):

	dependencies = [
		('v1', '0039_add_filter_spec_to_cfgovrendition'),
	]

	operations = [
		migrations.RunPython(forward, reverse),
	]
