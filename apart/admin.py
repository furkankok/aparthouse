from django.contrib import admin
from .models import ApartUniversity, ApartCategory, ApartServiceCategory, ApartService, ApartBillDetail, Apart, ApartImage

# Register your models here.
admin.site.register(ApartUniversity)
admin.site.register(ApartCategory)
admin.site.register(ApartServiceCategory)
admin.site.register(ApartService)
admin.site.register(ApartBillDetail)
admin.site.register(Apart)
admin.site.register(ApartImage)
