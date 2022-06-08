import os
from ProyectoSIG import settings
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
from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.edit import View
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.core import management
from django.core.management.commands import loaddata, dumpdata


# Create your views here.

@login_required
def index(request):
    labels = []
    data = []

    clinicas = Clinica.objects.all()
    for c in clinicas:
        labels.append(c.nombreCli)

    consultorios = Consultorio.objects.values('clinica_id').annotate(Numero=Count('clinica_id'))
    for cons in consultorios:
        data.append(cons['Numero'])

    cli = Clinica.objects.all().count()
    con = Consultorio.objects.all().count()
    context = {
        'clinicas': cli,
        'consultorios': con,
        'labels': labels,
        'data': data,
    }
    return render(request, 'index.html', context)


def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()

            #bitacora(request.user, "Registro de usuario: " + formulario.username)

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
def registrarUsuario(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()

            bitacora(request.user, "Registro de usuario: " + formulario.cleaned_data['username'] + "(" + formulario.cleaned_data['first_name'] + " " + formulario.cleaned_data['last_name'] +")")

            messages.success(request, "Usuario registrado exitosamente")
            return redirect(to="listarUsuario")
        else:
            data["form"] = formulario
    return render(request, 'usuario/registrarUsuario.html', data)


def listarUsuario(request):
    usuarios = User.objects.all()
    data = {
        'usuarios': usuarios,
    }

    if request.user is not None and request.user.is_superuser == 1 or request.user.rol == 'administrador':

        #if usuarios:
            #bitacora(request.user, "Ver listado de usuarios")

        return render(request, 'usuario/listarUsuario.html', data)
    else:
        return render(request, 'usuario/401.html')


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

            if usuario:
                bitacora(request.user, "Modificación de usuario: " + usuario.username + " (" + usuario.first_name + " "+ usuario.last_name +")")

            messages.success(request, " Usuario actualizado correctamente")
            return redirect(to="listarUsuario")
        data['form'] = formulario
    return render(request, 'usuario/editarUsuario.html', data)


@login_required
def eliminarUsuario(request, id):
    usuario = get_object_or_404(User, id=id)

    if usuario:
        bitacora(request.user, "Eliminación de usuario: " + usuario.username)

    usuario.delete()
    messages.success(request, " Usuario eliminado correctamente")
    return redirect(to="listarUsuario")


# Salidas TACTICAS -------------------------------------------------------
@login_required
def pacientes_consultorio(request):
    fec = request.GET.get('buscarFecha')  # Filtro por fecha
    cli = request.GET.get('buscarClinica')  # Filtro por clinica

    clinicas = Clinica.objects.all()
    pacientes = Paciente.objects.all()

    context = {'clinicas': clinicas}

    if cli:
        if cli == '0':
            msj = 'Debe seleccionar la clínica primero'
            context = {'clinicas': clinicas, 'noClinica': msj}

        else:
            consultorios = Consultorio.objects.filter(clinica_id=cli).order_by('id')
            expedientes = Expediente.objects.filter(clinica_id=cli)

            cant = []
            for c in consultorios:
                i = 0
                z = {'obj': None, 'cant': None}
                for e in expedientes:
                    if e.consultorio_id == c.id:
                        i = i + 1
                z['obj'] = c
                z['cant'] = i
                cant.append(z)

            context = {'clinicas': clinicas, 'consultorios': consultorios, 'pacientes': pacientes, 'exp': expedientes,
                       'cliID': int(cli), 'cant': cant}

            bitacora(request.user, " Ver Pacientes por Consultorio")

    if request.user is not None and request.user.is_superuser == 1 or request.user.rol == 'administrador' or request.user.rol == 'tactico':
        return render(request, 'Salidas_Tacticas/pacientes_consultorio.html', context)
    else:
        return render(request, 'usuario/401.html')


@login_required
def pacientes_especie_consultorio(request):
    fec = request.GET.get('buscarFecha')  # Filtro por fecha
    cli = request.GET.get('buscarClinica')  # Filtro por clinica
    espec = request.GET.get('buscarEspecie')  # Filtro por especie

    clinicas = Clinica.objects.all()
    pacientes = Paciente.objects.all()

    especiesString = []
    especies = []
    for p in pacientes:
        if p.especie not in especiesString:
            especiesString.append(p.especie)
            especies.append(p)

    context = {'clinicas': clinicas, 'esp': especies}

    if cli and espec:
        if cli == '0' and espec != '0':
            msj = 'Debe seleccionar la clínica primero'
            context = {'clinicas': clinicas, 'esp': especies, 'noClinica': msj, 'espID': int(espec)}
        if cli != '0' and espec == '0':
            msj = 'Debe seleccionar la Especie'
            context = {'clinicas': clinicas, 'esp': especies, 'cliID': int(cli), 'noClinica': msj, 'espID': int(espec)}
        else:
            if cli != '0' and espec != '0':
                consultorios = Consultorio.objects.filter(clinica_id=cli).order_by('id')
                expedientes = Expediente.objects.filter(clinica_id=cli)
                espSeleccionada = Paciente.objects.get(id=espec)

                cant = []
                for c in consultorios:
                    i = 0
                    z = {'obj': None, 'cant': None}
                    for e in expedientes:
                        if e.consultorio_id == c.id:
                            if e.paciente.especie == espSeleccionada.especie:
                                i = i + 1
                    z['obj'] = c
                    z['cant'] = i
                    cant.append(z)

                context = {'clinicas': clinicas, 'consultorios': consultorios, 'pacientes': pacientes,
                           'exp': expedientes, 'esp': especies, 'espSel': espSeleccionada, 'cliID': int(cli),
                           'espID': int(espec), 'cant': cant}

                bitacora(request.user, " Ver Pacientes por Especie por Consultorio")

    if request.user is not None and request.user.is_superuser == 1 or request.user.rol == 'administrador' or request.user.rol == 'tactico':
        return render(request, 'Salidas_Tacticas/pacientes_especie_consultorio.html', context)
    else:
        return render(request, 'usuario/401.html')


# Salidas ESTRATEGICAS -------------------------------------------------------
@login_required
def consultas_consultorio(request):
    fec1 = request.GET.get('buscarFecha1')  # Filtro por fecha
    fec2 = request.GET.get('buscarFecha2')  # Filtro por fecha
    cli = request.GET.get('buscarClinica')  # Filtro por clinica

    clinicas = Clinica.objects.all()

    context = {'clinicas': clinicas}

    if (fec1 != "" or fec2 != "") and cli == '0':
        msj = 'Debe seleccionar la clínica primero'
        context = {'clinicas': clinicas, 'noClinica': msj}

    if cli:
        if cli != '0':
            if fec1 != "" and fec2 != "":
                formatted_date1 = time.strptime(fec1, "%Y-%m-%d")
                formatted_date2 = time.strptime(fec2, "%Y-%m-%d")
                if (formatted_date1 > formatted_date2):
                    msj = 'La fecha 1 debe ser Menor que la fecha 2'
                    context = {'clinicas': clinicas, 'noClinica': msj}
                else:
                    consultorios = Consultorio.objects.filter(clinica_id=cli).order_by('id')
                    consultas = Consulta.objects.filter(clinica_id=cli).filter(fechaConsulta__gt=fec1).filter(
                        fechaConsulta__lt=fec2).order_by('id')

                    cant = []

                    for c in consultorios:
                        i = 0
                        z = {'obj': None, 'cant': None}
                        for e in consultas:
                            if e.consultorio_id == c.id:
                                i = i + 1
                        z['obj'] = c
                        z['cant'] = i
                        cant.append(z)

                    context = {'clinicas': clinicas, 'consultorios': consultorios, 'consultas': consultas,
                               'cliID': int(cli), 'cant': cant}

                    bitacora(request.user, "Ver Consultas por Consultrio por rango de fecha")

            else:
                consultorios = Consultorio.objects.filter(clinica_id=cli)
                consultas = Consulta.objects.filter(clinica_id=cli)

                cant = []

                for c in consultorios:
                    i = 0
                    z = {'obj': None, 'cant': None}
                    for e in consultas:
                        if e.consultorio_id == c.id:
                            i = i + 1
                    z['obj'] = c
                    z['cant'] = i
                    cant.append(z)

                context = {'clinicas': clinicas, 'consultorios': consultorios, 'consultas': consultas,
                           'cliID': int(cli), 'cant': cant}

                bitacora(request.user, "Ver Consultas por Consultorio")

    if request.user is not None and request.user.is_superuser == 1 or request.user.rol == 'administrador' or request.user.rol == 'estrategico':
        return render(request, 'Salidas_Estrategicas/consulta_consultorio.html', context)
    else:
        return render(request, 'usuario/401.html')


@login_required
def vacunas_consultorio(request):
    fec1 = request.GET.get('buscarFecha1')  # Filtro por fecha
    fec2 = request.GET.get('buscarFecha2')  # Filtro por fecha
    cli = request.GET.get('buscarClinica')  # Filtro por clinica
    cantidad = request.GET.get('buscarCantidad')  # Filtro por cantidad

    clinicas = Clinica.objects.all()
    vacunas = Vacuna.objects.none()

    context = {'clinicas': clinicas}

    if (fec1 != "" or fec2 != "") and cli == '0':
        msj = 'Debe seleccionar la clínica primero'
        context = {'clinicas': clinicas, 'noClinica': msj}

    if cli:
        if cli != '0':
            if fec1 != "" and fec2 != "":
                formatted_date1 = time.strptime(fec1, "%Y-%m-%d")
                formatted_date2 = time.strptime(fec2, "%Y-%m-%d")
                if (formatted_date1 > formatted_date2):
                    msj = 'La fecha 1 debe ser Menor que la fecha 2'
                    context = {'clinicas': clinicas, 'noClinica': msj}
                else:
                    if cantidad == '0':
                        consultorios = Consultorio.objects.filter(clinica_id=cli).order_by('id')

                        for c in consultorios:
                            vacunas |= Vacuna.objects.filter(consultorio_id=c.id).filter(fechaAplic__gt=fec1).filter(
                                fechaAplic__lt=fec2).order_by('consultorio_id')

                        nombres = []  # Guardamos los nombres de las vacunas para contar cuantas son c/u
                        for vacuna in vacunas:
                            if vacuna.nombreVac not in nombres:
                                nombres.append(vacuna.nombreVac)

                        res = []
                        for c in consultorios:
                            for no in nombres:
                                vac = Vacuna.objects.filter(consultorio_id=c.id).filter(nombreVac=no).filter(
                                    fechaAplic__gt=fec1).filter(fechaAplic__lt=fec2).count()
                                va = Vacuna.objects.filter(nombreVac=no).first()

                                if int(vac) != 0:
                                    r = {'cID': c.id, 'obj': va, 'cant': vac}
                                    res.append(r)

                        context = {'clinicas': clinicas, 'consultorios': consultorios, 'vacunas': vacunas,
                                   'cliID': int(cli), 'conteo': res}

                        bitacora(request.user, "Vacunas por Consultorio por rango de fecha")
            else:
                if cantidad == '0':
                    consultorios = Consultorio.objects.filter(clinica_id=cli).order_by('id')

                    for c in consultorios:
                        vacunas |= Vacuna.objects.filter(consultorio_id=c.id).order_by('consultorio_id')

                    nombres = []  # Guardamos los nombres de las vacunas para contar cuantas son c/u
                    for vacuna in vacunas:
                        if vacuna.nombreVac not in nombres:
                            nombres.append(vacuna.nombreVac)

                    res = []
                    for c in consultorios:
                        for no in nombres:
                            vac = Vacuna.objects.filter(consultorio_id=c.id).filter(nombreVac=no).count()
                            va = Vacuna.objects.filter(nombreVac=no).first()

                            if int(vac) != 0:
                                r = {'cID': c.id, 'obj': va, 'cant': vac}
                                res.append(r)

                    context = {'clinicas': clinicas, 'consultorios': consultorios, 'vacunas': vacunas,
                               'cliID': int(cli), 'conteo': res}

                    bitacora(request.user, "Vacunas por Consultorio")

    if request.user is not None and request.user.is_superuser == 1 or request.user.rol == 'administrador' or request.user.rol == 'estrategico':
        return render(request, 'Salidas_Estrategicas/vacunas_consultorio.html', context)
    else:
        return render(request, 'usuario/401.html')


@login_required
def vacunas_populares_consultorio(request):
    fec1 = request.GET.get('buscarFecha1')  # Filtro por fecha
    fec2 = request.GET.get('buscarFecha2')  # Filtro por fecha
    cli = request.GET.get('buscarClinica')  # Filtro por clinica
    cantidad = request.GET.get('buscarCantidad')  # Filtro por cantidad

    clinicas = Clinica.objects.all()
    vacunas = Vacuna.objects.none()

    context = {'clinicas': clinicas}

    if (fec1 != "" or fec2 != "") and cli == '0':
        msj = 'Debe seleccionar la clínica primero'
        context = {'clinicas': clinicas, 'noClinica': msj}

    if cli:
        if cli != '0':
            if fec1 != "" and fec2 != "":
                formatted_date1 = time.strptime(fec1, "%Y-%m-%d")
                formatted_date2 = time.strptime(fec2, "%Y-%m-%d")
                if (formatted_date1 > formatted_date2):
                    msj = 'La fecha 1 debe ser Menor que la fecha 2'
                    context = {'clinicas': clinicas, 'noClinica': msj}
                else:
                    if cantidad == '1':
                        consultorios = Consultorio.objects.filter(clinica_id=cli).order_by('id')

                        res = []
                        for c in consultorios:
                            vacunas = Vacuna.objects.filter(consultorio_id=c.id).filter(fechaAplic__gt=fec1).filter(
                                fechaAplic__lt=fec2).order_by('consultorio_id')

                            nombres = []  # Guardar nombres de las vacunas de este consultorio
                            for v in vacunas:
                                nombres.append(v.nombreVac)
                            # buscar el nombre que mas se repite
                            if len(nombres) > 0:
                                popular = max(set(nombres), key=nombres.count)
                                # contar cuantas vacunas cumplen con el nombre popular y que sean de este consultorio
                                vac = Vacuna.objects.filter(consultorio_id=c.id).filter(nombreVac=popular).count()
                                # Count solo devuelve la cantdidad (int) para tener los datos de la vacuna tomamos una cualquiera
                                va = Vacuna.objects.filter(nombreVac=popular).first()

                                if int(vac) != 0:
                                    r = {'cID': c.id, 'obj': va, 'cant': vac}
                                    res.append(r)

                        context = {'clinicas': clinicas, 'consultorios': consultorios, 'vacunas': vacunas,
                                   'cliID': int(cli), 'conteo': res}

                        bitacora(request.user, "Vacunas más aplicadas por rango de fecha")
            else:
                if cantidad == '1':
                    consultorios = Consultorio.objects.filter(clinica_id=cli).order_by('id')

                    res = []
                    for c in consultorios:
                        vacunas = Vacuna.objects.filter(consultorio_id=c.id).order_by('consultorio_id')

                        nombres = []  # Guardar nombres de las vacunas de este consultorio
                        for v in vacunas:
                            nombres.append(v.nombreVac)
                        # buscar el nombre que mas se repite
                        if len(nombres) > 0:
                            popular = max(set(nombres), key=nombres.count)
                            # contar cuantas vacunas cumplen con el nombre popular y que sean de este consultorio
                            vac = Vacuna.objects.filter(consultorio_id=c.id).filter(nombreVac=popular).count()
                            # Count solo devuelve la cantdidad (int) para tener los datos de la vacuna tomamos una cualquiera
                            va = Vacuna.objects.filter(nombreVac=popular).first()

                            if int(vac) != 0:
                                r = {'cID': c.id, 'obj': va, 'cant': vac}
                                res.append(r)

                    context = {'clinicas': clinicas, 'consultorios': consultorios, 'vacunas': vacunas,
                               'cliID': int(cli), 'conteo': res}

                    bitacora(request.user, "Vacunas más aplicadas")

    if request.user is not None and request.user.is_superuser == 1 or request.user.rol == 'administrador' or request.user.rol == 'estrategico':
        return render(request, 'Salidas_Estrategicas/vacunas_populares_consultorio.html', context)
    else:
        return render(request, 'usuario/401.html')


def bitacora(usuario, accion):
    bitacora = Bitacora()

    bitacora.usuario = usuario
    bitacora.accion = accion

    bitacora.save()

    return 0


def listado_bitacora(request):
    fec1 = request.GET.get('buscarFecha1')  # Filtro por fecha
    fec2 = request.GET.get('buscarFecha2')  # Filtro por fecha

    context = {}

    if (fec1 == "" and fec2 == "") or (fec1 == None and fec2 == None):
        bitacoras = Bitacora.objects.all().order_by('-fecha')
        context = {'bitacoras': bitacoras}
    else:
        if (fec1 == "" and fec2 != "") or (fec1 != "" and fec2 == ""):
            msj = 'Debe proporcionar ambas fechas para buscar por rango'
            context = {'msj': msj}
            print(fec1, fec2, "falta 1")

        if fec1 != "" and fec2 != "":
            if (fec1 != "" and fec1 != None):
                formatted_date1 = time.strptime(fec1, "%Y-%m-%d")
            if (fec2 != "" and fec2 != None):
                formatted_date2 = time.strptime(fec2, "%Y-%m-%d")

            if (formatted_date1 > formatted_date2):
                msj = 'La fecha 1 debe ser Menor que la fecha 2'
                context = {'msj': msj}
                print(fec1, fec2, "vienen las 2")
            else:
                bitacoras = Bitacora.objects.filter(fecha__gt=fec1).filter(fecha__lt=fec2).order_by('-fecha')
                context = {'bitacoras': bitacoras}
                print(fec1, fec2)



    if request.user is not None and request.user.is_superuser == 1 or request.user.rol == 'administrador':
        return render(request, 'listado_bitacora.html', context)
    else:
        return render(request, 'usuario/401.html')


class reporteUsuarios(LoginRequiredMixin,View):

    def link_callback(self, uri, rel):

        # use short variable names
        sUrl = settings.STATIC_URL
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))

        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:

            usuarios = User.objects.all()
            generado = datetime.now()

            template = get_template('reportes/reporteUsuarios.html')
            context = {
                'usuarios': usuarios,
                'generado': generado,
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            bitacora(request.user, "Generó reporte de Usuarios")
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('listarUsuario'))

