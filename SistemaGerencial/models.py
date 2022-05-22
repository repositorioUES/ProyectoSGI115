from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    is_administador = models.BooleanField('Administrador', default=False)
    is_estrategico = models.BooleanField('Estrategico', default=False)
    is_tactico = models.BooleanField('Tactico', default=False)