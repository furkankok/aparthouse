from django.conf import settings
import requests
from django.http import JsonResponse

def success_response(message="", data=None):
    return JsonResponse({
        "status": "success",
        "message": message,
        "data": data,
        "title": "Başarılı"
    })

def error_response(message):

    return JsonResponse({
        "status": "error",
        "message": message,
        "title": "Hata"
    }, status=400)

def check_recaptcha(token):
    control = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
        "secret": settings.RECAPTCHA_SECRET,
        "response": token
    }).json()
    return control['success']


# check is staff decorator
from django.http import HttpResponseForbidden
from functools import wraps
from oauth2_provider.decorators import protected_resource

def is_staff(view_func):
    @protected_resource()
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper