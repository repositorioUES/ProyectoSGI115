from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
# Create your views here.
from SistemaGerencial.forms import CustomUserCreationForm
from SistemaGerencial.models import User


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
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Registro exitoso")
            return redirect(to="index")
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)

def listarUsuario(request):
    usuarios = User.objects.all()
    data = {
        'usuarios': usuarios,
    }

    if request.user is not None and request.user.rol != 'administrador':
        return render(request, 'usuario/401.html')
    else:
        return render(request, 'usuario/listarUsuario.html', data)


