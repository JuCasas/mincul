# Generated by Django 3.2.12 on 2022-06-24 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conservacion', '0025_tarea_responsable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarea',
            name='estado',
            field=models.CharField(blank=True, choices=[('1', 'Registrada'), ('2', 'En proceso'), ('3', 'Finalizada')], default='1', max_length=2, null=True),
        ),
    ]
