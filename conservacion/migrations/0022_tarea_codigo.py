# Generated by Django 3.2.12 on 2022-06-22 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conservacion', '0021_alter_proyectoconservacion_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarea',
            name='codigo',
            field=models.CharField(max_length=8, null=True),
        ),
    ]
