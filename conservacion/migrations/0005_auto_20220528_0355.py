# Generated by Django 3.2.12 on 2022-05-28 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('incidente', '0001_initial'),
        ('mincul_app', '0001_initial'),
        ('traslado', '0002_auto_20220528_0355'),
        ('patrimonios', '0003_auto_20220528_0355'),
        ('conservacion', '0004_alter_proyectoconservacion_responsable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentoporactividad',
            name='actividad',
        ),
        migrations.RemoveField(
            model_name='documentoporactividad',
            name='documento',
        ),
        migrations.RemoveField(
            model_name='patrimonioporproyecto',
            name='patrimonio',
        ),
        migrations.RemoveField(
            model_name='patrimonioporproyecto',
            name='proyecto',
        ),
        migrations.RemoveField(
            model_name='documentoportarea',
            name='estado',
        ),
        migrations.RemoveField(
            model_name='tarea',
            name='documentos',
        ),
        migrations.AddField(
            model_name='actividad',
            name='actividadPrecia',
            field=models.ManyToManyField(blank=True, related_name='_conservacion_actividad_actividadPrecia_+', to='conservacion.Actividad'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='proyecto',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='conservacion.proyectoconservacion'),
        ),
        migrations.AddField(
            model_name='proyectoconservacion',
            name='documentos',
            field=models.ManyToManyField(to='mincul_app.Documento'),
        ),
        migrations.AddField(
            model_name='proyectoconservacion',
            name='incidentes',
            field=models.ManyToManyField(to='incidente.Incidente'),
        ),
        migrations.AddField(
            model_name='tarea',
            name='documentos1',
            field=models.ManyToManyField(related_name='documentosTarea', through='conservacion.DocumentoPorTarea', to='mincul_app.Documento'),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='documentos',
            field=models.ManyToManyField(to='mincul_app.Documento'),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='patrimonio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patrimonios.patrimonio'),
        ),
        migrations.AlterField(
            model_name='campoextra',
            name='documento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mincul_app.documento'),
        ),
        migrations.AlterField(
            model_name='documentoportarea',
            name='campo',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='documentoportarea',
            name='documento',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='mincul_app.documento'),
        ),
        migrations.AlterField(
            model_name='documentoportarea',
            name='tarea',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='conservacion.tarea'),
        ),
        migrations.DeleteModel(
            name='ConservadorPorActividad',
        ),
        migrations.DeleteModel(
            name='Documento',
        ),
        migrations.DeleteModel(
            name='DocumentoPorActividad',
        ),
        migrations.DeleteModel(
            name='PatrimonioPorProyecto',
        ),
    ]
