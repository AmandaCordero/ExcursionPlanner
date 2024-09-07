from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my-method/', views.my_method, name='my_method'),
]
