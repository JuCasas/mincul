# Generated by Django 3.2.12 on 2022-06-15 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0014_auto_20220612_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='institucion',
            name='campo',
            field=models.CharField(max_length=200, null=True),
        ),
    ]