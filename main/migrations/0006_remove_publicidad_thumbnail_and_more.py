# Generated by Django 4.2.1 on 2023-07-19 02:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_config_alter_provincia_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicidad',
            name='thumbnail',
        ),
        migrations.RemoveField(
            model_name='publicidadgeneral',
            name='thumbnail',
        ),
    ]
