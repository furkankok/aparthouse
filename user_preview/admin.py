from django.contrib import admin

from user_preview.models import UserInfo, ApartComment

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(ApartComment)
