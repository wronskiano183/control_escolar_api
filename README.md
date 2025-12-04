
README Repositorio Backend (Django Rest Framework)

Este repositorio contiene el backend del Sistema de Gestión Académica, que sirve como la capa de datos para el frontend de Angular.

Tecnologías Utilizadas
Framework: Django

API: Django 

Base de Datos: MySQL

Autenticación: Gestión de tokens de sesión y permisos por rol.



Endpoints y Seguridad

Se implementan Vistas de API optimizadas que manejan las operaciones CRUD:

Vistas (MateriasAll, MateriaView): Controlan el flujo de datos.

Serializers: Aseguran la conversión y validación de datos entre Python y JSON, estandarizando formatos de tiempo (HH:MM).

Seguridad: Uso de Transacciones Atómicas (@transaction.atomic) para garantizar que las operaciones de creación y actualización sean seguras y consistentes.

Permisos: Se aplican permisos de autenticación (IsAuthenticated) a la mayoría de los endpoints para proteger los datos.