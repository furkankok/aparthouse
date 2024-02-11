from django.urls import path
from apart.models import ApartCategory, ApartUniversity, ApartServiceCategory, ApartService, ApartBillDetail, ApartImage
from apart_admin import views
from models_to_url import ModelToURL

urlpatterns = [
    path('apart_category/', ModelToURL(ApartCategory).get_urls()),
    path('apart_university/', ModelToURL(ApartUniversity).get_urls()),
    path('apart_service_category/', ModelToURL(ApartServiceCategory).get_urls()),
    path('apart_service/', ModelToURL(ApartService).get_urls()),
    path('apart_bill_detail/', ModelToURL(ApartBillDetail).get_urls()),
    path('apart_image/', ModelToURL(ApartImage).get_urls()),
]