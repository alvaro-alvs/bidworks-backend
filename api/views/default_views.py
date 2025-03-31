import json
from django.http import HttpResponse, JsonResponse


#* Views de debug
def HealthCheck(request):
    if request.method == 'GET':
        
        return JsonResponse({'status': 'To bem, to respirando'}, status=200)