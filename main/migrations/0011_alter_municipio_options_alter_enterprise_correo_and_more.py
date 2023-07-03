# Generated by Django 4.2.1 on 2023-07-03 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_remove_enterprise_provincia'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='municipio',
            options={'ordering': ('nombre',)},
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='correo',
            field=models.EmailField(blank=True, max_length=250, null=True, verbose_name='Teléfono'),
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='fecha_aprobacion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de aprobación'),
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='representante',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Representante'),
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='telefono',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Teléfono'),
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='tipo',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Tipo'),
        ),
    ]
