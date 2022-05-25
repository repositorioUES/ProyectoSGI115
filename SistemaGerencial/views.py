from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from SistemaGerencial.models import *
from SistemaGerencial.forms import *
from SistemaGerencial.forms import CustomUserCreationForm, CustomUserEditForm
from SistemaGerencial.models import User
import time
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

#Salidas TACTICAS -------------------------------------------------------
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
          
        else:
            if cli != '0' and espec == '0':
                consultorios = Consultorio.objects.filter(clinica_id = cli).order_by('id')
                expedientes = Expediente.objects.filter(clinica_id = cli)

                cant = []
                
                for c in consultorios:
                    i = 0
                    z = {'obj':None, 'cant':None}
                    for e in expedientes:
                        if e.consultorio_id == c.id:
                            i = i + 1
                    z['obj'] = c
                    z['cant'] = i
                    cant.append(z)
             
                context ={'clinicas':clinicas, 'consultorios':consultorios, 'pacientes':pacientes, 'exp':expedientes,'esp':especies, 'cliID': int(cli), 'cant':cant}
            else:
                if cli != '0' and espec != '0':
                    consultorios = Consultorio.objects.filter(clinica_id = cli).order_by('id')
                    expedientes = Expediente.objects.filter(clinica_id = cli)
                    espSeleccionada = Paciente.objects.get(id = espec)
                   
                    cant = []
                
                    for c in consultorios:
                        i = 0
                        z = {'obj':None, 'cant':None}
                        for e in expedientes:
                            if e.consultorio_id == c.id:
                                if e.paciente.especie == espSeleccionada.especie:
                                    i = i + 1
                        z['obj'] = c
                        z['cant'] = i
                        cant.append(z)
                
                    context ={'clinicas':clinicas, 'consultorios':consultorios, 'pacientes':pacientes, 'exp':expedientes,'esp':especies, 'espSel':espSeleccionada, 'cliID': int(cli), 'espID': int(espec),'cant':cant}
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

#Salidas ESTRATEGICAS -------------------------------------------------------
def consultas_consultorio(request):
    fec1 = request.GET.get('buscarFecha1') # Filtro por fecha
    fec2 = request.GET.get('buscarFecha2') # Filtro por fecha
    cli = request.GET.get('buscarClinica') # Filtro por clinica

    clinicas = Clinica.objects.all()

    context ={'clinicas':clinicas}
    
    if (fec1 != "" or fec2 != "") and cli == '0':
        msj = 'Debe seleccionar la clínica primero'
        context ={'clinicas':clinicas, 'noClinica':msj} 

    if cli:
        if cli != '0':
            if fec1 != "" and fec2 != "":
                formatted_date1 = time.strptime(fec1, "%Y-%m-%d")
                formatted_date2 = time.strptime(fec2, "%Y-%m-%d")
                if(formatted_date1 > formatted_date2):
                    msj = 'La fecha 1 debe ser Menor que la fecha 2'
                    context ={'clinicas':clinicas, 'noClinica':msj}
                else:
                    consultorios = Consultorio.objects.filter(clinica_id = cli).order_by('id')
                    consultas = Consulta.objects.filter(clinica_id=cli).filter(fechaConsulta__gt = fec1).filter(fechaConsulta__lt = fec2).order_by('id')

                    cant = []
                    
                    for c in consultorios:
                        i = 0
                        z = {'obj':None, 'cant':None}
                        for e in consultas:
                            if e.consultorio_id == c.id:
                                i = i + 1
                        z['obj'] = c
                        z['cant'] = i
                        cant.append(z)
                        
                    context ={'clinicas':clinicas, 'consultorios':consultorios, 'consultas':consultas, 'cliID': int(cli),'cant':cant}
                    
            else:
                consultorios = Consultorio.objects.filter(clinica_id = cli)
                consultas = Consulta.objects.filter(clinica_id = cli)
    
                cant = []
                    
                for c in consultorios:
                    i = 0
                    z = {'obj':None, 'cant':None}
                    for e in consultas:
                        if e.consultorio_id == c.id:
                            i = i + 1
                    z['obj'] = c
                    z['cant'] = i
                    cant.append(z)

                context ={'clinicas':clinicas, 'consultorios':consultorios, 'consultas':consultas, 'cliID': int(cli),'cant':cant}

    return render(request, 'Salidas_Estrategicas/consulta_consultorio.html', context)

def vacunas_consultorio(request):
    #fec = request.GET.get('buscarFecha') # Filtro por fecha
    cli = request.GET.get('buscarClinica') # Filtro por clinica
    cantidad = request.GET.get('buscarCantidad') # Filtro por cantidad

    clinicas = Clinica.objects.all()
    vacunas = Vacuna.objects.none()

    context ={'clinicas':clinicas}
            
    if cli:
        if cli != '0':
            consultorios = Consultorio.objects.filter(clinica_id = cli)
            expedientes = Expediente.objects.filter(clinica_id = cli)

            pacID = []
            for e in expedientes:
                if e.paciente_id not in pacID:
                    pacID.append(e.paciente_id)
                    
            for p in pacID:
                vacunas |= Vacuna.objects.filter(paciente_id = p).distinct()

            if cantidad == '1':
                vacNom = []
                for v in vacunas:
                    vacNom.append(v.nombreVac)
                
                vacPopular = max(set(vacNom), key = vacNom.count)
                context ={'clinicas':clinicas, 'consultorios':consultorios, 'exp':expedientes, 'vacunas':vacunas, 'vacPopular':vacPopular,'cliID': int(cli), 'cant': int(cantidad)}
       
            context ={'clinicas':clinicas, 'consultorios':consultorios, 'exp':expedientes, 'vacunas':vacunas,'cliID': int(cli)}
            
    return render(request, 'Salidas_Estrategicas/vacunas_consultorio.html', context)
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



