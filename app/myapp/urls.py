from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_point, name='create_point'),
    path('create_point/<int:point_id>/', views.create_point, name='edit_point'),
    path('delete_point/<int:point_id>/', views.delete_point, name='delete_point'),
]
