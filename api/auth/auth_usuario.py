import requests
import json
import bcrypt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.models.usuario import Usuario
from api.models.credentials import SenhaUsuario

from api.views.usuario_views import NovoUsuario

def LoginUsuarioOAuth(request):
    """
    Recebe o access token do Google e realiza a autenticação usando a API oficial do Google
    
    body: {
        access_token: str
    } -> {
        status: str
    }
    """
    if request.method == 'POST':
        body = json.loads(request.body)
        
        if not body.get('access_token'):
            return JsonResponse({'status': 'Missing access token'}, status=400)
        
        google_response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', headers={'Authorization': f'Bearer {body["access_token"]}'})
        
        print(google_response.status_code)
        
        if google_response.status_code == 200:
            google_data = google_response.json()
            
            print(google_data)
            
            return JsonResponse({'status': 'User authenticated'}, status=200)
        
        else:
            return JsonResponse({'status': 'Error authenticating user'}, status=403)
        
    else:
        return JsonResponse({'status': 'Invalid request'}, status=400)
            


def LoginUsuario(request):
    """
    Recebe o email e senha do usuario e realiza a autenticação
    
    """
    #* AUTENTICAÇÃO FUNCIONANDO VIA JSON
    
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)

    #* Decodifica os dados da requisição (JSON)
    data = json.loads(request.body)
    
    if not isinstance(data, dict):
        return JsonResponse({'status': 'error', 'message': 'Dados inválidos (JSON malformado)'}, status=400)


    email = data.get('email')
    senha = data.get('password')

    #* Validação básica dos campos
    if not email or not senha:
        return JsonResponse({'status': 'error', 'message': 'Email e senha são obrigatórios'}, status=400)

    #* Busca o usuário pelo email
    try:
        user = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Usuário nao encontrado'}, status=404)


    #* Busca as credenciais do usuário (senha hasheada)
    creds = SenhaUsuario.objects.get(user=user)

    #* Verifica se as credenciais foram encontradas
    if not creds:
        return JsonResponse({'status': 'error', 'message': 'Credenciais não encontradas'}, status=401)

    #* Verifica a senha com bcrypt
    try:
        senha_bytes = senha.encode('utf-8')
        senha_hasheada_bytes = creds.senha
        
        if bcrypt.checkpw(senha_bytes, senha_hasheada_bytes):
            #* Autenticação bem-sucedida! (implementar JWT aqui)
            return JsonResponse({
                'status': 'success',
                'user': {
                    'email': user.email,
                    'nome': user.first_name,  # Adicione outros campos se necessário
                    'sobrenome': user.last_name
                }
            }, status=200)
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'Erro ao verificar a senha'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Credenciais inválidas'}, status=401)
