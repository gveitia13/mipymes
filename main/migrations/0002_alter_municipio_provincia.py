# Generated by Django 4.2.1 on 2023-07-04 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='municipio',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='municipios', to='main.provincia'),
        ),
    ]
