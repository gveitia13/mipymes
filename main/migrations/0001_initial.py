# Generated by Django 4.2.1 on 2023-07-03 09:22

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', ckeditor.fields.RichTextField(verbose_name='Contacto')),
            ],
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250, unique=True, verbose_name='Nombre')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='enterprise/logo/', verbose_name='Logo')),
                ('tipo', models.CharField(blank=True, max_length=250, null=True, verbose_name='Tipo')),
                ('actividad', models.CharField(max_length=250, verbose_name='Actividad')),
                ('representante', models.CharField(blank=True, max_length=250, null=True, verbose_name='Representante')),
                ('telefono', models.CharField(blank=True, max_length=250, null=True, verbose_name='Teléfono')),
                ('correo', models.EmailField(blank=True, max_length=250, null=True, verbose_name='Correo')),
                ('fecha_aprobacion', models.DateField(blank=True, null=True, verbose_name='Fecha de aprobación')),
                ('is_active', models.BooleanField(default=False, verbose_name='Aprobado')),
            ],
            options={
                'verbose_name': 'Empresa',
                'ordering': ('is_active',),
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250, unique=True, verbose_name='Nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector', models.CharField(max_length=250, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Sector',
                'verbose_name_plural': 'Sectores',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servicio', models.CharField(max_length=250, verbose_name='Servicio')),
                ('enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicios', to='main.enterprise')),
            ],
            options={
                'verbose_name': 'Servicio',
            },
        ),
        migrations.CreateModel(
            name='Publicidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='publicidad/thumbnail/', verbose_name='Thumbnail')),
                ('image', models.ImageField(upload_to='publicidad/imagen/', verbose_name='Imagen')),
                ('link', models.URLField(verbose_name='Link')),
                ('enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publicidades', to='main.enterprise')),
            ],
            options={
                'verbose_name': 'Publicidad',
                'verbose_name_plural': 'Publicidades',
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250, verbose_name='Nombre')),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.provincia')),
            ],
            options={
                'ordering': ('nombre',),
            },
        ),
        migrations.AddField(
            model_name='enterprise',
            name='municipio',
            field=models.ForeignKey(blank=True, max_length=250, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.municipio'),
        ),
        migrations.AddField(
            model_name='enterprise',
            name='sectores',
            field=models.ManyToManyField(blank=True, null=True, related_name='sectores', to='main.sector'),
        ),
        migrations.CreateModel(
            name='Enlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enlace', models.URLField(verbose_name='Enlace')),
                ('nombre', models.CharField(max_length=250, verbose_name='Nombre')),
                ('enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enlaces', to='main.enterprise')),
            ],
            options={
                'verbose_name': 'Enlace',
            },
        ),
    ]
