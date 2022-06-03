from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('registro/', registro, name="registro"),
    path('password-change/', ChangePasswordView.as_view(), name='cambiarContra'),
    path('usuario/listarUsuario', listarUsuario, name="listarUsuario"),
    path('usuario/registrarUsuario', registrarUsuario, name="registrarUsuario"),
    path('usuario/editarUsuario/<id>/', editarUsuario, name="editarUsuario"),
    path('usuario/eliminarUsuario/<id>/', eliminarUsuario, name="eliminarUsuario"),
    path('pacientes_consultorio/', pacientes_consultorio, name="pacientes_consultorio"),
    path('pacientes_especie_consultorio/', pacientes_especie_consultorio, name="pacientes_especie_consultorio"),
    path('consultas_consultorio/', consultas_consultorio, name="consultas_consultorio"),
    path('vacunas_consultorio/', vacunas_consultorio, name="vacunas_consultorio"),
    path('vacunas_populares_consultorio/', vacunas_populares_consultorio, name="vacunas_populares_consultorio"),
    path('listado_bitacora/', listado_bitacora, name="listado_bitacora"),
]