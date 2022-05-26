from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.
class User(AbstractUser):
    ROL = (('administrador','Administrador'),('estrategico', 'Estrategico'), ('tactico', 'Tactico'))
    rol = models.CharField(max_length=20, choices=ROL, blank=True, help_text='')


# Modelo del PACIENTE -------------------------------------------------------------------
class Paciente(models.Model):
    id = models.AutoField(primary_key=True)
    nombrePac = models.CharField(max_length=50,help_text="")
    especie = models.CharField(max_length=50, help_text="")
    fechaInscrip = models.DateField(auto_now_add = True)# fecha de inscripcion del paciente
    
    def __str__(self): #Para que retorne el nombre y no el Id
        return self.nombrePac
#FIN PACIENTE

# Modelo de CLINICA -------------------------------------------------------------------
class Clinica(models.Model):
    id = models.AutoField(primary_key = True)
    propietario = models.CharField(max_length=50)
    nombreCli = models.CharField(max_length=60)

    def __str__(self):
        return self.nombreCli
#FIN CLINICA

# Modelo de CONSULTORIO -------------------------------------------------------------------
class Consultorio(models.Model):
    id = models.AutoField(primary_key = True)
    clinica = models.ForeignKey('Clinica', on_delete = models.CASCADE)
    nombreCons = models.CharField(max_length=60)

    def __str__(self):
        return self.nombreCons
#FIN CONSULTORIO

# Modelo de CONSULTA -------------------------------------------------------------------
class Consulta (models.Model):
    id = models.AutoField(primary_key = True)
    paciente = models.ForeignKey('Paciente', on_delete = models.PROTECT, null=True)
    fechaConsulta = models.DateField(auto_now_add = True)# fecha de creación de la consulta
    clinica = models.ForeignKey('Clinica', on_delete = models.PROTECT)
    consultorio = models.ForeignKey('Consultorio', on_delete = models.PROTECT)
    hora = models.CharField(max_length=100,null=False)
    medico = models.CharField(max_length=100,null=False)

#FIN CONSULTA

# Modelo de VACUNA -------------------------------------------------------------------
class Vacuna(models.Model):
    id = models.AutoField(primary_key = True)
    paciente = models.ForeignKey('Paciente', on_delete = models.PROTECT, null=True)
    consultorio = models.ForeignKey('Consultorio', on_delete = models.PROTECT)
    fechaAplic = models.DateField(auto_now_add = True)# fecha de aplicada la vacuna
    nombreVac = models.CharField(max_length=100,null=False)
    
    def __str__(self):
        return self.nombreVac
#FIN VACUNA

# Modelo de EXPEDIENTE -------------------------------------------------------------------
class Expediente (models.Model):
    id = models.AutoField(primary_key = True)
    paciente = models.ForeignKey('Paciente', on_delete = models.PROTECT, null=True)
    clinica = models.ForeignKey('Clinica', on_delete = models.PROTECT)
    consultorio = models.ForeignKey('Consultorio', on_delete = models.PROTECT)
    
    def __str__(self):
        i = str(id)
        return i
#FIN CONSULTA