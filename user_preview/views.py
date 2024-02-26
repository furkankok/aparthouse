import json
import uuid
from django.shortcuts import render
from django.http import HttpResponse
from oauth2_provider.decorators import protected_resource
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import Http404
from django.utils.html import strip_tags
from user_preview.models import UserInfo

from django.views.decorators.http import require_http_methods
from django.core.mail import EmailMessage
from utils import check_recaptcha, error_response, success_response


@require_http_methods(["POST"])
# @protected_resource()
def register(request):
    data = json.loads(request.body)

    if not check_recaptcha(data['recaptcha']):
        return error_response("Recaptcha is required")
    
    
    if data['password'] != data['password2']:
        return error_response("Passwords do not match")
    
    user = User.objects.create_user(data['email'], data['email'], data['password'], first_name = data['first_name'], last_name = data['last_name'], is_active = False)

    user_info = UserInfo.objects.create(user=user, email_token=uuid.uuid4())

    msg = f"""
        <a href='http://localhost:3000/email_verify?token={user_info.email_token}'>Verify Email</a>
    """


    mail = EmailMessage(
        "Subject here",
        msg,
        "furkankoksaldi28@gmail.com",
        [data['email']],
    )
    mail.content_subtype = "html"
    mail.send()
    return success_response("Email gönderildi. Lütfen emailinizi kontrol edin.")

@require_http_methods(["POST"])
def email_verify(request):
    token = request.GET.get('token')
    user_info = UserInfo.objects.filter(email_token=token, email_token_used = False).last()

    if user_info is None:
        raise Http404("Token not found")
    
    user_info.email_token_used = True
    user_info.user.is_active = True
    user_info.user.save()
    user_info.save()

    return success_response("Email verified")


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
        [data['email']],
    )
    
    return success_response("Email sent")


@require_http_methods(["POST"])
def reset_password(request):
    data = json.loads(request.body)

    if data['password'] != data['password2']:
        return error_response("Şifre eşleşmiyor. Lütfen tekrar deneyin.")
    
    user_info = UserInfo.objects.filter(forget_password_token=data['token'], forget_password_token_used = False).last()

    if user_info is None:
        raise Http404("Token not found")
    
    user_info.forget_password_token_used = True
    user_info.user.set_password(data['password'])
    user_info.user.save()
    user_info.save()

    return success_response("Şifre değiştirildi")

