from django.urls import path
from apart import views

urlpatterns = [
	path('<int:apart_id>/', views.apart_detail, name='apart_detail'),

]