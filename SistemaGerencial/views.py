from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
# Create your views here.
from SistemaGerencial.forms import CustomUserCreationForm
from SistemaGerencial.models import *
from SistemaGerencial.forms import *
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

#Saldas TACTICAS -------------------------------------------------------
def pacientes_consultorio(request):
    fec = request.GET.get('buscarFecha') # Filtro por fecha
    cli = request.GET.get('buscarClinica') # Filtro por clinica
    espec = request.GET.get('buscarEspecie') # Filtro por especie

    clinicas = Clinica.objects.all()
    pacientes = Paciente.objects.all()

    especiesString = []
    especies = []
    for p in pacientes:
        if p.especie not in especiesString:
            especiesString.append(p.especie)
            especies.append(p)

    context ={'clinicas':clinicas, 'especies':especies}

    if cli and espec:
        if cli == '0' and espec != '0':
            msj = 'Debe seleccionar la clínica primero'
            context ={'clinicas':clinicas, 'esp':especies, 'noClinica':msj, 'espID': int(espec)}
            print(especies)
        else:
            if cli != '0' and espec == '0':
                consultorios = Consultorio.objects.filter(clinica_id = cli)
                expedientes = Expediente.objects.filter(clinica_id = cli)

                context ={'clinicas':clinicas, 'consultorios':consultorios, 'pacientes':pacientes, 'exp':expedientes,'esp':especies, 'cliID': int(cli)}
            else:
                if cli != '0' and espec != '0':
                    consultorios = Consultorio.objects.filter(clinica_id = cli)
                    expedientes = Expediente.objects.filter(clinica_id = cli)
                    espSeleccionada = Paciente.objects.get(id = espec)

                    context ={'clinicas':clinicas, 'consultorios':consultorios, 'pacientes':pacientes, 'exp':expedientes,'esp':especies, 'espSel':espSeleccionada, 'cliID': int(cli), 'espID': int(espec)}
    return render(request, 'Salidas_Tacticas/pacientes_consultorio.html', context)

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



