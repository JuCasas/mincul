# Generated by Django 3.2.12 on 2022-05-24 06:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conservacion', '0003_auto_20220523_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyectoconservacion',
            name='responsable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
