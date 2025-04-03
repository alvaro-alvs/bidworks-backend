"""
URL configuration for bidworks_backend project.

O array `urlpatterns` lista as rotas da URL para as views, usando a função path([rota], view).

    docs:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
    
Exemplos que vieram no template:
    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path


urlpatterns = [
    path('api/v1/', include('api.urls')),
]
