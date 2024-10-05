from django.shortcuts import render
from django.http import JsonResponse

import json
import markdown

from ..llm import show_info_route
from ..utils.map_utils import Map
from ..modules.module_1.module_1 import plan_route


def view_route_description(request):
    # Cargamos los datos del mapa
    map_data = Map()
    
    # Cargamos los datos de los turistas
    with open('./myapp/utils/route_data.json', 'r') as file:
        route = json.load(file)
    
    interesting_points = []
    for goal in route:
        interesting_points.append({
            'id': goal,
            'location': map_data.points[goal].location,
            'height': map_data.points[goal].height,
            'characteristics':map_data.points[goal].characteristics
        }) 

    info = show_info_route(interesting_points)

    return render(request, 'route_info.html', {'info': info})

    
def ver_encuesta(request):
    # Leer el contenido del archivo Markdown
    with open('./myapp/modules/module_0/info.md', 'r', encoding='utf-8') as file:
        contenido_markdown = file.read()

    # Convertir el contenido Markdown a HTML
    contenido_html = markdown.markdown(contenido_markdown)

    # Pasar el contenido HTML al template
    return render(request, 'survey.html', {'contenido_html': contenido_html})
