# Generated by Django 3.2.12 on 2022-06-22 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidente', '0008_auto_20220619_0057'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidente',
            name='codigo',
            field=models.CharField(max_length=10, null=True),
        ),
    ]