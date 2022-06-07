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
    path('reporte_Usuarios/', reporteUsuarios.as_view(), name="reporte_Usuarios"),
    path('reporte_Bitacora/', reporteBitacora.as_view(), name="reporte_Bitacora"),
    path('reporte_PacientesConsultorio/', reportePacientesConsultorio.as_view(), name="reporte_PacientesConsultorio"),
    path('reporte_PacientesEspecie/', reportePacientesEspecie.as_view(), name="reporte_PacientesEspecie"),
    path('reporte_ConsultasConsultorio/', reporteConsultasConsultorio.as_view(), name="reporte_ConsultasConsultorio"),
    path('reporte_VacunasConsultorio/', reporteVacunasConsultorio.as_view(), name="reporte_VacunasConsultorio"),
    path('reporte_VacunasMasAplicadas/', reporteVacunasMasAplicadas.as_view(), name="reporte_VacunasMasAplicadas"),
    path('respaldo_restauracion/', respaldo_restauracion, name="respaldo_restauracion"),
    path('respaldo/', respaldo, name="respaldo"),
    path('restauracion/', restauracion, name="restauracion"),

]
