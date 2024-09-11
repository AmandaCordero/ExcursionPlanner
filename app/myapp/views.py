import json
from django.http import JsonResponse

from django.shortcuts import get_object_or_404, render
from .models import Point, Edge, Tourist
from .phind import phind
from django.shortcuts import render, redirect
from .forms import PointForm, EdgeForm, TouristForm
from django.views.generic.edit import CreateView
from .utils.map_utils import Map
from .modules.module_1.module_1 import plan_route


def pagina_inicio(request):
    return render(request, 'index.html')


# Points CRUD

def create_point(request, point_id=None):
    if point_id:
        point = get_object_or_404(Point, id=point_id)
    else:
        point = None

    if request.method == 'POST':
        form = PointForm(request.POST, instance=point)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PointForm(instance=point)
    
    points = Point.objects.all()
    return render(request, 'create_point.html', {'form': form, 'points': points, 'point': point})

def delete_point(request, point_id):
    point = get_object_or_404(Point, id=point_id)
    point.delete()
    return redirect('create_point')

def get_points(request):
    puntos = list(Point.objects.all().values())
    return JsonResponse(puntos, safe=False)

def save_points(request):
    points = list(Point.objects.all().values())
    if len(points) > 0:
        # Guardar los datos de los puntos
        with open('./myapp/utils/points_data.json', 'w') as file:
            json.dump(points, file, indent=4)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'No hay turistas guardados'})
    
# Edges CRUD

def create_edge(request, edgeId=None):
    if edgeId:
        edge = get_object_or_404(Edge, id=edgeId)
    else:
        edge = None

    if request.method == 'POST':
        form = EdgeForm(request.POST, instance=edge)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = EdgeForm(instance=edge)
        
    edges = Edge.objects.all()
    return render(request, 'create_edge.html', {'form': form, 'edges':edges, 'edge':edge})

def delete_edge(request, edgeId):
    edge = get_object_or_404(Edge, id=edgeId)
    edge.delete()
    return redirect('create_edge')

def get_edges(request):
    edges = list(Edge.objects.values())
    return JsonResponse(edges, safe=False)

def save_edges(request):
    edges = list(Edge.objects.all().values())
    if len(edges) > 0:
        # Guardar los datos de los caminos
        with open('./myapp/utils/edges_data.json', 'w') as file:
            json.dump(edges, file, indent=4)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'No hay caminos guardados'})
    
# Tourists CRUD

def create_tourist(request, tourist_id=None):
    if tourist_id:
        tourist = get_object_or_404(Tourist, id=tourist_id)
    else:
        tourist = None

    if request.method == 'POST':
        form = TouristForm(request.POST, instance=tourist)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = TouristForm(instance=tourist)
    
    tourists = Tourist.objects.all()
    return render(request, 'create_tourist.html', {'form': form, 'tourists': tourists, 'tourist': tourist})

def delete_tourist(request, tourist_id):
    tourist = get_object_or_404(Tourist, id=tourist_id)
    tourist.delete()
    return redirect('create_tourist')

def get_tourists(request):
    tourists = list(Tourist.objects.all().values())
    return JsonResponse(tourists, safe=False)

def save_tourists(request):
    tourists = list(Tourist.objects.all().values())
    if len(tourists) > 0:
        # Guardar los datos de los turistas
        with open('./myapp/utils/tourists_data.json', 'w') as file:
            json.dump(tourists, file, indent=4)
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'No hay turistas guardados'})



def plan_route_info(request):
    # Cargamos los datos del mapa
    map_data = Map()
    
    # Cargamos los datos de los turistas
    with open('./myapp/utils/tourists_data.json', 'r') as file:
        tourists = json.load(file)
    
    characteristics = []
    for tourist in tourists:
        characteristics.append(tourist['characteristics'])
    
    route, goals = plan_route(map_data, characteristics)
    
    interesting_points = []
    for goal in goals:
        interesting_points.append({
            'id': goal,
            'location': map_data.points[goal].location,
            'height': map_data.points[goal].height,
            'characteristics':map_data.points[goal].characteristics
        }) 

    info = phind(interesting_points)
    
    return render(request, 'route_info.html', {'data': data, 'info': info})

