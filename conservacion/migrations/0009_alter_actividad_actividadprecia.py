# Generated by Django 4.0.3 on 2022-06-01 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conservacion', '0008_alter_actividad_actividadprecia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='actividadPrecia',
            field=models.ManyToManyField(blank=True, to='conservacion.actividad'),
        ),
    ]