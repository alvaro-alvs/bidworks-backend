# middleware.py
import json
from django.http import JsonResponse
from api.models.credentials import TokenUsuario

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ignora validação para rotas públicas (ex: gerar token)
        allowed_routes = [
            '/api/v1/login/',
            '/api/v1/login/oauth/',
            '/api/v1/sign-up/',
            '/api/v1/get-token/'
            '/api/v1/validate-token/',
        ]
        
        if request.path in allowed_routes:
            return self.get_response(request)
        
            
        #* Obtém o token do header 'Authorization'
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse(
                {"error": "Token de autenticação ausente ou inválido"},
                status=401
            )
        
        #* Extrai o token
        token = auth_header.split(" ")[1]
        
        #* Verifica se o token existe no database
        database_token = TokenUsuario.objects.filter(token=token).first()
        
        # Verifica se o token é valido
        if not database_token:
            return JsonResponse(
                {"error": "Token inválido ou expirado"}, 
                status=403
            )
        
        return self.get_response(request)