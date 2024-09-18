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
        save_map_img()
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
        save_map_img()
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
    
    with open('./myapp/utils/route_data.json', 'w') as file:
            json.dump(route, file, indent=4)

    interesting_points = []
    for goal in goals:
        interesting_points.append({
            'id': goal,
            'location': map_data.points[goal].location,
            'height': map_data.points[goal].height,
            'characteristics':map_data.points[goal].characteristics
        }) 
    
    return render(request, 'route_info.html', {'data': route})

def view_route_description(request):
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
    
    info = show_info_route(interesting_points)
    return JsonResponse(info, safe=False)
    

def run_simulate(request):

    with open('./myapp/utils/route_data.json', 'r') as file:
        route = json.load(file)
    
    with open('./myapp/utils/tourists_data.json', 'r') as file:
        tourists = json.load(file)

    map_data = Map()
    
    desires = [person['characteristics'] for person in tourists]

    edges = {}
    edges_size = {}
    points = {}
    for key in map_data.paths_details.keys():
        edges[key] = map_data.paths_details[key]["characteristics"] 
        edges_size[key] = map_data.paths_details[key]["distance"]
    
    for key in map_data.points.keys():
        points[key] = map_data.points[key].characteristics

    map = Mapa(points, edges_size, edges=edges)

    precomputed_data = precompute_excursion_data(desires, route, map)
    
    simulate = Simulation()

    camp_points_data = []
    reagroup_points_data = []
    launch_points_data = []
    for _ in range(100):
        camp_points, reagroup_points,  launch_points = simulate.simulate_excursion(desires, route, map, precomputed_data)
        camp_points_data.append(camp_points)
        reagroup_points_data.append(reagroup_points)
        launch_points_data.append(launch_points)

    info = {
        'camp_points_data': camp_points_data,
        'reagroup_points_data': reagroup_points_data,
        'launch_points_data': launch_points_data
    }
    return render(request, 'run_simulate.html', {'info': info})

def ver_encuesta(request):
    # Leer el contenido del archivo Markdown
    with open('./myapp/modules/module_0/info.md', 'r', encoding='utf-8') as file:
        contenido_markdown = file.read()

    # Convertir el contenido Markdown a HTML
    contenido_html = markdown.markdown(contenido_markdown)

    # Pasar el contenido HTML al template
    return render(request, 'survey.html', {'contenido_html': contenido_html})

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

class Mapa:
    def __init__(self, points, edges_size, edges):
        self.points = points
        self.edges_size = edges_size
        self.edges = edges



def precompute_excursion_data(desires, route, map):
    # Precompute the waiting times and intentions for each tourist at each point
    precomputed_data = []
    
    for i in range(len(desires)):
        agent_data = []
        for point in route:
            point_data = map.points[point]
            beliefs = {
                "point_flora": point_data[2],
                "point_fauna": point_data[3],
                "point_history": point_data[4],
                "point_rivers": point_data[5]
            }
            his_desires = {}
            his_desires["point"] = {
            'user_flora': desires[i][2],
            'user_fauna': desires[i][3],
            'user_history': desires[i][4],
            'user_rivers':desires[i][5]
            }
            his_desires["path"] = {
            'user_isolation': desires[i][0],
            'user_challenge':desires[i][1],
            'user_flora': desires[i][2],
            'user_fauna': desires[i][3]
            }

            waiting_time = compute_fuzzy_output(context='waiting_time', **(beliefs | his_desires["point"]))
            agent_data.append({
                "waiting_time": waiting_time
            })
        precomputed_data.append(agent_data)
    
    return precomputed_data
