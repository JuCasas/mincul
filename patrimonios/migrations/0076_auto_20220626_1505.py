# Generated by Django 3.2.12 on 2022-06-26 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0075_auto_20220626_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patrimonioetnografico',
            name='diametro',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='patrimonioetnografico',
            name='fondo',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
