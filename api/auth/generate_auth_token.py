from datetime import datetime, timedelta
from django.utils import timezone
import secrets
import bcrypt
from django.http import JsonResponse
from api.models.credentials import TokenUsuario

    
def GenerateAuthToken(usuario):
    if not usuario:
        return
    
    token = secrets.token_urlsafe(32)
    expires_at = timezone.now() + timedelta(days=7)
    
    # print(token)
    
    TokenUsuario.objects.update_or_create(
        user=usuario,
        defaults={
            'token': token,
            'expires_at': expires_at
        }
    )
    
    
    return token

# views.py
from django.core.cache import cache


def ValidateToken(request):
    token = request.headers.get('Authorization', '').split('Bearer ')[-1]
    is_valid = cache.get(f'auth_token:{token}') is not None
    return JsonResponse({ 'valid': is_valid })