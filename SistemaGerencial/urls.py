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

]