from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect

import json
import networkx as nx
import matplotlib.pyplot as plt

from ..models import Point
from ..forms import PointForm


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
 

def save_map_img():
    # Cargamos los datos
    with open('./myapp/utils/points_data.json', 'r') as file1:
        points = json.load(file1)
        
    # Cargamos los datos
    with open('./myapp/utils/edges_data.json', 'r') as file2:
        edges = json.load(file2)
    
    # Crear el grafo
    G = nx.Graph()

    # Estira la imagen
    factor_x = 2  # Factor de estiración en el eje X
    factor_y = 1    # Factor de estiración en el eje Y

    stretched_points = []
    for point in points:
        stretched_x = point['x'] * factor_x
        stretched_y = point['y'] * factor_y
        stretched_points.append({
            'point_id': point['point_id'],
            'x': stretched_x,
            'y': stretched_y,
            'height': point['height'],
            'characteristics': point['characteristics']
        })

    # Añadir nodos estirados
    for stretched_point in stretched_points:
        G.add_node(stretched_point['point_id'], pos=(stretched_point['x'], stretched_point['y']), height=stretched_point['height'], characteristics=stretched_point['characteristics'])

    # Añadir aristas
    for edge in edges:
        G.add_edge(edge['point1_id'], edge['point2_id'], distance=edge['distance'], characteristics=edge['characteristics'])

    # Dibujar el grafo
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw_networkx(G, pos, with_labels=True, node_size=500, node_color='skyblue', font_size=10, font_color='black')

    # Añadir gráficos de barras cerca de cada nodo
    for stretched_point in stretched_points:
        x, y = stretched_point['x'], stretched_point['y']
        characteristics = stretched_point['characteristics']

    # Guardar la imagen en formato SVG
    plt.savefig('./static/images/map.svg', format='svg', dpi=300, bbox_inches='tight')
