from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicio, name='pagina_inicio'),
    
    # Point urls
    path('create_point/', views.create_point, name='create_point'),
    path('create_point/<int:point_id>/', views.create_point, name='edit_point'),
    path('delete_point/<int:point_id>/', views.delete_point, name='delete_point'),
    path('points/', views.get_points, name='obtener_puntos'),
    path('save_points/', views.save_points, name='save_points'),
    
    # Edge urls
    path('create_edge/', views.create_edge, name='create_edge'),
    path('create_edge/<int:edgeId>/', views.create_edge, name='edit_edge'),
    path('delete_edge/<int:edgeId>/', views.delete_edge, name='delete_edge'),
    path('edges/', views.get_edges, name='get_edges'),
    path('save_edges/', views.save_edges, name='save_edges'),
    
    # Tourist urls
    path('create_tourist/', views.create_tourist, name='create_tourist'),
    path('create_tourist/<int:tourist_id>/', views.create_tourist, name='edit_tourist'),
    path('delete_tourist/<int:tourist_id>/', views.delete_tourist, name='delete_tourist'),
    path('tourists/', views.get_tourists, name='get_tourists'),
    path('save_tourists/', views.save_tourists, name='save_tourists'),
    
    path('plan_route/', views.plan_route_info, name='plan_route'),
    path('plan_route/get_info/', views.view_route_description, name='get_info'),
    path('run_simulate/', views.run_simulate, name='run_simulate'),
]
