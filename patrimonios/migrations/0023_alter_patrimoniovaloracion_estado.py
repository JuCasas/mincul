# Generated by Django 3.2.12 on 2022-06-16 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0022_merge_20220616_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patrimoniovaloracion',
            name='estado',
            field=models.CharField(choices=[('1', 'Pendiente'), ('2', 'Aceptado')], default='1', max_length=2),
        ),
    ]
