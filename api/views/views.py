import json
from django.http import HttpResponse, JsonResponse
from ..models import Usuario, Credentials
from django.views.decorators.csrf import csrf_exempt


#* Criar algo baseado no padrão REST _> implementar segurança 



#* função de validação de formulario
def validatePayload(body):
    """
    Validates the given payload to check if it meets the
    requirements for a user object.
    """
    if not body:
        return False
    
    required_keys = ['name', 'email', 'password']
    
    try:
        for key in required_keys:
            if not body[key]:
                return False
    
        if not isinstance(body['password'], str) or len(body['password']) < 8:
            return False
        
        return True
    
    except KeyError:
        return False
    

@csrf_exempt
def CreateUser(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        
        #* camada de validação 
        if not validatePayload(body):
            return JsonResponse({'status': 'Error'}, status=418)
        
        #* criação do objeto
        created = Usuario.objects.create(**body)
        
        credential_created = Credentials
        
        if not created:
            return JsonResponse({'status': 'Error'}, status=418)
        
        return JsonResponse({'status': 'User created'}, status=201)
    
    else:
        return JsonResponse({'status': 'no user given'}, status=400)

def HealthCheck(request):
    if request.method == 'GET':
        users_list = Usuario.objects.all()
        
        formated_user_list = []
        
        for user in users_list:
            formated_user_list.append({
                'name': user.nome,
                'email': user.email,
                'isActive': user.isActive
            })
        
        if len(users_list) == 0:
            return JsonResponse({'status': 'Error'})
    
        return JsonResponse({'status': 'OK', 'user_list': formated_user_list }, status=200)