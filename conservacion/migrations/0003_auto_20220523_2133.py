# Generated by Django 3.2.12 on 2022-05-24 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0001_initial'),
        ('conservacion', '0002_auto_20220523_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyectoconservacion',
            name='estado',
            field=models.CharField(blank=True, choices=[('1', 'Activo'), ('2', 'Inactivo')], default='1', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='proyectoconservacion',
            name='tipoProyecto',
            field=models.CharField(blank=True, choices=[('0', 'Preventivo'), ('1', 'Correctivo')], default='0', max_length=2, null=True),
        ),
        migrations.CreateModel(
            name='PatrimonioPorProyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(blank=True, choices=[('1', 'Activo'), ('2', 'Inactivo')], default='1', max_length=2, null=True)),
                ('patrimonio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patrimonios.patrimonio')),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conservacion.proyectoconservacion')),
            ],
        ),
    ]
