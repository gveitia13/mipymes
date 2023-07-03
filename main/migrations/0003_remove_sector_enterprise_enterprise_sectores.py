# Generated by Django 4.2.1 on 2023-07-03 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_enterprise_fecha_aprobacion_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sector',
            name='enterprise',
        ),
        migrations.AddField(
            model_name='enterprise',
            name='sectores',
            field=models.ManyToManyField(related_name='sectores', to='main.sector'),
        ),
    ]
