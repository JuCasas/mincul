# Generated by Django 3.2.12 on 2022-06-12 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0013_propietario_documentos'),
    ]

    operations = [
        migrations.AddField(
            model_name='propietario',
            name='pronombre',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='propietario',
            name='url',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]