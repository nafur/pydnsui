# Generated by Django 3.0.4 on 2020-04-02 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('federation', '0015_zone_authorative'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zone',
            name='authorative',
        ),
        migrations.AddField(
            model_name='server',
            name='configured_here',
            field=models.BooleanField(default=True, verbose_name='Zones for this server are configured here.'),
        ),
    ]