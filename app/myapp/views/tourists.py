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
