# Generated by Django 3.2.12 on 2022-06-18 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0024_auto_20220617_2148'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='autor',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='autor',
            name='long',
        ),
        migrations.AddField(
            model_name='institucion',
            name='lat',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='institucion',
            name='long',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
    ]
