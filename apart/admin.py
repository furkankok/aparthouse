from django.contrib import admin
from .models import (Apart, ApartBillDetail, ApartCategory, ApartDistance, ApartImage, ApartFirm,
                     ApartService, ApartServiceCategory, ApartUniversity, City, Town)



@admin.register(ApartUniversity)
class ApartUniversityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'city', 'country', 'address', 'lat', 'lon', 'created_at']



@admin.register(ApartCategory)
class ApartCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
   


@admin.register(ApartServiceCategory)
class ApartServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
   
@admin.register(ApartService)
class ApartServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'created_at']
    

@admin.register(ApartBillDetail)
class ApartBillDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
  

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
   


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'city', 'created_at']
  


@admin.register(Apart)
class ApartAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'lat', 'lon', 'created_at']
   


@admin.register(ApartImage)
class ApartImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'apart', 'image', 'created_at']


@admin.register(ApartDistance)
class ApartDistanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'university', 'apart', 'yurume', 'otobus', 'tramvay', 'created_at']


@admin.register(ApartFirm)
class ApartFirmAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']