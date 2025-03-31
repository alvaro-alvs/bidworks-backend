import json
import bcrypt
from django.http import JsonResponse
from api.models.credentials import SenhaUsuario


def AuthUsuario(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        
        if body.get('email') and body.get('password'):
            try:
                senha = SenhaUsuario.objects.get(email=body['email'])
            except SenhaUsuario.DoesNotExist:
                return JsonResponse({'status': 'User not found'}, status=400)
            
            if bcrypt.checkpw(body['password'].encode('utf-8'), senha.senha.encode('utf-8')):
                return JsonResponse({'status': 'User authenticated'}, status=200)