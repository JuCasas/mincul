# Generated by Django 3.2.12 on 2022-06-21 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonios', '0038_auto_20220621_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='institucion',
            name='url',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
