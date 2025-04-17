import bcrypt
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import  JsonResponse
from django.views.decorators.http import require_POST
from api.models import usuario, credentials
from api.services.validate_form import validateForm #* importando validador de formulario
from api.auth.auth_usuario import GenerateAuthToken


#* Ja da pra fazer algo no front
def GetUsuario(request, id): #* recebe o ID do Usuario
    usuario_buscado = usuario.Usuario.objects.get(id=id)
    
    print(usuario_buscado.email)
    
    usuario_is_cliente = usuario.Cliente.objects.filter(usuario=usuario_buscado)
    usuario_is_dev = usuario.Dev.objects.filter(usuario=usuario_buscado)
    
    status = 'Usuario ainda não é Cliente nem Dev'
    
    if usuario_is_cliente:
        status = 'Usuario é um Cliente'
        
    if usuario_is_dev:
        status = 'Usuário é um Dev'
        
    if usuario_is_cliente and usuario_is_dev:
        status = 'Usuário é um Dev e Cliente'
            
    return JsonResponse({'nome': usuario_buscado.first_name, 'status': status}, status=200)



#* Cria um novo usuario e salva o hash da senha no database
@require_POST
def NovoUsuario(request):
    try:
        # Verifica se o Content-Type é application/json
        content_type = request.headers.get('Content-Type', '')
        if 'application/json' not in content_type:
            return JsonResponse({'status': 'Content-Type must be application/json'}, status=400)

        # Decodifica JSON do request body
        try:
            form_data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'Invalid JSON format'}, status=400)

        # Validação dos dados do formulário
        is_valid, error_msg = validateForm(form_data)
        if not is_valid:
            return JsonResponse({'status': error_msg}, status=400)

        # Extrai e remove senha dos dados do usuário
        senha = form_data.pop('password', None)
        if not senha:
            return JsonResponse({'status': 'Password is required'}, status=400)

        # Cria novo usuário
        try:
            novo_usuario = usuario.Usuario.objects.create(**form_data)
        except Exception as e:
            return JsonResponse({'status': f'Error creating user: {str(e)}'}, status=400)

        # Gera e salva senha
        try:
            senha_criada = GerarSenha(usuario=novo_usuario, senha=senha)
            if not senha_criada:
                novo_usuario.delete()
                return JsonResponse({'status': 'Error creating password'}, status=500)
        except Exception as e:
            novo_usuario.delete()
            return JsonResponse({'status': f'Error with password: {str(e)}'}, status=500)

        # Gera token de acesso
        try:
            access_token = GenerateAuthToken(novo_usuario)
            if not access_token:
                novo_usuario.delete()
                return JsonResponse({'status': 'Error generating access token'}, status=500)
        except Exception as e:
            novo_usuario.delete()
            return JsonResponse({'status': f'Error with token: {str(e)}'}, status=500)

        # Prepara resposta
        response_data = {
            "usuario": {
                "first_name": novo_usuario.first_name,
                "last_name": novo_usuario.last_name,
                "email": novo_usuario.email,
            },
            "tokens": {
                "access": access_token,
            }
        }

        return JsonResponse(response_data, status=201)

    except Exception as e:
        return JsonResponse({'status': f'Unexpected error: {str(e)}'}, status=500)

#* recebe uma senha e o id do usuario -> cria um hash para a senha -> em seguida salva o hash no database
def GerarSenha(usuario, senha):
    """
    Recebe um Usuario(model) e gera uma senha e salva no banco de dados
    """
    salt = bcrypt.gensalt()
    senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)
    
    senha_criada = credentials.SenhaUsuario(user=usuario, senha=senha_hashed)
    
    if senha_criada:
        senha_criada.save()
        
    return senha_criada

    
