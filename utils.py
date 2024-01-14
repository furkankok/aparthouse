from django.conf import settings
import requests


def check_recaptcha(token):
    control = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
        "secret": settings.RECAPTCHA_SECRET,
        "response": token
    }).json()
    return control['success']