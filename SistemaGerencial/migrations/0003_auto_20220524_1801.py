# Generated by Django 3.2.4 on 2022-05-25 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SistemaGerencial', '0002_auto_20220524_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consulta',
            name='fecha',
        ),
        migrations.AddField(
            model_name='consulta',
            name='hora',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]