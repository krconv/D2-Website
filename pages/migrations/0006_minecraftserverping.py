# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20161019_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='MinecraftServerPing',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('is_online', models.BooleanField(verbose_name='is online')),
                ('status', models.CharField(verbose_name='server status', max_length=16)),
                ('latency', models.DecimalField(decimal_places=2, verbose_name='latency', max_digits=10)),
                ('player_count_online', models.IntegerField(verbose_name='online player count')),
                ('player_count_max', models.IntegerField(verbose_name='maximum player count')),
                ('date', models.DateTimeField(verbose_name='ping date', auto_now_add=True)),
            ],
            options={
                'permissions': (('minecraft_server_address', 'Can view the server host'), ('minecraft_server_status', 'Can view the server status'), ('minecraft_server_players_count', "Can view the server's online player count"), ('minecraft_server_players_names', "Can view the server's online player names")),
            },
        ),
    ]