class reporteBitacora(LoginRequiredMixin,View):

    def link_callback(self, uri, rel):

        # use short variable names
        sUrl = settings.STATIC_URL
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))

        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:

            bitacoras = Bitacora.objects.all().order_by('-fecha')
            generado = datetime.now()

            template = get_template('reportes/reporteBitacora.html')
            context = {
                'bitacoras': bitacoras,
                'generado': generado,
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            bitacora(request.user, "Generó reporte de Bitacora")
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('listarUsuario'))

class reportePacientesConsultorio(LoginRequiredMixin,View):

    def link_callback(self, uri, rel):

        # use short variable names
        sUrl = settings.STATIC_URL
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))

        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            generado = datetime.now()

            template = get_template('reportes/reportePacientesConsultorio.html')
            context = {
                'generado': generado,
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            bitacora(request.user, "Generó reporte Pacientes-Consultorio")
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('pacientes_consultorio'))

class reportePacientesEspecie(LoginRequiredMixin,View):

    def link_callback(self, uri, rel):

        # use short variable names
        sUrl = settings.STATIC_URL
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))

        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:

            template = get_template('reportes/reportePacientesEspecie.html')
            context = {

            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('pacientes_especie_consultorio'))

class reporteConsultasConsultorio(LoginRequiredMixin,View):

    def link_callback(self, uri, rel):

        # use short variable names
        sUrl = settings.STATIC_URL
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))

        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            generado = datetime.now()
            template = get_template('reportes/reporteConsultasConsultorio.html')
            context = {
                'generado': generado,
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            bitacora(request.user, "Generó reporte Consultas-Consultorios")
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('consultas_consultorio'))

