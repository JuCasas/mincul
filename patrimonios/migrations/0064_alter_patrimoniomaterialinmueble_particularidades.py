# Generated by Django 3.2.12 on 2022-06-23 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0063_alter_responsable_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patrimoniomaterialinmueble',
            name='particularidades',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
    ]
