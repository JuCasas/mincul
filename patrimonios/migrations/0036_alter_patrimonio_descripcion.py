# Generated by Django 3.2.12 on 2022-06-20 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0035_alter_patrimonio_observacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patrimonio',
            name='descripcion',
            field=models.CharField(max_length=4000, null=True),
        ),
    ]
