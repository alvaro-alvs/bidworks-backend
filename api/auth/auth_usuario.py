import requests
import json
import bcrypt
from django.http import JsonResponse
from api.models.usuario import Usuario
from api.auth.generate_auth_token import GenerateAuthToken
from api.models.credentials import SenhaUsuario, TokenUsuario
from django.views.decorators.http import require_POST


@require_POST
def LoginUsuarioOAuth(request):
    """
    Recebe o access token do Google e realiza a autenticação usando a API oficial do Google
    
    body: {
        access_token: str
    } -> {
        status: str
    }
    """
    body = json.loads(request.body)
    
    if not body.get('access_token'):
        return JsonResponse({'status': 'Missing access token'}, status=400)
    
    try:
        google_response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', headers={'Authorization': f'Bearer {body["access_token"]}'})
        google_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return JsonResponse({'status': 'Error connecting to Google API'}, status=500)
    
    if google_response.status_code == 200:
        try:
            google_data = google_response.json()
            # print('google data: ', google_data)
            
            last_name = google_data.get('family_name', '')
            user = GetOrCreateUsuario(email=google_data['email'], first_name=google_data['given_name'], last_name=last_name, password='', foto=google_data['picture'])
            token = GenerateAuthToken(user) #* Gera o token e salva no db -> retorna apenas a string do token
            
            if not token:
                return JsonResponse({'status': 'Error generating token'}, status=500)
            
            user_payload = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'foto': user.foto
            }
            
            return JsonResponse({'status': 'autenticado', 'usuario': user_payload, 'tokens': { 'access': token }}, status=200)
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'Error parsing Google response'}, status=400)
    else:
        return JsonResponse({'status': 'Error authenticating user'}, status=403)


def GetOrCreateUsuario(email, first_name, last_name, password, foto):
    try:
        user = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        user = Usuario.objects.create(email=email, first_name=first_name, last_name=last_name, foto=foto)
        
        if password:
            SenhaUsuario.objects.create(user=user, password=password)
        
        # Salva as credenciais
        user.save()
    return user

@require_POST
def LoginUsuario(request):
    """
    Recebe o email e senha do usuario e realiza a autenticação
    """
    try:
        data = json.loads(request.body)
        
        if not isinstance(data, dict):
            return JsonResponse({'status': 'error', 'message': 'Dados inválidos'}, status=400)

        email = data.get('email')
        senha = data.get('password')
        # DEBUG
        # print(f"email: {email}, senha: {senha}")

        
        if not email or not senha:
            return JsonResponse({'status': 'error', 'message': 'Credenciais obrigatórias'}, status=400)

        # Busca o usuário
        user = Usuario.objects.get(email=email)

        # Verifica se o usuário existe
        if not user:
            return JsonResponse({'status': 'error', 'message': 'Usuário não encontrado'}, status=404)

        # Busca as credenciais
        creds = SenhaUsuario.objects.filter(user=user).first()

        # Verifica se as credenciais existem
        if not creds:
            return JsonResponse({'status': 'error', 'message': 'Credenciais inválidas'}, status=401)

        # Verifica senha
        senha_bytes = senha.encode('utf-8')
        if not bcrypt.checkpw(senha_bytes, bytes(creds.senha)):
            return JsonResponse({'status': 'error', 'message': 'Credenciais inválidas'}, status=401)

        """
        Daqui pra baixo, a função gera e retorna o auth_token do usuario autenticado

        ta errado? Ta. Mas funciona
        """

        #* Gera o token de acesso
        access_token = GenerateAuthToken(user)
        
        json_user = {
            # 'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }

        response = JsonResponse({
            'status': 'success',
            'usuario': json_user,
            'tokens': {
                'access': access_token,
            }
        }, status=200)
        
        # response.set_cookie(
        #     key='auth_token',
        #     value=access_token,
        #     httponly=True,
        #     secure=True,
        #     samesite='Strict',
        #     max_age=60 * 60 * 24 * 7
        # )
        
        return response

    except Usuario.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Usuário não encontrado'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'JSON inválido'}, status=400)
    except AttributeError:
        return JsonResponse({'status': 'error', 'message': 'Credenciais inválidas'}, status=401)
    except Exception as e:
        print(f"Erro no login: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Erro interno'}, status=500)
