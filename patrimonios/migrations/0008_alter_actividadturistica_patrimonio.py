# Generated by Django 3.2.12 on 2022-06-07 04:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0007_auto_20220606_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividadturistica',
            name='patrimonio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patrimonios.patrimonio'),
        ),
    ]
