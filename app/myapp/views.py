from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .phind import phind
from .models import Point
from django.shortcuts import render, redirect
from .forms import PointForm
from django.views.generic.edit import CreateView
from .models import Edge
from .forms import EdgeForm
from .modules.module_1 import plan_route

def pagina_inicio(request):
    return render(request, 'index.html')


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


def plan_route_info(request):
    data = plan_route()

    points = [{
        "id": 32,
        "location": [886,747],
        "characteristics": [0.6, 0.4, 0, 0.2, 0, 0],
        "altitude": "low",
        "height": 10
    },
    {
        "id": 36,
        "location": [1230,413],
        "characteristics": [0.9, 0.8, 0.4, 0, 0, 0.5],
        "altitude": "top",
        "height": 120
    },
    {
        "id": 55,
        "location": [1744,730],
        "characteristics": [0.9, 0.4, 0.3, 0.7, 0, 0.3],
        "altitude": "low",
        "height": 10
    },
    {
        "id": 60,
        "location": [1760,45],
        "characteristics": [0.8, 0.1, 0, 0.2, 0, 0.8],
        "altitude": "low",
        "height": 6
    }]

    info = phind(points)
    
    return render(request, 'route_info.html', {'data': data, 'info': info})

