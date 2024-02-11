from django.shortcuts import render
from utils import is_staff, success_response
from oauth2_provider.decorators import protected_resource
from django.http import HttpResponseForbidden

