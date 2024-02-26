from functools import wraps

import requests
from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse
from oauth2_provider.decorators import protected_resource


def success_response(message="", data=None, paginate=None):
    return JsonResponse({
        "status": "success",
        "message": message,
        "data": data,
        "title": "Başarılı",
        "paginate": {
            "count": paginate.count,
            "num_pages": paginate.num_pages,
            "page_range": list(paginate.page_range),
        } if paginate else None
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



def is_staff(view_func):
    @protected_resource()
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper