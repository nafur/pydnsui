# Generated by Django 3.0.4 on 2020-04-02 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('federation', '0014_server_auth_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='zone',
            name='authorative',
            field=models.BooleanField(default=True, verbose_name='This instances is authorative for the configuration of this zone.'),
        ),
    ]