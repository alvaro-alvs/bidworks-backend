import bcrypt
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import  JsonResponse
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


#* Recebe o email e senha do usuario e realiza a autenticação
@csrf_exempt
def LoginUsuario(request):
    #* AUTENTICAÇÃO FUNCIONANDO VIA JSON
    
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)

    #* Decodifica os dados da requisição (JSON)
    data = json.loads(request.body)
    
    if not isinstance(data, dict):
        return JsonResponse({'status': 'error', 'message': 'Dados inválidos (JSON malformado)'}, status=400)


    email = data.get('email')
    senha = data.get('senha')

    #* Validação básica dos campos
    if not email or not senha:
        return JsonResponse({'status': 'error', 'message': 'Email e senha são obrigatórios'}, status=400)

    #* Busca o usuário pelo email
    user = usuario.Usuario.objects.get(email=email)
    
    if not user:
        return JsonResponse({'status': 'error', 'message': 'Usuário não encontrado'}, status=404)

    #* Busca as credenciais do usuário (senha hasheada)
    creds = credentials.SenhaUsuario.objects.get(user=user)

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


#* Cria um novo usuario e salva o hash da senha no database
@csrf_exempt  # Remova isso em produção! Use CSRF token corretamente.
def NovoUsuario(request):
    if request.method == 'POST':
        # Verifica se o Content-Type é multipart/form-data
        content_type = request.headers.get('Content-Type', '')
        if 'multipart/form-data' not in content_type:
            return JsonResponse({'status': 'Content-Type must be multipart/form-data'}, status=400)

        # Dados do formulário estão em request.POST (não em request.body)
        form_data = request.POST.dict()  # Converte QueryDict para dicionário Python

        print('form data: ', form_data) #* debug

        # Validação dos dados
        is_valid, error_msg = validateForm(form_data)
        
        if not is_valid:
            return JsonResponse({'status': error_msg}, status=400)
        
        #* separação da senha
        SENHA = form_data.get('password')
        del form_data['password']

        # Criação do usuário
        try:
            usuario_criado = usuario.Usuario.objects.create(**form_data)
        except Exception as e:
            return JsonResponse({'status': f'Error: {str(e)}'}, status=400)

        # Geração de senha (ajuste conforme sua lógica)
        senha_criada = GerarSenha(usuario=usuario_criado, senha=SENHA)

        if not senha_criada:
            return JsonResponse({'status': 'Error creating password'}, status=400)

        return JsonResponse({'status': 'User created'}, status=201)
    else:
        return JsonResponse({'status': 'Method not allowed'}, status=405)
    

#* recebe uma senha e o id do usuario -> cria um hash para a senha -> em seguida salva o hash no database
def GerarSenha(usuario, senha):
    salt = bcrypt.gensalt()
    senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)
    
    senha_criada = credentials.SenhaUsuario(user=usuario, senha=senha_hashed)
    
    if senha_criada:
        senha_criada.save()
        
    return senha_criada

    
