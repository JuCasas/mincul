# Generated by Django 3.2.12 on 2022-06-11 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidente', '0005_auto_20220611_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidente',
            name='descripcion',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
