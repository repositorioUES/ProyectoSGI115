from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from SistemaGerencial.forms import CustomUserCreationForm, CustomUserEditForm
from SistemaGerencial.models import User
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

@login_required
def index(request):
    return render(request, 'index.html')

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"],
                                password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Registro exitoso")
            return redirect(to="index")
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)

class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'usuario/cambiarContra.html'
    success_message = "Contraseña actualizada"
    success_url = reverse_lazy('index')

@login_required
def listarUsuario(request):
    usuarios = User.objects.all()
    data = {
        'usuarios': usuarios,
    }

    if request.user is not None and request.user.rol != 'administrador':
        return render(request, 'usuario/401.html')
    else:
        return render(request, 'usuario/listarUsuario.html', data)

@login_required
def registrarUsuario(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Usuario registrado exitosamente")
            return redirect(to="listarUsuario")
        else:
            data["form"] = formulario
    return render(request, 'usuario/registrarUsuario.html', data)

@login_required
def editarUsuario(request, id):
    usuario = get_object_or_404(User, id=id)
    data = {
        'form': CustomUserEditForm(instance=usuario)
    }

    if request.method == 'POST':
        formulario = CustomUserEditForm(data=request.POST, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request," Usuario actualizado correctamente")
            return redirect(to="listarUsuario")
        data['form'] = formulario
    return render(request, 'usuario/editarUsuario.html', data)

@login_required
def eliminarUsuario(request, id):
    usuario = get_object_or_404(User, id=id)
    usuario.delete()
    messages.success(request, " Usuario eliminado correctamente")
    return redirect(to="listarUsuario")



