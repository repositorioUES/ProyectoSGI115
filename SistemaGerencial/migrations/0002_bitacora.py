# Generated by Django 3.2.4 on 2022-06-03 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SistemaGerencial', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bitacora',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nomUsuario', models.CharField(max_length=50)),
                ('usuarioId', models.IntegerField()),
                ('nomPersona', models.CharField(max_length=100)),
                ('accion', models.CharField(max_length=100)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
