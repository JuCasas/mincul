# Generated by Django 3.2.12 on 2022-05-24 02:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conservacion', '0003_auto_20220523_2133'),
        ('patrimonios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudTraslado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doiSolicitante', models.CharField(blank=True, max_length=12, null=True)),
                ('nombreSolicitante', models.CharField(blank=True, max_length=200, null=True)),
                ('direccion', models.CharField(blank=True, max_length=200, null=True)),
                ('distrito', models.CharField(blank=True, max_length=100, null=True)),
                ('provincia', models.CharField(blank=True, max_length=100, null=True)),
                ('departamento', models.CharField(blank=True, max_length=100, null=True)),
                ('telefonoSolicitante', models.CharField(blank=True, max_length=9, null=True)),
                ('celularSolicitante', models.CharField(blank=True, max_length=9, null=True)),
                ('correoSolicitante', models.CharField(blank=True, max_length=100, null=True)),
                ('representanteLegal', models.CharField(blank=True, max_length=100, null=True)),
                ('doiRepresentante', models.CharField(blank=True, max_length=12, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=200, null=True)),
                ('nombreResponsable', models.CharField(blank=True, max_length=200, null=True)),
                ('numeroRNAoRNDA', models.CharField(blank=True, max_length=20, null=True)),
                ('domicilioResponsable', models.CharField(blank=True, max_length=200, null=True)),
                ('procedenciaMuestras', models.CharField(blank=True, max_length=200, null=True)),
                ('personaEfectuaraTraslado', models.CharField(blank=True, max_length=200, null=True)),
                ('destino', models.CharField(blank=True, max_length=200, null=True)),
                ('fechaSalidaProgramada', models.DateField(blank=True, null=True, verbose_name='fechaSalidaProgramada')),
                ('fechaRetornoProgramada', models.DateField(blank=True, null=True, verbose_name='fechaRetornoProgramada')),
                ('fechaSalidaReal', models.DateField(blank=True, null=True, verbose_name='fechaSalidaReal')),
                ('fechaRetornoReal', models.DateField(blank=True, null=True, verbose_name='fechaRetornoReal')),
                ('estado', models.CharField(blank=True, choices=[('1', 'Activo'), ('2', 'Inactivo')], default='1', max_length=2, null=True)),
                ('documentos', models.ManyToManyField(to='conservacion.Documento')),
                ('gestor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gestor', to=settings.AUTH_USER_MODEL)),
                ('gestorConservacionTraslados', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gestorConservacionTraslados', to=settings.AUTH_USER_MODEL)),
                ('patrimonios', models.ManyToManyField(to='patrimonios.Patrimonio')),
            ],
        ),
        migrations.CreateModel(
            name='SolicitudPorPatrimonio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(blank=True, choices=[('1', 'Activo'), ('2', 'Inactivo')], default='1', max_length=2, null=True)),
                ('patrimonio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patrimonios.patrimonio')),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traslado.solicitudtraslado')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentoPorSolicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(blank=True, choices=[('0', 'Documento'), ('1', 'Declaracion Jurada')], default='1', max_length=2, null=True)),
                ('estado', models.CharField(blank=True, choices=[('1', 'Activo'), ('2', 'Inactivo')], default='1', max_length=2, null=True)),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conservacion.documento')),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traslado.solicitudtraslado')),
            ],
        ),
    ]
