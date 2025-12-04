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
import json
from django.shortcuts import get_object_or_404


class MaestrosAll(generics.CreateAPIView):
    # Esta función es esencial para todo donde se requiera autorización de inicio de sesión (token)
    permission_classes = (permissions.IsAuthenticated,)
    # Invocamos la petición GET para obtener todos los maestros

    def get(self, request, *args, **kwargs):
        maestros = Maestros.objects.filter(user__is_active=1).order_by("id")
        lista = MaestroSerializer(maestros, many=True).data
        for maestro in lista:
            if isinstance(maestro, dict) and "materias_json" in maestro:
                try:
                    maestro["materias_json"] = json.loads(
                        maestro["materias_json"])
                except Exception:
                    maestro["materias_json"] = []

        return Response(lista, 200)


class MaestroView(generics.CreateAPIView):

    # Permisos por método (sobrescribe el comportamiento default)
    # Verifica que el usuario esté autenticado para las peticiones GET, PUT y DELETE
    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return []  # POST no requiere autenticación

    def get(self, request, *args, **kwargs):
        maestro = get_object_or_404(Maestros, id=request.GET.get("id"))
        maestro = MaestroSerializer(maestro, many=False).data
        # Si todo es correcto, regresamos la información
        return Response(maestro, 200)
    # Registrar maestros

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Serializamos los datos del maestro para volverlo de nuevo JSON
        user_data = UserSerializer(data=request.data)

        if user_data.is_valid():
            # guardamos los datos del maestro
            role = request.data['rol']
            first_name = request.data["first_name"]
            last_name = request.data["last_name"]
            email = request.data["email"]
            password = request.data["password"]
            # Valida si existe el usuario o bien el email registrado
            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                return Response({"message": f"El correo {email} ya está registrado."}, 400)

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
            # Almacenar los datos adicionales del maestro
            maestro = Maestros.objects.create(user=user,
                                              clave_maestros=request.data["clave_maestros"],
                                              telefono=request.data.get(
                                                  "telefono", ""),
                                              rfc=request.data.get(
                                                  "rfc", "").upper(),
                                              cubiculo=request.data.get(
                                                  "cubiculo", ""),
                                              area_investigacion=request.data.get(
                                                  "area_investigacion", ""),
                                              materias_json=request.data.get(
                                                  "materias_json", []),
                                              fecha_nacimiento=request.data.get(
                                                  "fecha_nacimiento", None),
                                              )
            maestro.save()

            return Response({"Maestro creado con el ID": maestro.id}, 201)

        return Response(user_data.errors, status=status.HTTP_400_BAD_REQUEST)


# Actualizar datos del administrador


    @transaction.atomic
    def put(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        # Primero obtenemos el administrador a actualizar
        maestro = get_object_or_404(Maestros, id=request.data["id"])

        maestro.clave_maestros = request.data["clave_maestros"]
        maestro.telefono = request.data["telefono"]
        maestro.rfc = request.data["rfc"].upper()
        maestro.cubiculo = request.data["cubiculo"]
        maestro.area_investigacion = request.data["area_investigacion"]
        maestro.materias_json = request.data["materias_json"]
        maestro.fecha_nacimiento = request.data["fecha_nacimiento"]
        maestro.save()

        # Actualizamos los datos del usuario asociado (tabla auth_user de Django)
        user = maestro.user
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()

        return Response({"message": "maestro actualizado correctamente", "maestro": MaestroSerializer(maestro).data}, 200)
        # return Response(user,200)

# Eliminar maestro con delete (Borrar realmente)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        maestro = get_object_or_404(Maestros, id=request.GET.get("id"))
        try:
            maestro.user.delete()
            return Response({"details": "Maestro eliminado"}, 200)
        except Exception as e:
            return Response({"details": "Algo pasó al eliminar"}, 400)
