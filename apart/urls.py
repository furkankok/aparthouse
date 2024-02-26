from django.urls import path
from apart import views

urlpatterns = [
	path('<int:apart_id>/', views.apart_detail, name='apart_detail'),
	path('<int:apart_id>/comment/', views.apart_comment, name='apart_comment'),
]