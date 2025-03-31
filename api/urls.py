

from django.urls import path
from api.views.default_views import HealthCheck
from api.views.usuario_views import NovoUsuario, LoginUsuario, GetUsuario
from api.views.proposta_views import ListarPropostas

#* API module urls
#* localhost/api/v1/:
urlpatterns = [
    path('', HealthCheck, name='check'),                            #* health check
    path('usuario/<int:id>/', GetUsuario),                          #* recebe o ID do Usuario
    path('login/', LoginUsuario, name='login-usuario'),             #* realiza a autenticação
    path('sign-up/', NovoUsuario, name='criar-usuario'),            #* cria um novo usuario
    path('list-props/', ListarPropostas, name='lsitar-propostas'),  #* listar todas as propostas
]