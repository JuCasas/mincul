# Generated by Django 3.2.12 on 2022-06-26 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0070_auto_20220625_0948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patrimoniohistoricoartistico',
            name='material',
        ),
        migrations.AlterField(
            model_name='patrimonioarqueologico',
            name='cultura',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='patrimonioetnografico',
            name='filacionCultural',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='patrimonioetnografico',
            name='procedencia',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='patrimoniopaleontologico',
            name='clase',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='patrimoniopaleontologico',
            name='epocaGeologica',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='patrimoniopaleontologico',
            name='eraGeologica',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='patrimoniopaleontologico',
            name='phylumDivision',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='patrimoniopaleontologico',
            name='reino',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='patrimoniopaleontologico',
            name='tipoFosilizacion',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='patrimoniopaleontologico',
            name='tipoMuestra',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
