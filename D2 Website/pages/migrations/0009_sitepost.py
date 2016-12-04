# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_auto_20161203_1008'),
    ]

    operations = [
        migrations.CreateModel(
            name='SitePost',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=30)),
                ('author', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=500)),
            ],
        ),
    ]
