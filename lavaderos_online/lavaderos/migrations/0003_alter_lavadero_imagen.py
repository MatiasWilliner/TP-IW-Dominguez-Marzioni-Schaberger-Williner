# Generated by Django 4.1 on 2022-09-03 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lavaderos', '0002_lavadero_encargado_lavadero_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lavadero',
            name='imagen',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
