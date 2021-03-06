# Generated by Django 3.2.12 on 2022-06-16 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0019_auto_20220616_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='tipo',
            field=models.CharField(choices=[('1', 'Inmaterial'), ('2', 'Material Inmueble'), ('3', 'Material Mueble')], max_length=2),
        ),
        migrations.AlterField(
            model_name='patrimonio',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patrimonios.categoria'),
        ),
        migrations.AlterField(
            model_name='patrimonio',
            name='tipoPatrimonio',
            field=models.CharField(choices=[('1', 'Inmaterial'), ('2', 'Material Inmueble'), ('3', 'Material Mueble')], default='1', max_length=2),
        ),
    ]
