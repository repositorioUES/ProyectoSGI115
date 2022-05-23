from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    ROL = (('administrador','Administrador'),('estrategico', 'Estrategico'), ('tactico', 'Tactico'))
    rol = models.CharField(max_length=20, choices=ROL, blank=True, help_text='')