# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20161019_1027'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='minecraftuser',
            options={'permissions': ('minecraft_register', 'Can add a registered Minecraft user')},
        ),
    ]
