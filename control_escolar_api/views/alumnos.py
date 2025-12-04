from django.db.models import *
from django.db import transaction
from control_escolar_api.serializers import UserSerializer
from control_escolar_api.serializers import *
from control_escolar_api.models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404


class AlumnosAll(generics.CreateAPIView):
    # Esta función es esencial para todo donde se requiera autorización de inicio de sesión (token)
    permission_classes = (permissions.IsAuthenticated,)
    # Invocamos la petición GET para obtener todos los alumnos

    def get(self, request, *args, **kwargs):
        alumnos = Alumnos.objects.filter(user__is_active=1).order_by("id")
        lista = AlumnoSerializer(alumnos, many=True).data
        return Response(lista, 200)


class AlumnoView(generics.CreateAPIView):

    # Permisos por método (sobrescribe el comportamiento default)
    # Verifica que el usuario esté autenticado para las peticiones GET, PUT y DELETE
    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return []  # POST no requiere autenticación

    def get(self, request, *args, **kwargs):
        alumnos = get_object_or_404(Alumnos, id=request.GET.get("id"))
        admin = AlumnoSerializer(alumnos, many=False).data
        # Si todo es correcto, regresamos la información
        return Response(admin, 200)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Serializamos los datos del administrador para volverlo de nuevo JSON
        user = UserSerializer(data=request.data)

        if user.is_valid():
            # guardar los datos del alumno
            role = request.data['rol']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']
 # Valida si existe el usuario o bien el email registrado
            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                return Response({"message": f"El correo {email} ya está registrado"}, 400)

            user = User.objects.create(username=email,
                                       email=email,
                                       first_name=first_name,
                                       last_name=last_name,
                                       is_active=1)
            user.save()
            user.set_password(password)
            user.save()

            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            group.save()

            alumno = Alumnos.objects.create(user=user,
                                            clave_alumno=request.data["clave_alumno"],
                                            fecha_nacimiento=request.data["fecha_nacimiento"],
                                            curp=request.data["curp"].upper(),
                                            rfc=request.data["rfc"].upper(),
                                            edad=request.data["edad"],
                                            telefono=request.data["telefono"],
                                            ocupacion=request.data["ocupacion"]
                                            )
            alumno.save()

            return Response({"Alumno creado con el ID: ": alumno.id}, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

        # Actualizar datos del alumno

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        # Primero obtenemos el administrador a actualizar
        alumno = get_object_or_404(Alumnos, id=request.data["id"])
        alumno.clave_alumno = request.data["clave_alumno"]
        alumno.telefono = request.data["telefono"]
        alumno.rfc = request.data["rfc"]
        alumno.curp = request.data["curp"]
        alumno.edad = request.data["edad"]
        alumno.fecha_nacimiento = request.data["fecha_nacimiento"]
        alumno.ocupacion = request.data["ocupacion"]
        alumno.save()
        # Actualizamos los datos del usuario asociado (tabla auth_user de Django)
        user = alumno.user
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()

        return Response({"message": "Alumno actualizado correctamente", "alumno": AlumnoSerializer(alumno).data}, 200)
        # return Response(user,200)

        # eliminar maestros

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        alumno = get_object_or_404(Alumnos, id=request.GET.get("id"))
        try:
            alumno.user.delete()
            return Response({"details": "Alumno eliminado"}, 200)
        except Exception as e:
            return Response({"details": "Algo pasó al eliminar"}, 400)
