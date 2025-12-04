from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class administradoresSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Administradores
        fields = '__all__'

# TODO: Declarar los serializadores para los perfiles de alumnos y maestros


class AlumnoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    fecha_nacimiento = serializers.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model = Alumnos
        fields = '__all__'


class MaestroSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    fecha_nacimiento = serializers.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model = Maestros
        fields = '__all__'


class MateriaSerializer(serializers.ModelSerializer):

    hora_inicio = serializers.TimeField(format='%H:%M')
    hora_final = serializers.TimeField(format='%H:%M')

    class Meta:
        model = Materias
        fields = '__all__'
