import json
import math
import random

# Lee el archivo JSON existente
with open('./utils/edges_data.json', 'r') as f:
    edges = json.load(f)
    
# Lee el archivo JSON existente
with open('./utils/points_data.json', 'r') as f:
    points = json.load(f)

# Función para calcular la distancia entre dos puntos
def calculate_distance(point1_id, point2_id, points):
    random_extra_distance = [10,20,30,40,50]
    
    # Seleccionar un elemento aleatorio
    plus = random.choice(random_extra_distance)
    
    point1 = points['points'][point1_id]
    point2 = points['points'][point2_id]
    
    return math.sqrt((point1['location'][0] - point2['location'][0])**2 + (point1['location'][1] - point2['location'][1])**2) + plus


# Procesa cada elemento del JSON
for edge in edges['edges']:
    point1 = edge['point1']
    point2 = edge['point2']
    distance = calculate_distance(point1, point2, points)
    edge['distance'] = distance

# Guarda el nuevo JSON
with open('edges_data_new.json', 'w') as f:
    json.dump(edges, f, indent=2)

print("Proceso completado. El archivo edges_data_new.json ha sido creado.")