from django.shortcuts import render

import json
import statistics
import random
import math

from .statistics import calculate_statistics, calculate_statistics2, calculate_statistics3
from ..modules.module_2.defuzzification_module import compute_fuzzy_output
from ..modules.module_2.module_2_main import Simulation
from ..utils.map_utils import Map
from ..modules.module_1.module_1 import plan_route

def run_simulate(request):

    little = True
    verbose = False

    with open('./myapp/utils/tourists_data.json', 'r') as file:
        tourists = json.load(file)

    map_data = Map()
    
    desires = [person['characteristics'] for person in tourists]

    edges = {}
    edges_size = {}
    points = {}
    for key in map_data.edges.keys():
        edges[key] = map_data.edges[key].characteristics
        edges_size[key] = map_data.edges[key].distance
    
    for key in map_data.points.keys():
        points[key] = map_data.points[key].characteristics

    map = Mapa(points, edges_size, edges=edges)

    simulate = Simulation()

    temperature = 1000
    cooling_rate = 0.99
    std_threshold = 0.05
    min_observations = 10
    
    best_solution = []
    best_cost = None
    cost = None
    cost_history = []
    routes_data = []
    route=[]

    precomputed_data = precompute_excursion_data(desires, map)

    with open('./myapp/utils/simulation.json', 'r') as file:
        simulation_data = json.load(file)

    
    count = 0
    while temperature > 0.1:

        route, temperature, best_solution, best_cost = plan_route(map_data, temperature, cooling_rate, best_solution, best_cost, route, cost)   

        if little or verbose:
            print("#############################################################################")
            print("#############################################################################")
            print(f'                    COMIENZA LA SIMULACION {count}')
            print("#############################################################################")
            print("#############################################################################")
            print(f'Ruta: {route}')
    
        camp_points, reagroup_points,  launch_points, cost = simulate.simulate_excursion(desires, route, map, precomputed_data, verbose, simulation_data)
        cost = cost[0][0]
        cost_history.append(cost)
        
        if little or verbose:
            print(f'Costo: {cost}')

        routes_data.append(route)

        count += 1
        
        # Verifica el criterio de parada si hay suficientes observaciones
        if len(cost_history) >= min_observations:
            std_dev = statistics.stdev(cost_history)
            adjusted_std_dev = std_dev / math.sqrt(len(cost_history))
            mean_cost = statistics.mean(cost_history)
            if adjusted_std_dev < std_threshold * mean_cost:
                break
    
    
    calculate_statistics3(routes_data, filename="routes_stats.png")
    calculate_statistics2(cost_history, filename="costs_stats")
    
    cost_history = []
    camp_points_data = []
    reagroup_points_data = []
    launch_points_data = []
    count = 0
    while True:

        if little or verbose:
            print("#############################################################################")
            print("#############################################################################")
            print(f'                    COMIENZA LA SIMULACION FINAL {count}')
            print("#############################################################################")
            print("#############################################################################")
            print(f'Ruta: {route}')
        
        camp_points, reagroup_points,  launch_points, cost = simulate.simulate_excursion(desires, route, map, precomputed_data, verbose, simulation_data)
        cost = cost[0][0]
        cost_history.append(cost)
        
        if little or verbose:
            print(f'Costo: {cost}')

        camp_points_data.append(camp_points)
        reagroup_points_data.append(reagroup_points)
        launch_points_data.append(launch_points)
        cost_history.append(cost)

        count += 1
        
        # Verifica el criterio de parada si hay suficientes observaciones
        if len(cost_history) >= min_observations:
            std_dev = statistics.stdev(cost_history)
            adjusted_std_dev = std_dev / math.sqrt(len(cost_history))
            mean_cost = statistics.mean(cost_history)
            if adjusted_std_dev < std_threshold * mean_cost:
                break

    if little or verbose:
        print("\n\n\n")
        print(f"Mejor solucion: {best_solution}")
        print(f"Mejor costo: {best_cost}")

    
    with open('./myapp/utils/route_data.json', 'w') as file:
        json.dump(best_solution, file, indent=4)    

    calculate_statistics(camp_points_data, filename="camp_stats")
    calculate_statistics(reagroup_points_data, filename="reagroup_stats")
    calculate_statistics(launch_points_data, filename="launch_stats")

    info = f"{', '.join(best_solution[1:-1])}"
    return render(request, 'run_simulate.html', {'info': info})

def precompute_excursion_data(desires, map):
    # Precompute the waiting times and intentions for each tourist at each point
    precomputed_data = []
    
    for i in range(len(desires)):
        agent_data = {}
        for key, point_data in map.points.items():
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
            agent_data[key] = {
                "waiting_time": waiting_time,
                "beliefs": beliefs
            }
        precomputed_data.append(agent_data)
    
    return precomputed_data

class Mapa:
    def __init__(self, points, edges_size, edges):
        self.points = points
        self.edges_size = edges_size
        self.edges = edges
