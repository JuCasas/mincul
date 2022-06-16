# Generated by Django 3.2.12 on 2022-06-12 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0014_auto_20220611_1912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propietario',
            name='pronombre',
        ),
        migrations.RemoveField(
            model_name='propietario',
            name='url',
        ),
        migrations.AddField(
            model_name='patrimonio',
            name='pronombre',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='patrimonio',
            name='url',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]