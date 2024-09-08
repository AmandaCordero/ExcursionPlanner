import heapq
import math

def plan_route(map_data, tourist_preferences):
    
    characteristics = [0,0,0,0,0,0]
    for tourist in tourist_preferences:
        for i in range(6):
            characteristics[i] = characteristics[i]+tourist[i]
    
    for i in range(6):
        characteristics[i] = characteristics[i]/len(tourist_preferences)
    
    return a_star_search(map_data, characteristics)


def a_star_search(map, characteristics):
    
    # Obtener datos de interes del mapa
    start,exit = map.start, map.exit
    interest_points_unvisited = []
    for point in map.interest_points:
        interest_points_unvisited.append(point)

    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = []
    g_score = {start: 0}

    goal = get_goal(start, map, interest_points_unvisited, map.exit, characteristics)
    f_score = {start: heuristic(start, goal, map)}
    temp_came_from = {}
    
    accidently_visits = []
    
    while open_list:
        _, current = heapq.heappop(open_list)
        
        if current in interest_points_unvisited and not current in accidently_visits:
            accidently_visits.append(current)
        
        # De momento la implementación tendrá una unica salida, en un futuro
        # se puede implementar la entrada como una salida también
        if current == exit:
            came_from.append(temp_came_from)
            return reconstruct_path(came_from, current, map)
        elif current == goal:
            # print('accidente: ', accidently_visits)
            for point in accidently_visits:
                # print('voy a eliminar: ', point, ', de la lista: ', interest_points_unvisited, '\n')
                interest_points_unvisited.remove(point)
            accidently_visits = []
            goal = get_goal(goal, map, interest_points_unvisited, map.exit, characteristics)
            came_from.append(temp_came_from)
            temp_came_from = {}
            open_list = []
            g_score = {current: 0}
            f_score = {current: heuristic(current, goal, map)}
        # else:
        #     goal = get_goal(current, map, interest_points_unvisited, goal, characteristics)


        for neighbor in get_neighbors(current, map):
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
            
    return goal

# Valor estimado del punto según los intereses de los turistas
def calculate_point_value(map, point_id, tourists_characteristics):
    point = map.points[point_id]
    value = 0
    
    for i in range(6):
        value += 1000*point.characteristics[i]*(1-abs(point.characteristics[i]-tourists_characteristics[i]))
    
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
            path.append(map.points[current])
    
    path.reverse()

    return path
