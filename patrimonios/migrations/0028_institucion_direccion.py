# Generated by Django 3.2.12 on 2022-06-18 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0027_institucion_documentos'),
    ]

    operations = [
        migrations.AddField(
            model_name='institucion',
            name='direccion',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
