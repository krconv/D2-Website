# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20161017_2050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dutyshift',
            options={'permissions': ('duty', 'Can see the duty displayduty_name', 'Can see the name of the RA on dutyduty_phone', 'Can see the phone number of the RA on dutyduty_room', 'Can see the room of the RA on duty')},
        ),
    ]
