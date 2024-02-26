from django.urls import path
from apart.models import ApartCategory, ApartUniversity, ApartServiceCategory, ApartService, ApartBillDetail, ApartImage
from apart_admin import views
from models_to_url import ModelToURL

urlpatterns = [
    path('apart_category/', ModelToURL(ApartCategory).get_urls()),
    # path('apart_university/', ModelToURL(ApartUniversity).get_urls()),
    # path('apart_service_category/', ModelToURL(ApartServiceCategory).get_urls()),
    # path('apart_service/', ModelToURL(ApartService).get_urls()),
    # path('apart_bill_detail/', ModelToURL(ApartBillDetail).get_urls()),
    # path('apart_image/', ModelToURL(ApartImage).get_urls()),
    path('', views.index, name='index'),
    path('firma-ekle/', views.firma_ekle, name='firma_ekle'),
    path('firma-duzenle/<int:firm_id>/', views.firma_duzenle, name='firma_duzenle'),
    path('firma-sil/<int:firm_id>/', views.firma_sil, name='firma_sil'),
    path('<int:firm_id>/apart-ekle/', views.apart_ekle, name='apart_ekle'),
    path('get-town/', views.get_town, name='get_town'),
]