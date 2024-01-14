"""
URL configuration for aparthouse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
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
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate
import requests
from oauth2_provider.views import TokenView as OAuth2TokenView

from utils import check_recaptcha

class LoginToken(OAuth2TokenView):
    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if not user:
            return HttpResponse("Email or pass wrong", status=400)
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            recaptcha = request.POST.get("recaptcha", None)
            if recaptcha is None:
                return HttpResponse("Recaptcha is required", status=400)
            if not check_recaptcha(recaptcha):
                return HttpResponse("Recaptcha is wrong", status=400)
        return response

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('o/token/', lambda request: HttpResponseForbidden()),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('o/login_token/', LoginToken.as_view()),
    path('user/', include('user_preview.urls')),

]
