# Generated by Django 3.2.12 on 2022-06-22 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0039_institucion_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividadturistica',
            name='categoria',
            field=models.CharField(default='1', max_length=100),
        ),
        migrations.AlterField(
            model_name='actividadturistica',
            name='tipo',
            field=models.CharField(default='1', max_length=100),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='categoria',
            field=models.CharField(default='1', max_length=100),
        ),
    ]
