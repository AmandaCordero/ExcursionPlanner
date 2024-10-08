import heapq
import random
import math

def plan_route(map_data, temperature, cooling_rate, best_solution, best_cost, last_route, cost):    
    """
    Planifica una ruta basada en las preferencias de los turistas y características del mapa.
    Implementa un criterio de parada basado en la desviación estándar de los costos recientes, ajustada por la raíz del número de observaciones.

    Args:
        map_data (object): Datos del mapa, incluyendo información sobre puntos de interés y caminos.
        temperature (float): Temperatura inicial para el proceso de Simulated Annealing.
        cooling_rate (float): Tasa de enfriamiento para reducir gradualmente la temperatura.
        best_solution (list): La mejor solución encontrada hasta el momento.
        best_cost (float): El costo asociado a la mejor solución encontrada.
        last_route (list): La última ruta generada.
        cost (float): El costo de la última ruta generada.
        std_threshold (float): Umbral ajustado de desviación estándar para el criterio de parada.
        min_observations (int): Mínimo número de observaciones necesarias para calcular la desviación estándar.

    Returns:
        tuple: Una tupla con la ruta generada, la temperatura actualizada, la mejor solución y el mejor costo.
    """

    if not last_route:
        return generate_minimal_solution(map_data), temperature, best_solution, best_cost
    elif not best_solution:
        best_solution = last_route
        best_cost = cost
        return generate_neighbor_solution(map_data, last_route), temperature, best_solution, best_cost

    cost_diff = cost - best_cost
    if cost_diff < 0 or random.uniform(0, 1) < math.exp(-cost_diff / temperature):

        if cost < best_cost:
            best_solution = last_route
            best_cost = cost

    temperature *= cooling_rate
    last_route = generate_neighbor_solution(map_data, last_route)  # Genera la nueva ruta

    return last_route, temperature, best_solution, best_cost

# Dijkstra
def generate_minimal_solution(graph, initial_nodes=[], exclude_node=None):
    # Inicialización
    distances = {node.id: float('infinity') for node in graph.points.values()}
    
    if initial_nodes == []:
        initial_nodes = graph.starts
    
    for initial_node in initial_nodes:
        distances[initial_node] = 0
        priority_queue = [(0, initial_node)]
    
    predecessors = {node.id: None for node in graph.points.values()}
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor in graph.paths[current_node]:

            if exclude_node and neighbor==exclude_node:
                continue
            
            distance = current_distance + graph.edges[(current_node,neighbor)].distance
                        
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    min_end_cost = float('infinity')
    end = None
    for node_end in graph.exits:
        if distances[node_end] < min_end_cost:
            end = node_end
            min_end_cost = node_end
    
    # Reconstruir el camino
    path = []
    current_node = end
    while current_node is not None:
        path.append(current_node)
        current_node = predecessors[current_node]
    path = path[::-1]  # Invertir el camino
    
    return path

def generate_neighbor_solution(graph, solution):
    num = random.random()
    if num < 0.5:
        return generate_neighbors_by_add(graph,solution)
    else:
        return generate_neighbors_by_delete(graph,solution)

def generate_neighbors_by_add(graph, path):
    for node in path:
        if node == path[len(path)-1]:
            break
        for neighbor in graph.paths[node]:
            if neighbor not in path:
                new_path = []
                for point in path:
                    if point == node:
                        new_path.append(point)
                        new_path.append(neighbor)
                    else: 
                        new_path.append(point)
                if is_valid_path(graph, new_path):
                    return new_path
    
    copy_path = []
    for item in path:
        copy_path.append(item)
    
    
    for _ in range(len(path)):
        selected_point = random.choice(copy_path)

        if all(isNextinPath(path,selected_point,neighbor) for neighbor in graph.paths[selected_point]):
            copy_path.remove(selected_point)
            continue
        
        for neighbor in graph.paths[selected_point]:
            if neighbor not in path:
                begin_solution = []
                for point in path:
                    begin_solution.append(point)
                    if point == selected_point:
                        break
                return begin_solution + generate_minimal_solution(graph, [neighbor], selected_point)
        
    return None

def generate_neighbors_by_delete(graph, path):
    
    for node in path:
        if node == path[len(path)-1] or node==path[0]:
            break
    
        new_path = []
        for point in path:
            if point == node:
                continue
            else: 
                new_path.append(point)
        if is_valid_path(graph, new_path):
                return new_path
            
    copy_path = []
    for item in path:
        copy_path.append(item)
    
    for _ in range(len(path)):
        selected_point = random.choice(copy_path)
        if selected_point==path[0] or selected_point==path[len(path)-1]:
            copy_path.remove(selected_point)
            continue
        
        begin_solution = []
        for point in path:
            if point == selected_point:
                break
            begin_solution.append(point)
        
        start = begin_solution[len(begin_solution)-1]

        rest = generate_minimal_solution(graph, [start], selected_point)

        if len(rest) == 0:
            copy_path.remove(selected_point)
            continue
            
        return begin_solution[0:len(begin_solution)-1] + rest
        
    return None



def is_valid_path(graph, path):
    for i in range(len(path) - 1):
        if path[i+1] not in graph.paths[path[i]]:
            return False
    return True

def isNextinPath(path,node,neightbor):
    
    if len(path)==1:
        return False
    
    for i in range(len(path)):
        if path[i] != node:
            continue
        
        if i==0:
            if path[1]==neightbor:
                return True
            else:
                return False
        
        if i == len(path)-1:
            if path[len(path)-2]== neightbor:
                return True
            else:
                return False
        
        if path[i]==node:
            if path[i-1]==neightbor or path[i+1]==neightbor:
                return True
            else:
                return False
    
    return False


