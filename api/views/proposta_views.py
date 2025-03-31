
#* Freela representa o modelo de uma proposta
from api.models.proposta import Freela


def ListarPropostas(request):
    propostas = Freela.objects.all()
    
    return propostas

def ListarPropostasUsuario(request, id): #* recebe o ID do Usuario
    propostas = Freela.objects.filter(cliente=id)
    
    return propostas

def GetProposta(request, id):
    proposta = Freela.objects.get(id=id)
    
    return proposta
    
    
    
# sddds tipagem forte :,(