class reporteVacunasConsultorio(LoginRequiredMixin,View):

    def link_callback(self, uri, rel):

        # use short variable names
        sUrl = settings.STATIC_URL
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))

        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:

            template = get_template('reportes/reporteVacunasConsultorio.html')
            context = {

            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('vacunas_consultorio'))

class reporteVacunasMasAplicadas(LoginRequiredMixin,View):

    def link_callback(self, uri, rel):

        # use short variable names
        sUrl = settings.STATIC_URL
        mUrl = settings.MEDIA_URL
        mRoot = settings.MEDIA_ROOT

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))

        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:

            template = get_template('reportes/reporteVacunasMasAplicadas.html')
            context = {

            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

            # create a pdf
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('vacunas_populares_consultorio'))

@login_required()
def respaldo_restauracion(request):
    if request.user is not None and request.user.is_superuser == 1 or request.user.rol == 'administrador':
        return render(request, 'Respaldo_Restauracion/respaldo_restauracion.html')
    else:
        return render(request, 'usuario/401.html')

@login_required()
def respaldo(request):
    if request.user is not None and request.user.is_superuser == 1 or request.user.rol == 'administrador':
        backup = management.call_command('dumpdatautf8', output='respaldo.json', indent=2, format='json', exclude=['auth', 'contenttypes', 'sessions'])
        bitacora(request.user, "Generó respaldo de la Base de Datos")
        return render(request, 'Respaldo_Restauracion/respaldo.html', {"backup": backup})
    else:
        return render(request, 'usuario/401.html')

@login_required()
def restauracion(request):
    if request.user is not None and request.user.is_superuser == 1 or request.user.rol == 'administrador':
        restore = management.call_command('loaddata', 'respaldo.json')
        bitacora(request.user, "Restauró la Base de Datos")
        return render(request, 'Respaldo_Restauracion/restauracion.html', {"restore": restore})
    else:
        return render(request, 'usuario/401.html')
