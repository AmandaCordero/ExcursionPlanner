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
        save_map_img()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'No hay caminos guardados'})
   