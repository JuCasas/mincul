# Generated by Django 3.2.12 on 2022-06-18 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mincul_app', '0002_alter_documento_url'),
        ('patrimonios', '0026_patrimonio_documentos'),
    ]

    operations = [
        migrations.AddField(
            model_name='institucion',
            name='documentos',
            field=models.ManyToManyField(to='mincul_app.Documento'),
        ),
    ]