from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),  
    path('register/', views.register, name='register'),  
    path('thank_you/', views.thank_you, name='thank_you'),  
]


