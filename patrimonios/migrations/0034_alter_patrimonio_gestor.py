# Generated by Django 3.2.12 on 2022-06-20 22:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patrimonios', '0033_alter_patrimonio_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patrimonio',
            name='gestor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
