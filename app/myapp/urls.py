from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicio, name='pagina_inicio'),
    path('create_point/', views.create_point, name='create_point'),
    path('create_point/<int:point_id>/', views.create_point, name='edit_point'),
    path('delete_point/<int:point_id>/', views.delete_point, name='delete_point'),
    path('points/', views.get_points, name='obtener_puntos'),
    
    path('create_edge/', views.create_edge, name='create_edge'),
    path('create_edge/<int:edgeId>/', views.create_edge, name='edit_edge'),
    path('delete_edge/<int:edgeId>/', views.delete_edge, name='delete_edge'),
    path('edges/', views.get_edges, name='get_edges'),
    
    path('plan_route/', views.plan_route_info, name='plan_route'),
]
