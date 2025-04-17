import bcrypt
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import  JsonResponse
from django.views.decorators.http import require_POST
from api.models import usuario, credentials
from api.services.validate_form import validateForm #* importando validador de formulario

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
    # Verifica se o Content-Type é application/json
    content_type = request.headers.get('Content-Type', '')
    if 'application/json' not in content_type:
        return JsonResponse({'status': 'Content-Type must be application/json'}, status=400)

    # Dados do formulário estão em request.body (não em request.POST)
    form_data = json.loads(request.body)  # Decodifica JSON para dicionário Python

    # print('form data: ', form_data) #* debug

    #* Validação dos dados
    is_valid, error_msg = validateForm(form_data)
    
    if not is_valid:
        return JsonResponse({'status': error_msg}, status=400)
    
    #* separação da senha
    SENHA = form_data.get('password')
    
    del form_data['password']

    #* Criação do usuário
    try:
        usuario_criado = usuario.Usuario.objects.create(**form_data)
    except Exception as e:
        return JsonResponse({'status': str(e)}, status=400)

    #* Geração de senha (ajuste conforme sua lógica)
    #* gera a senha
    senha_criada = GerarSenha(usuario=usuario_criado, senha=SENHA)

    if not senha_criada:
        return JsonResponse({'status': 'Error creating password'}, status=500)


    access_token = GenerateAuthToken(usuario_criado)

    new_user_payload = {
        "usuario": {
            "first_name": usuario_criado.first_name,
            "last_name": usuario_criado.last_name,
                "email": usuario_criado.email,
            },
        "tokens": {
            "access": access_token,
        }
    }

    return JsonResponse(new_user_payload, status=201)


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

    
