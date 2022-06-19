# Generated by Django 3.2.12 on 2022-06-19 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0030_puntogeografico'),
        ('incidente', '0007_auto_20220617_2148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incidente',
            name='institucion',
        ),
        migrations.RemoveField(
            model_name='incidente',
            name='patrimonio',
        ),
        migrations.RemoveField(
            model_name='incidente',
            name='tipoIncidentado',
        ),
        migrations.AddField(
            model_name='incidente',
            name='zona',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patrimonios.puntogeografico'),
        ),
    ]
