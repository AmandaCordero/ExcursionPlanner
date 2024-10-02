import json
from django.http import JsonResponse

from django.shortcuts import get_object_or_404, render
import markdown

from .modules.module_2.defuzzification_module import compute_fuzzy_output

from .modules.module_2.module_2_main import Simulation

from .models import Point, Edge, Tourist
from .llm import show_info_route
from django.shortcuts import render, redirect
from .forms import PointForm, EdgeForm, TouristForm
from django.views.generic.edit import CreateView
from .utils.map_utils import Map
from .modules.module_1.module_1 import plan_route
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


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
        save_map_img()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'No hay turistas guardados'})
 