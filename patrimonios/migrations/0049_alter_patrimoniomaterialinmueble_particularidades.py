# Generated by Django 3.2.12 on 2022-06-23 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0048_auto_20220623_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patrimoniomaterialinmueble',
            name='particularidades',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
