from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

from django.db import models
from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"


class Administradores(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    clave_admin = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    ocupacion = models.CharField(max_length=255, null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del admin "+self.user.first_name+" "+self.user.last_name

# TODO: Agregar perfiles para estudiantes y profesores


class Alumnos(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    clave_alumno = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    curp = models.CharField(max_length=18, null=True, blank=True)
    rfc = models.CharField(max_length=13, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    ocupacion = models.CharField(max_length=255, null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Alumno {self.user.first_name} {self.user.last_name}"


class Maestros(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False)
    clave_maestros = models.CharField(
        max_length=100, unique=True, null=False, blank=False)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    rfc = models.CharField(max_length=13, null=True, blank=True)
    cubiculo = models.CharField(max_length=255, null=True, blank=True)
    area_investigacion = models.CharField(
        max_length=255, null=True, blank=True)
    # solo con el list ya sirve para que sepa que va a recibir una listah
    materias_json = models.JSONField(default=list, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Perfil del maestro {self.user.first_name} {self.user.last_name}"


class Materias(models.Model):
    id = models.BigAutoField(primary_key=True)
    nrc = models.CharField(max_length=20, unique=True, null=False, blank=False)
    nombre_materia = models.CharField(max_length=255, null=False, blank=False)
    seccion = models.CharField(max_length=50, null=False, blank=False)
    dias = models.JSONField(default=list, blank=True)
    hora_inicio = models.TimeField(null=False, blank=False)
    hora_final = models.TimeField(null=False, blank=False)
    salon = models.CharField(max_length=100, null=False, blank=False)
    programa_educativo = models.CharField(
        max_length=255, null=False, blank=False)
    profesor_asignado = models.ForeignKey(
        Maestros,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    creditos = models.PositiveIntegerField(null=False, blank=False)
    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Materia {self.nombre_materia} - NRC {self.nrc}"
