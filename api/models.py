from django.db import models

#* Modelos -> user, Freela, worker _> definir modelos adjacentes baseados no diagrama
class Usuario(models.Model):
    #* definir campos
    #* definir relações
    nome = models.CharField(max_length=100) #* por padrão é NOT_NULL
    email = models.CharField(max_length=100, null=True, blank=True) #* definido como NULL || #* verificar se pode ser nulo
    isActive = models.BooleanField(default=True)

class Credentials(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    password = models.BinaryField()
    last_otp = models.BinaryField(null=True, blank=True)



#* Abstract Users
class Cliente(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    

class Dev(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)


#* regra de negocio
class Prop(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    tags = models.JSONField(null=True, blank=True)
    description = models.TextField()
