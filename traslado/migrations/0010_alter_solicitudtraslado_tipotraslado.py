# Generated by Django 3.2.12 on 2022-06-23 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traslado', '0009_alter_solicitudtraslado_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudtraslado',
            name='tipoTraslado',
            field=models.CharField(blank=True, choices=[('1', 'Exposición en el extranjero'), ('2', 'Exponsición nacional'), ('3', 'Misión Diplomática')], default='1', max_length=2, null=True),
        ),
    ]
