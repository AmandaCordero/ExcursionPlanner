from django.shortcuts import render

import json

from .statistics import calculate_statistics
from ..modules.module_2.defuzzification_module import compute_fuzzy_output
from ..modules.module_2.module_2_main import Simulation
from ..utils.map_utils import Map
from ..modules.module_1.module_1 import plan_route

def run_simulate(request):

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

    camp_points_data = []
    reagroup_points_data = []
    launch_points_data = []
    
    temperature = 1000
    best_solution = []
    best_cost = None
    route=[]
    cost = None

    precomputed_data = precompute_excursion_data(desires, map)
    
    count = 0
    while temperature > 0.1:
        
        route, temperature, best_solution, best_cost = plan_route(map_data, temperature, best_solution, best_cost, route, cost)   
        
        print("#############################################################################")
        print("#############################################################################")
        print(f'                    COMIENZA LA SIMULACION {count}')
        print("#############################################################################")
        print("#############################################################################")
        camp_points, reagroup_points,  launch_points, cost = simulate.simulate_excursion(desires, route, map, precomputed_data)
        camp_points_data.append(camp_points)
        reagroup_points_data.append(reagroup_points)
        launch_points_data.append(launch_points)

        count += 1

    
    print("\n\n\n")
    print(f"Mejor solucion: {best_solution}")
    print(f"Mejor costo: {best_cost}")

    camp_stats = calculate_statistics(camp_points_data)
    reagroup_stats = calculate_statistics(reagroup_points_data)
    launch_stats = calculate_statistics(launch_points_data)

    info = ""
    info += "Camp Points Data Statistics:"
    for stat, value in camp_stats.items():
        info += f"{stat}: {value}"

    info += "\nReagroup Points Data Statistics:"
    for stat, value in reagroup_stats.items():
        info += f"{stat}: {value}"

    info += "\nLaunch Points Data Statistics:"
    for stat, value in launch_stats.items():
        info += f"{stat}: {value}" 
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
