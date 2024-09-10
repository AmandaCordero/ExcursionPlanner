import heapq
import math

def plan_route(map_data, tourist_preferences):
    """
    Planifica una ruta basada en las preferencias de los turistas y características del mapa.

    Args:
        map_data (object): Datos del mapa, incluyendo información sobre puntos de interés y caminos.
        tourist_preferences (list): Lista de preferencias de los turistas, donde cada elemento es una lista de 6 valores.

    Returns:
        list: Ruta planificada utilizando A* Search.

    Note:
        Este método utiliza A* Search para encontrar la mejor ruta considerando las preferencias de los turistas,
        las características de los puntos de interés y la topografía del mapa.
    """
    
    # Calcular el promedio por cada caracteristica de todos los turistas
    characteristics = [0,0,0,0,0,0]
    for tourist in tourist_preferences:
        for i in range(6):
            characteristics[i] = characteristics[i]+tourist[i]
    for i in range(6):
        characteristics[i] = characteristics[i]/len(tourist_preferences)
    
    # Calcular la mejor ruta con A*
    return a_star_search(map_data, characteristics)


def a_star_search(map, characteristics):
    
    # Obtener datos de interes del mapa
    start,exit = map.start, map.exit
    
    # Hacer una copia de los puntos de interés para ir descartando los visitados
    interest_points_unvisited = []
    for point in map.interest_points:
        interest_points_unvisited.append(point)

    # Crear la cola de prioridad para extraer en cada momento el que menor valor de f_score tenga
    open_list = []
    heapq.heappush(open_list, (0, start))
        
    # Diccionario que indica de cada nodo descubierto cuál es su nodo padre
    temp_came_from = {}
    
    # Contiene todos los diccionarios temp_came_from para cada A* hecho por cada objetivo
    came_from = []
    
    # Costos ya recorridos
    g_score = {start: 0}
    
    # Definir el primer objetivo entre todos los puntos de interés
    goal = get_goal(start, map, interest_points_unvisited, map.exit, characteristics)
    
    # Costo general de un camino teniendo en cuenta el costo recorrido y la heurística
    f_score = {start: heuristic(start, goal, map)}
    
    # Puntos de interés visitados a pesar de no ser objetivos para luego extraerlos de los puntos a visitar
    accidently_visits = []
    
    while open_list:
        
        _, current = heapq.heappop(open_list)
        
        # Checkear si el punto visitado es un punto de interés
        if current in interest_points_unvisited and not current in accidently_visits:
            accidently_visits.append(current)
        
        
        if current == exit and goal == exit:
            
            # En este punto se supone que concluyó el algoritmo
            came_from.append(temp_came_from)
            return reconstruct_path(came_from, current, map)
        
        elif current == goal:
            
            # Se extraen los puntos de interés accidentalmente visitados
            for point in accidently_visits:
                interest_points_unvisited.remove(point)
            accidently_visits = []
            
            # Se selecciona un nuevo punto objetivo
            goal = get_goal(goal, map, interest_points_unvisited, map.exit, characteristics)

            # Se prepara el diccionario de parents
            came_from.append(temp_came_from)
            temp_came_from = {}
            
            # Se toma un nuevo registro de valores de g y f para los puntos a partir de este
            open_list = []
            g_score = {current: 0}
            f_score = {current: heuristic(current, goal, map)}
        # else:
        #     goal = get_goal(current, map, interest_points_unvisited, goal, characteristics)


        for neighbor in get_neighbors(current, map):
            # Se calcula el costo hasta este nuevo vecino
            tentative_g_score = g_score[current] + heuristic(current, neighbor, map)

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                temp_came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal, map)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None

def get_goal(start, map, interest_points_unvisited, default_goal, characteristics):
    min_f,goal = heuristic(start, default_goal, map), default_goal
    for point in interest_points_unvisited:
        path_to_point_f = 0
        
        path_to_point_f = heuristic(start, point, map) + heuristic(point, default_goal, map) - calculate_point_value(map, point, characteristics)
        
        if path_to_point_f < min_f:
            goal = point
            min_f = path_to_point_f
    print('goal: ', goal)
    return goal

# Valor estimado del punto según los intereses de los turistas
def calculate_point_value(map, point_id, tourists_characteristics):
    point = map.points[point_id]
    value = 0
    
    for i in range(6):
        if point.characteristics[i] == 0 or tourists_characteristics[i] == 0:
            continue
        value += 1000*(1-abs(point.characteristics[i]-tourists_characteristics[i]))
    
    return value
    
# Costo estimado para ir de un punto a otro (sean adyacentes o no)
def heuristic(start, end, map):
    if start == end:
        return 0
    
    point1 = map.points[start]
    point2 = map.points[end]
    
    # Esta es la distancia que separa en el plano a los dos puntos sin tener en cuenta la altura
    distance = math.sqrt(abs(point1.location[0]-point2.location[0])**2 + (point1.location[1]-point2.location[1])**2)
    
    # Calcular la distancia de subida que hay entre los puntos
    elevation = 0
    if point1.altitude == "hill_one" and (point2.altitude == 'hill_two' or point2.altitude == 'top'):
        elevation = point2.height - 60
    elif (point1.altitude == 'hill_two' or point1.altitude == 'top') and point2.altitude == "hill_one":
        elevation = point2.height - 60
    else:
        elevation = point2.height - point1.height
    
    # Calculamos la distancia real entre los puntos teniendo en cuenta la altura
    real_distance = math.sqrt(distance**2 + elevation**2)
    
    cost = 0
    if elevation <= 0:
        cost = real_distance * (1-elevation/distance)
    else:
        cost = real_distance * (1+elevation/distance)
    
    return cost

# Obtener los puntos adyacentes al punto analizado
def get_neighbors(point_id, map):
    neighbors = []
    for neighbor in map.paths[point_id]:
            neighbors.append(neighbor)
    return neighbors

# Reconstruir el camino desde el inicio hasta el final
def reconstruct_path(came_from, current, map):
    came_from.reverse()
    
    path = [current]
    
    for parent_dic in came_from:
        while current in parent_dic:
            current = parent_dic[current]
            # path.append(map.points[current])
            path.append(current)
    
    path.reverse()

    return path
