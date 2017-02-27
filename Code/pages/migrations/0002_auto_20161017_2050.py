# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='minecraftuser',
            name='last_login_date',
            field=models.DateTimeField(null=True, verbose_name='last login date'),
        ),
    ]
