# Generated by Django 3.2.12 on 2022-06-14 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traslado', '0006_solicitudtraslado_detallerechazo'),
    ]

    operations = [
        migrations.AddField(
            model_name='entidadsolicitante',
            name='estado',
            field=models.CharField(blank=True, choices=[('1', 'Activo'), ('2', 'Inactivo')], default='1', max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='entidadsolicitante',
            name='tipo',
            field=models.CharField(blank=True, choices=[('0', 'Tipo1'), ('1', 'Tipo2')], default='1', max_length=2, null=True),
        ),
    ]