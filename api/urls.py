from django.urls import path
from api.views.default_views import HealthCheck
from api.views.usuario_views import NovoUsuario, LoginUsuario, GetUsuario
from api.views.proposta_views import ListarPropostas, GetProposta, ListarPropostasUsuario

#! POUCA COISA AQUI FOI TESTADA, 
#! SE VIR ALGUMA MENGAGEM DE ERRO, JA CORRIJA POE GENTILEZA

cliente_urls = [
    # definir
]

dev_urls = [
    # difinir
]

#* Urls de propostas
propostas_urls = [
    path('listar-propostas/', ListarPropostas, name='listar-propostas'),                #* listar todas as propostas
    path('propostas-usuario/<int:id>/', ListarPropostasUsuario, name='obter-proposta'), #* recebe o id de uma proposta
    path('proposta/<int:id>/', GetProposta, name='obter-proposta'),                     #* recebe o id de uma proposta
]

#* Urls do usuario
usuario_urls = [
    path('usuario/<int:id>/', GetUsuario),               #* recebe o ID do Usuario
    path('login/', LoginUsuario, name='login-usuario'),  #* realiza a autenticação
    path('sign-up/', NovoUsuario, name='criar-usuario'), #* cria um novo usuario
]

#* API module urls
#*      /api/v1/:
urlpatterns = [
    path('', HealthCheck, name='check'), #* health check
] + propostas_urls + usuario_urls