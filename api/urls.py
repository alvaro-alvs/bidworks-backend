from django.urls import path

#* API Views
from api.views.default_views import HealthCheck
from api.views.usuario_views import NovoUsuario, GetUsuario
from api.views.proposta_views import ListarPropostas, GetProposta, ListarPropostasUsuario
from api.auth.generate_auth_token import GenerateAuthToken, ValidateToken

#* Auth Service
from api.auth.auth_usuario import LoginUsuarioOAuth, LoginUsuario



"""
! POUCA COISA AQUI FOI TESTADA, 
! SE VIR ALGUMA MENGAGEM DE ERRO, JA CORRIJA POE GENTILEZA
"""


cliente_urls = [
    # definir
]

dev_urls = [
    # difinir
]

#* Urls de propostas
propostas_urls = [
    path('propostas-usuario/<int:id>/', ListarPropostasUsuario, name='obter-proposta'), #* recebe o id de um Cliente
    path('listar-propostas/', ListarPropostas, name='listar-propostas'),                #* lista todas as propostas
    path('proposta/<int:id>/', GetProposta, name='obter-proposta'),                     #* recebe o id de uma proposta
]

#* Urls do usuario
usuario_urls = [
    path('login/oauth/', LoginUsuarioOAuth, name='login-usuario-oauth'),    #* realiza a autenticação com google
    path('usuario/<int:id>/', GetUsuario, name='get-usuario'),              #* recebe o ID do Usuario
    path('sign-up/', NovoUsuario, name='criar-usuario'),                    #* cria um novo usuario
    path('login/', LoginUsuario, name='login-usuario'),                     #* realiza a autenticação com email
]

#* API module urls
#*      /api/v1/:
urlpatterns = [
    path('get-token/', GenerateAuthToken, name='get-token'),
    path('validate-token/', ValidateToken),
    path('', HealthCheck, name='check'), #* health check
] + propostas_urls + usuario_urls