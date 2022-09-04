from asyncio import constants
from asyncio.windows_events import NULL
from tkinter import CASCADE
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Lavadero(models.Model):
    ESTADOS = [
        ('A', 'Abierto'),
        ('C', 'Cerrado'),
        ('I', 'Inactivo')
    ]

    nombre = models.CharField(max_length=128)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    telefono_aux = models.CharField(max_length=15, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=1,
        choices=ESTADOS,
        default='C',
    )
    encargado = models.CharField(max_length=128, default="")
    imagen = models.ImageField(null=True, blank=True, upload_to="images/")
    objects = models.Manager()

    def __str__(self):
        return self.nombre

class Tarifa(models.Model):
    TIPOS_LAVADO = [
        ('M', 'Moto'),
        ('A', 'Auto'),
        ('P', 'Pickup'),
        ('C', 'Camion')
    ]

    tipo = models.CharField(
        max_length=1,
        choices=TIPOS_LAVADO,
    )
    lavadero = models.ForeignKey(Lavadero, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tipo', 'lavadero'], name='unique_tipo_lavadero_combination'
            )
        ]

class Horario(models.Model):
    DIAS = [
        ('L', 'Lunes'),
        ('M', 'Martes'),
        ('X', 'Miercoles'),
        ('J', 'Jueves'),
        ('V', 'Viernes'),
        ('S', 'Sabado'),
        ('D', 'Domingo')
    ]

    lavadero = models.ForeignKey(Lavadero, on_delete=models.CASCADE)
    dia = models.CharField(
        max_length=1,
        choices=DIAS,
    )
    desde = models.TimeField()
    hasta = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['lavadero', 'dia'], name ='unique_lavadero_dia_combination'
            )
        ]
