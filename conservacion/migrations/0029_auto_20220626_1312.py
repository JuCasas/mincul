# Generated by Django 3.2.12 on 2022-06-26 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conservacion', '0028_alter_campo_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campo',
            name='estado',
            field=models.CharField(blank=True, choices=[('1', 'Activo'), ('2', 'Inactivo')], default='1', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='estado',
            field=models.CharField(blank=True, choices=[('1', 'Registrada'), ('2', 'En proceso'), ('3', 'En evaluacion'), ('4', 'Rechazada'), ('5', 'Finalizada')], default='1', max_length=2, null=True),
        ),
    ]
