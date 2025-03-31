from django.db import models
from api.models.usuario import Usuario

class SenhaUsuario(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    senha = models.BinaryField()
    last_otp = models.BinaryField(null=True, blank=True)