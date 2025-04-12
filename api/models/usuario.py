from django.db import models



#* Modelo de usuario -> herda para Dev e Cliente
class Usuario(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True) #* este campo é unico
    telefone = models.CharField(max_length=15, null=True, blank=True) #* este campo é unico (deveria?) acho que sim
    dn = models.DateField(null=True, blank=True) #* data de nascimento
    foto = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


#* Modelo do Cliente -> por postar propostas
class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='cliente_profile')
    abrev = models.CharField(max_length=10, null=True, blank=True)
    # propostas_pagas = models.IntegerField(null=True, blank=True) #* quantidade de propostas pagas / bem-sucedidas
    rate = models.FloatField(null=True, blank=True) #* adicionado campo de avaliação para o cliente também
    
    #* As propostas do cliente são listadas no arquivo de propostas


#* Modelo do Dev / Worker / Freelancer
class Dev(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='dev_profile')
    texto_bio = models.TextField(null=True, blank=True)
    rate = models.FloatField(null=True, blank=True) #* media de avaliacao
    stack = models.JSONField( #* tecnologias do dev
        null=True, 
        blank=True, 
        choices=[
            ("frontend", "frontend"), 
            ("backend", "backend"), 
            ("devops", "devops"), 
            ("data", "data"), 
            ("mobile", "mobile")
        ]
    )
