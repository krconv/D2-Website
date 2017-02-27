# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_auto_20161021_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='minecraftuser',
            name='last_login_date',
        ),
        migrations.AlterField(
            model_name='minecraftuser',
            name='username',
            field=models.CharField(unique=True, max_length=16, verbose_name='in-game username'),
        ),
    ]
