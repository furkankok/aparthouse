import json
import uuid
from django.shortcuts import render
from django.http import HttpResponse
from oauth2_provider.decorators import protected_resource
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import Http404

from user_preview.models import UserInfo

from django.views.decorators.http import require_http_methods

from utils import check_recaptcha


@require_http_methods(["POST"])
@protected_resource()
def register(request):
    data = json.loads(request.body)

    if not check_recaptcha(data['recaptcha']):
        return HttpResponse("Recaptcha is required", status=400)
    
    
    if data['password'] != data['password2']:
        return HttpResponse("Passwords do not match", status=400)
    
    user = User.objects.create_user(data['email'], data['email'], data['password'], first_name = data['first_name'], last_name = data['last_name'], is_active = False)

    user_info = UserInfo.objects.create(user=user, email_token=uuid.uuid4())
    send_mail(
        "Subject here",
        "Token = " + str(user_info.email_token),
        "furkankoksaldi28@gmail.com",
        ["hixori7973@pursip.com"],
    )

    return HttpResponse("User created", status=200)

@require_http_methods(["GET"])
def email_verify(request):
    token = request.GET.get('token')
    user_info = UserInfo.objects.filter(email_token=token, email_token_used = False).last()

    if user_info is None:
        raise Http404("Token not found")
    
    user_info.email_token_used = True
    user_info.user.is_active = True
    user_info.user.save()
    user_info.save()

    return HttpResponse("Email verified", status=200)


@require_http_methods(["POST"])
def forget_password(request):
    data = json.loads(request.body)
    user = User.objects.filter(email=data['email']).last()

    if user is None:
        raise Http404("User not found")

    user_info = UserInfo.objects.create(user=user, forget_password_token=uuid.uuid4())
    send_mail(
        "Subject here",
        "Token = " + str(user_info.forget_password_token),
        "furkankoksaldi28@gmail.com",
        ["hixori7973@pursip.com"],
    )
    
    return HttpResponse("Email sent", status=200)


@require_http_methods(["POST"])
def reset_password(request):
    data = json.loads(request.body)

    if data['password'] != data['password2']:
        return HttpResponse("Passwords do not match", status=400)
    
    user_info = UserInfo.objects.filter(forget_password_token=data['token'], forget_password_token_used = False).last()

    if user_info is None:
        raise Http404("Token not found")
    
    user_info.forget_password_token_used = True
    user_info.user.set_password(data['password'])
    user_info.user.save()
    user_info.save()

    return HttpResponse("Password changed", status=200)




