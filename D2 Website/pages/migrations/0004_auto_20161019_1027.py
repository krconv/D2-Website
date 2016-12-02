# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20161019_1021'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dutyshift',
            options={'permissions': (('duty_display', 'Can see the duty display'), ('duty_name', 'Can see the name of the RA on duty'), ('duty_phone', 'Can see the phone number of the RA on duty'), ('duty_room', 'Can see the room of the RA on duty'))},
        ),
    ]
