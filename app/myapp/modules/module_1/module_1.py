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
    """
    Implementa el algoritmo A* Search para encontrar la ruta que aporte más satisfacción según los intereses de los turistas.

    Args:
        map (object): Datos del mapa, incluyendo información sobre puntos de interés y caminos.
        characteristics (list): Resumen de los intereses de los turistas. 

    Returns:
        (list): Lista con los puntos (Point) en el orden de la ruta escogida, None si no se puede encontrar

    Note:
        Este método utiliza una búsqueda A* para encontrar la ruta óptima considerando:
        1. La estructura del grafo del mapa
        2. El punto de inicio
        3. Los intereses de los turistas
        3. La función heurística utilizada para guiar la búsqueda
        4. Las propiedades de los puntos y caminos en el mapa, además de la distancia
    """
    
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
    
    # Comtiene los puntos de interés visitados
    goals = []
    
    # Definir el primer objetivo entre todos los puntos de interés
    goal = get_goal(start, map, interest_points_unvisited, map.exit, characteristics)
    if goal != exit:
        goals.append(goal)
    
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
            return reconstruct_path(came_from, current, map), goals
        
        elif current == goal:
            
            # Se extraen los puntos de interés accidentalmente visitados
            for point in accidently_visits:
                interest_points_unvisited.remove(point)
            accidently_visits = []
            
            # Se selecciona un nuevo punto objetivo
            goal = get_goal(goal, map, interest_points_unvisited, map.exit, characteristics)
            if goal != exit:
                goals.append(goal)

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
            
            if map.paths_details[(current,neighbor)]['characteristics'][0]==0 and map.paths_details[(current,neighbor)]['characteristics'][1] == 0:
                coeficient_tourists_like = 1
            else:
                coeficient_tourists_like = abs(map.paths_details[(current,neighbor)]['characteristics'][0]-characteristics[0])
                coeficient_tourists_like += abs(map.paths_details[(current,neighbor)]['characteristics'][1]-characteristics[1])
                coeficient_tourists_like = coeficient_tourists_like/2
            
            # Se calcula el costo hasta este nuevo vecino
            tentative_g_score = g_score[current] + (1+coeficient_tourists_like)*map.paths_details[(current,neighbor)]['distance']

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                temp_came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal, map)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None

def get_goal(start, map, interest_points_unvisited, default_goal, characteristics):
    """
    Determina el próximo objetivo de la excursión basándose en las preferencias de los turistas y características del mapa.

    Args:
        start (num): Id del punto actual
        map (object): Datos del mapa, incluyendo información sobre puntos de interés y caminos.
        interest_points_unvisited (list): Puntos de interés del mapa que aún no han sido visitados.
        default_goal (num): Id del punto objetivo por defecto (generalmente la salida del mapa)
        characteristics (list): Lista de preferencias resumidas de los turistas

    Returns:
        goal: Id del punto de interés seleccionado como objetivo.

    Note:
        Este método utiliza la función heurística para evaluar la atracción de cada punto de interés
        basada en las preferencias del turista y las características del mapa.
        El objetivo final es el punto de interés que maximiza la atracción según estas consideraciones.

    Raises:
        ValueError: Si no se puede encontrar un punto de interés adecuado basándose en las preferencias del turista
    """
    
    min_f,goal = heuristic(start, default_goal, map), default_goal
    
    for point in interest_points_unvisited:
        
        path_to_point_f = heuristic2(start, point, default_goal, characteristics, map)
        
        if path_to_point_f < min_f:
            goal = point
            min_f = path_to_point_f
            
    return goal
    
def heuristic(start, end, map):
    """
    Calcula el costo aproximado entre dos puntos en el mapa.

    Args:
        start (num): Id del punto inicial del recorrido
        end (num): Id del punto final del recorrido
        map (object): Datos del mapa, incluyendo información sobre puntos de interés y caminos.

    Returns:
        cost: Costo estimado en el recorrido según la heurística utilizada

    Note:
        Esta función calcula la heurística utilizando la fórmula de Euclides para la distancia entre ambos puntos.
        Además tiene en cuenta la pendiente del recorrido para calcular el costo.
    """
    
    if start == end:
        return 0
    
    point1 = map.points[start]
    point2 = map.points[end]
    
    # Esta es la distancia entre los dos puntos sin tener en cuenta la altura
    distance = math.sqrt(abs(point1.location[0]-point2.location[0])**2 + (point1.location[1]-point2.location[1])**2)
    
    # Diferencia de altura entre ambos puntos
    elevation = point2.height - point1.height
    
    # Calculamos la distancia real entre los puntos teniendo en cuenta la altura
    real_distance = math.sqrt(distance**2 + elevation**2)
    
    cost = 0
    if elevation <= 0:
        cost = real_distance * (1-elevation/distance)
    else:
        cost = real_distance * (1+elevation/distance)
    
    return cost

def heuristic2(start, midpoint, end, characteristics, map):
    """
    Calcula el costo aproximado entre dos puntos en el mapa pasando por un punto intermedio.

    Args:
        start (num): Id del punto inicial del recorrido
        midpoint (num): Id del punto intermedio del recorrido
        end (num): Id del punto final del recorrido
        characteristics (list): Características de los turistas
        map (object): Datos del mapa, incluyendo información sobre puntos de interés y caminos.

    Returns:
        Costo estimado en el recorrido según la heurística utilizada

    Note:
        Esta función utiliza la función heuristic con la peculiaridad de que se tiene en cuenta
        los "beneficios" de pasar por el punto midpoint según los intereses de los turistas.

    """
    
    # Calcular el valor de este punto
    point = map.points[midpoint]
    value = 0
    for i in range(4):
        if point.characteristics[i] == 0 or characteristics[i+2] == 0:
            continue
        value += 1000*(1-abs(point.characteristics[i]-characteristics[i+2]))
        
    return heuristic(start, midpoint, map) + heuristic(midpoint, end, map) - value

def get_neighbors(point_id, map):
    """
    Obtiene los puntos adyacentes a un punto en el mapa

    Args:
        point_id (num): Id del punto a analizar
        map (object): Datos del mapa, incluyendo información sobre puntos de interés y caminos.


    Returns:
        neighbors: Lista de vecinos del nodo especificado
    """
    
    neighbors = []
    for neighbor in map.paths[point_id]:
            neighbors.append(neighbor)
    return neighbors

def reconstruct_path(came_from, current, map):
    """
    Reconstruye el camino completo desde el punto inicial hasta el objetivo final teniendo en cuenta el array came_from.

    Args:
        came_from (list): Array con los diccionarios que guardan los datos de un punto objetivo a otro de los puntos y por qué punto fue descubierto en el algoritmo.
        current (tuple): Coordenadas actuales del nodo actual.

    Returns:
        path (list): Puntos que forman el camino completo desde el punto inicial al final del mapa.

    Note:
        El array came_from contiene diccionarios con la información de los puntos descubiertos desde el punto inicio o desde un punto objetivo al próximo.
        Como se tiene el punto final del mapa para conformar el camino se formará inicialmente el camino al revés, y una vez se llegue a un punto que no se
        encuentre en el diccionario se supone que pertenezca al camino entre el par de objetivos anteriores.
    """
    
    came_from.reverse()
    
    path = [current]
    
    for parent_dic in came_from:
        while current in parent_dic:
            current = parent_dic[current]
            # path.append(map.points[current])
            path.append(current)
    
    path.reverse()

    return path
