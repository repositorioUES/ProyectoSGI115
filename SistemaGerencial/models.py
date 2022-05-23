from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.
class User(AbstractUser):
    is_administador = models.BooleanField('Administrador', default=False)
    is_estrategico = models.BooleanField('Estrategico', default=False)
    is_tactico = models.BooleanField('Tactico', default=False)


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

#FIN CONSULTA

# Modelo de VACUNA -------------------------------------------------------------------
class Vacuna(models.Model):
    id = models.AutoField(primary_key = True)
    paciente = models.ForeignKey('Paciente', on_delete = models.PROTECT, null=True)
    fechaAplic = models.DateField(auto_now_add = True)# fecha de aplicada la vacuna
    nombreVac = models.CharField(max_length=100,null=False)
    
    def __str__(self):
        return self.nombreVac
#FIN VACUNA