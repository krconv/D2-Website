# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DutyDisplay',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('spreadsheet_id', models.CharField(max_length=50, verbose_name='spreadsheet ID')),
                ('range', models.CharField(max_length=25, verbose_name='spreadsheet range')),
            ],
        ),
        migrations.CreateModel(
            name='DutyShift',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('date', models.DateField(verbose_name='shift date')),
                ('name', models.CharField(max_length=25, verbose_name='RA name')),
                ('phone', models.CharField(blank=True, max_length=25, verbose_name='phone')),
            ],
        ),
    ]
