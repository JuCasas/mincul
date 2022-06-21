# Generated by Django 3.2.12 on 2022-06-20 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0030_puntogeografico'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patrimonioinmaterial',
            name='tipo',
        ),
        migrations.AddField(
            model_name='patrimonioinmaterial',
            name='tipoInmaterial',
            field=models.CharField(choices=[('1', 'Acontecimientos Programados'), ('2', 'Folclore')], default='1', max_length=2),
        ),
        migrations.AlterField(
            model_name='patrimonioinmaterial',
            name='subtipo',
            field=models.CharField(choices=[('1', 'Artístico'), ('2', 'Eventos'), ('3', 'Fiestas'), ('4', 'Artesanía y Artes'), ('5', 'Creencias Populares'), ('6', 'Ferias y Mercados'), ('7', 'Gastronomía'), ('8', 'Músicas y Danzas')], default='1', max_length=2),
        ),
    ]
