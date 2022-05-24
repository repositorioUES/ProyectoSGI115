# Generated by Django 3.2.4 on 2022-05-23 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SistemaGerencial', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinica',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('propietario', models.CharField(max_length=50)),
                ('nombreCli', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombrePac', models.CharField(max_length=50)),
                ('especie', models.CharField(max_length=50)),
                ('fechaInscrip', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vacuna',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fechaAplic', models.DateField(auto_now_add=True)),
                ('nombreVac', models.CharField(max_length=100)),
                ('paciente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='SistemaGerencial.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Consultorio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombreCons', models.CharField(max_length=60)),
                ('clinica', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SistemaGerencial.clinica')),
            ],
        ),
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fechaConsulta', models.DateField(auto_now_add=True)),
                ('clinica', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='SistemaGerencial.clinica')),
                ('consultorio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='SistemaGerencial.consultorio')),
                ('paciente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='SistemaGerencial.paciente')),
            ],
        ),
    ]