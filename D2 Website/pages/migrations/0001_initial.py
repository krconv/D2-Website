# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DutyShift',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('date', models.DateField(verbose_name='shift date')),
                ('name', models.CharField(verbose_name='RA name', max_length=25)),
                ('phone', models.CharField(blank=True, verbose_name='RA phone number', max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='DutyShiftSource',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('spreadsheet_id', models.CharField(verbose_name='spreadsheet ID', max_length=50)),
                ('range', models.CharField(verbose_name='spreadsheet range', max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='MinecraftUser',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('username', models.CharField(verbose_name='in-game username', max_length=16)),
                ('secret_phrase', models.CharField(verbose_name='secret login phrase', max_length=32)),
                ('banned', models.BooleanField(verbose_name='banned', default=False)),
                ('last_login_date', models.DateTimeField(verbose_name='last login date')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
            options={
                'permissions': ('minecraft_add', 'Can add a registered Minecraft user'),
            },
        ),
        migrations.AddField(
            model_name='dutyshift',
            name='source',
            field=models.ForeignKey(to='pages.DutyShiftSource', verbose_name='data source'),
        ),
    ]
