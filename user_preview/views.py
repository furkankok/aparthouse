import json
from django.shortcuts import render
from django.http import HttpResponse
from oauth2_provider.decorators import protected_resource
from django.contrib.auth.models import User

# Create your views here.

@protected_resource()
def register(request):
    data = json.loads(request.body)

    if data['password'] != data['password2']:
        return HttpResponse("Passwords do not match", status=400)
    
    User.objects.create_user(data['email'], data['email'], data['password'], first_name = data['first_name'], last_name = data['last_name'])

    return HttpResponse("User created", status=200)













