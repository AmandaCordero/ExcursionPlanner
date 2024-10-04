from django.urls import path
from .views import edges
from .views import points
from .views import tourists
from .views import llm
from .views import landing
from .views import simulation
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', landing.pagina_inicio, name='pagina_inicio'),
    
    # Point urls
    path('create_point/', points.create_point, name='create_point'),
    path('create_point/<int:point_id>/', points.create_point, name='edit_point'),
    path('delete_point/<int:point_id>/', points.delete_point, name='delete_point'),
    path('points/', points.get_points, name='obtener_puntos'),
    path('save_points/', points.save_points, name='save_points'),
    
    # Edge urls
    path('create_edge/', edges.create_edge, name='create_edge'),
    path('create_edge/<int:edgeId>/', edges.create_edge, name='edit_edge'),
    path('delete_edge/<int:edgeId>/', edges.delete_edge, name='delete_edge'),
    path('edges/', edges.get_edges, name='get_edges'),
    path('save_edges/', edges.save_edges, name='save_edges'),
    
    # Tourist urls
    path('create_tourist/', tourists.create_tourist, name='create_tourist'),
    path('create_tourist/<int:tourist_id>/', tourists.create_tourist, name='edit_tourist'),
    path('delete_tourist/<int:tourist_id>/', tourists.delete_tourist, name='delete_tourist'),
    path('tourists/', tourists.get_tourists, name='get_tourists'),
    path('save_tourists/', tourists.save_tourists, name='save_tourists'),
    
    # path('plan_route/', simulation.plan_route_info, name='plan_route'),
    path('view_route_description/', llm.view_route_description, name='view_route_description'),
    path('mostrar_markdown/', llm.ver_encuesta, name='mostrar_markdown'),
    path('run_simulate/', simulation.run_simulate, name='run_simulate'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
