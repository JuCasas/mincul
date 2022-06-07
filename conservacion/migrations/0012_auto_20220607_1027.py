# Generated by Django 3.2.12 on 2022-06-07 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mincul_app', '0001_initial'),
        ('conservacion', '0011_auto_20220602_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('contenido', models.CharField(blank=True, max_length=200, null=True)),
                ('estado', models.CharField(blank=True, choices=[('1', 'Activo'), ('2', 'Inactivo')], default='1', max_length=2, null=True)),
                ('documentos', models.ManyToManyField(to='mincul_app.Documento')),
            ],
        ),
        migrations.RemoveField(
            model_name='documentoportarea',
            name='documento',
        ),
        migrations.RemoveField(
            model_name='documentoportarea',
            name='tarea',
        ),
        migrations.RemoveField(
            model_name='tarea',
            name='documentos',
        ),
        migrations.RemoveField(
            model_name='tarea',
            name='herramientas',
        ),
        migrations.RemoveField(
            model_name='tarea',
            name='indumentaria',
        ),
        migrations.RemoveField(
            model_name='tarea',
            name='materiales',
        ),
        migrations.DeleteModel(
            name='CampoExtra',
        ),
        migrations.DeleteModel(
            name='DocumentoPorTarea',
        ),
        migrations.AddField(
            model_name='campo',
            name='tarea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conservacion.tarea'),
        ),
    ]
