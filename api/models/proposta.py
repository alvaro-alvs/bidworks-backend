from django.db import models
from api.models.usuario import Cliente

#* Modelo de PROPOSTA
class Freela(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    tags = models.JSONField(null=True, blank=True)
    description = models.TextField()