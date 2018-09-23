# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_minecraftserverping'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='minecraftserverping',
            options={'permissions': (('minecraft_status_address', 'Can view the server host'), ('minecraft_status_status', 'Can view the server status'), ('minecraft_status_players_count', "Can view the server's online player count"), ('minecraft_status_players_names', "Can view the server's online player names"))},
        ),
        migrations.AlterModelOptions(
            name='minecraftuser',
            options={'permissions': (('minecraft_register', 'Can add a registered Minecraft user'),)},
        ),
        migrations.RemoveField(
            model_name='minecraftuser',
            name='secret_phrase',
        ),
        migrations.AddField(
            model_name='minecraftuser',
            name='password',
            field=models.CharField(verbose_name='password', default='password', max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='minecraftserverping',
            name='latency',
            field=models.DecimalField(max_digits=10, verbose_name='latency', default=0, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='minecraftserverping',
            name='player_count_max',
            field=models.IntegerField(verbose_name='maximum player count', default=0),
        ),
        migrations.AlterField(
            model_name='minecraftserverping',
            name='player_count_online',
            field=models.IntegerField(verbose_name='online player count', default=0),
        ),
    ]
