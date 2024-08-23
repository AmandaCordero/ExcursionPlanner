import heapq

def plan_route(map_data, characteristics):
    
    # characteristics: 
    characteristics = {'A': (1, 24), 'B': (4, 14)}
    
    #  map_data.map_matrix:
    #    0    1   #    #    4    #    6    #     8   #    10   #    #    #    14
    #   15   16   #    #    #    20   21   22   #    24   25   26   27  (28)  #
    #   30   #    32   33   34   35   #    #    38   39   40   #    #    #    44
    #   #    46   #    48   49   50   51   52   #    #    #    #    #    58   #
    #  (60)  #    62   #    64   65   66   #    68   69   #    #    #    #   (74)
    #   75   76   77   78   #    80   #    82   #    84   #    #    #    88   #
    #   #    91   92   93   94   95   96   #    98   #    #    #    #    #   104
    #  105  106   #    #    #   110  111  112   #   114   #    #    #   118  119
    #  120 (121) 122  123  124  125   #    #   128  129  130   #    #   133  134
    #   #   136   #   138   #   140  141  142  143   #   145  146 (147) 148   #
    #  150   #   152   #   154 (155) 156   #   158  159  160  161   #    #   164
    #  165  166   #   168  169  170   #   172   #   174  175  176  177  178   #
    #   #    #    #    #    #    #   186  187  188   #   190   #    #    #   194
    #  195 (196)  #    #    #   200  201  202  203  204  205  206  207  208  209
    #  210   #   212  213 (214) 215   #   217  218  219  220  221   #    #   224

    return a_star_search(map_data, characteristics)




def a_star_search(map, characteristics):
    
    # Obtener datos de interes del mapa
    start,exit = map.start, map.exit
    rows, cols = len(map.map_matrix), len(map.map_matrix[0])
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
        
        if current in interest_points_unvisited:
            accidently_visits.append(current)
        
        # De momento la implementación tendrá una unica salida, en un futuro
        # se puede implementar la entrada como una salida también
        if current == exit:
            came_from.append(temp_came_from)
            return reconstruct_path(came_from, current)
        elif current == goal:
            for point in accidently_visits:
                interest_points_unvisited.remove(point)
            accidently_visits = []
            goal = get_goal(goal, map, interest_points_unvisited, map.exit, characteristics)
            came_from.append(temp_came_from)
            temp_came_from = {}
            open_list = []
            g_score = {current: 0}
            f_score = {current: heuristic(current, goal, map)}
        else:
            goal = get_goal(current, map, interest_points_unvisited, goal, characteristics)

        for neighbor in get_neighbors(current, map, rows, cols):
            # Check si es un obstáculo
            if neighbor == -1:
                continue
            
            location_current = map.points[current].location
            location_neighbor = map.points[neighbor].location
            tentative_g_score = g_score[current] + 2
            # Revisar si el movimiento es en diagonal
            if location_current[0] != location_neighbor[0] and location_current[1] != location_neighbor[1]:
                tentative_g_score = g_score[current] + 2.27

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

def calculate_point_value(map, point_id, tourists_characteristics):
    point = map.points[point_id]
    value = 0
    for charecteristic in point.characteristics:
        if charecteristic[0] in tourists_characteristics:
            # El valor para cada característica se obtiene multiplicando el valor que
            # le dan los turisticas y la relevancia del sitio
            value += tourists_characteristics[charecteristic[0]][0]*charecteristic[1]
    return value
    
def heuristic(start, end, map):
    a = map.points[start].location
    b = map.points[end].location
    return max(abs(a[0] - b[0]),abs(a[1] - b[1]))

def get_neighbors(point, map, rows, cols):
    location = map.points[point].location
    neighbors = []
    for dx, dy in [(1, 0), (1,1), (0, 1), (-1,1), (-1,0), (-1,-1), (0, -1), (1,-1)]:
        x, y = location[0] + dx, location[1] + dy
        if 0 <= x < rows and 0 <= y < cols:
            neighbors.append(map.map_matrix[x][y])
    return neighbors

def reconstruct_path(came_from, current):
    came_from.reverse()
    
    path = [current]
    
    for parent_dic in came_from:
        while current in parent_dic:
            current = parent_dic[current]
            path.append(current)
    
    path.reverse()

    return path

# # Ejemplo de uso
# grid = [
#     [0, 1, 0, 0, 0],
#     [0, 1, 0, 1, 0],
#     [0, 0, 0, 0, 0],
#     [0, 1, 1, 1, 0],
#     [0, 0, 0, 1, 0]
# ]

# start = (0, 0)
# goal = (4, 4)
# path = a_star_search(grid, start, goal)
# print("Camino encontrado:", path)