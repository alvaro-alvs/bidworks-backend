from django.db import models
from api.models.usuario import Usuario

class SenhaUsuario(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    senha = models.BinaryField()
    last_otp = models.BinaryField(null=True, blank=True)
    
    
    
class TokenUsuario(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField(null=True, blank=True)