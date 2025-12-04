from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404
from control_escolar_api.models import Materias, Maestros
from control_escolar_api.serializers import UserSerializer
from control_escolar_api.serializers import MateriaSerializer
import json


class MateriasAll(generics.CreateAPIView):
    # Esta función es esencial para todo donde se requiera autorización de inicio de sesión (token)
    permission_classes = (permissions.IsAuthenticated,)

    # Invocamos la petición GET para obtener todas las materias
    def get(self, request, *args, **kwargs):
        materias = Materias.objects.all().order_by("id")
        lista = MateriaSerializer(materias, many=True).data
        for materia in lista:
            if isinstance(materia, dict) and "dias" in materia:
                try:
                    # Si dias viene como string JSON lo convertimos a lista
                    if isinstance(materia["dias"], str):
                        materia["dias"] = json.loads(materia["dias"])
                except Exception as e:
                    print(
                        f"Error procesando días para materia {materia.get('id')}: {e}")
                    materia["dias"] = []

        return Response(lista, 200)


class MateriaView(generics.CreateAPIView):

    # Permisos por método (sobrescribe el comportamiento default)
    # GET, PUT, DELETE requieren autenticación.
    def get_permissions(self):
        if self.request.method in ['GET', 'PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return []  # POST no requiere autenticación

    # Obtener materia por ID
    def get(self, request, *args, **kwargs):
        materia = get_object_or_404(Materias, id=request.GET.get("id"))
        materia = MateriaSerializer(materia, many=False).data
        # Si todo es correcto, regresamos la información
        return Response(materia, 200)
    # Registrar materias

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = MateriaSerializer(data=request.data)

        if serializer.is_valid():
            # guardamos los datos de la materia
            profesor_id = request.data.get("profesor_asignado")
            profesor = get_object_or_404(Maestros, id=profesor_id)
            materia = Materias.objects.create(
                nrc=request.data["nrc"],
                nombre_materia=request.data["nombre_materia"],
                seccion=request.data["seccion"],
                dias=request.data.get("dias", []),
                hora_inicio=request.data["hora_inicio"],
                hora_final=request.data["hora_final"],
                salon=request.data["salon"],
                programa_educativo=request.data["programa_educativo"],
                profesor_asignado=profesor,
                creditos=request.data["creditos"]
            )
            materia.save()
            return Response({"Materia creada con el ID": materia.id}, 201)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # actualizar materia

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        permission_classes = (permissions.IsAuthenticated,)
        materia = get_object_or_404(Materias, id=request.data["id"])

        materia.nrc = request.data["nrc"]
        materia.nombre_materia = request.data["nombre_materia"]
        materia.seccion = request.data["seccion"]
        materia.dias = request.data.get("dias", [])
        materia.hora_inicio = request.data["hora_inicio"]
        materia.hora_final = request.data["hora_final"]
        materia.salon = request.data["salon"]
        materia.programa_educativo = request.data["programa_educativo"]
        materia.creditos = request.data["creditos"]
        # Validar y actualizar profesor asignado
        profesor_id = request.data.get("profesor_asignado")
        if profesor_id:
            profesor = get_object_or_404(Maestros, id=profesor_id)
            materia.profesor_asignado = profesor

        materia.save()

        return Response({
            "message": "Materia actualizada correctamente",
            "materia": MateriaSerializer(materia).data
        }, 200)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        materia = get_object_or_404(Materias, id=request.GET.get("id"))
        try:
            materia.delete()
            return Response({"details": "Materia eliminada correctamente"}, 200)
        except Exception as e:
            print(f"Error al eliminar materia: {str(e)}")
            return Response({"details": "Error al eliminar la materia"}, 400)
