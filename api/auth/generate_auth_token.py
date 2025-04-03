import secrets

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.cache import cache

@require_http_methods(["GET"])
def GenerateAuthToken(request):
    token = secrets.token_hex(16)
    cache.set(
        f"auth_token:{token}",
        {
            "user_ip": request.META.get("REMOTE_ADDR"),
            "user_agent": request.META.get("HTTP_USER_AGENT", "")
        },
        3600  # Expira em 1 hora
    )
    return JsonResponse({"token": token, "expires_in": 3600})

# views.py
from django.core.cache import cache

@require_http_methods(["GET"])
def ValidateToken(request):
    token = request.headers.get('Authorization', '').split('Bearer ')[-1]
    is_valid = cache.get(f'auth_token:{token}') is not None
    return JsonResponse({ 'valid': is_valid })