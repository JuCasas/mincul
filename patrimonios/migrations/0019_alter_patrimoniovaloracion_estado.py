# Generated by Django 3.2.12 on 2022-06-16 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0018_merge_20220615_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patrimoniovaloracion',
            name='estado',
            field=models.CharField(choices=[('1', 'Registrado'), ('2', 'Aceptado')], default='1', max_length=2),
        ),
    ]
