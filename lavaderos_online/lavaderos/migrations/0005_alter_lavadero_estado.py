# Generated by Django 4.1 on 2022-09-20 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lavaderos', '0004_alter_lavadero_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lavadero',
            name='estado',
            field=models.CharField(choices=[('A', 'Abierto'), ('C', 'Cerrado'), ('I', 'Inactivo'), ('D', 'Disponible')], default='C', max_length=1),
        ),
    ]
