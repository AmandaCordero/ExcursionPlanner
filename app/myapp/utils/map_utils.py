from collections import deque
import json
import heapq
import math

class Point:
    def __init__(self, location, height, characteristics):
        self.characteristics = characteristics  
        self.location = location
        self.height = height
    
    def __repr__(self) -> str:
        return 'location: ' + str(self.location) + ' , ' + 'characteristics: ' + str(self.characteristics)

class Map:
    def __init__(self):
        self.start = 0
        self.exit = 0
        self.interest_points = []
        
        self.points = {}
        self.paths = {}
        self.paths_details = {}
        
        self._create_map()
        
    def _create_map(self):
        self._create_points()
        self._create_paths()
        
    def _create_points(self):
        # Cargamos los datos de los puntos
        with open('./myapp/utils/points_data.json', 'r') as file:
            data = json.load(file)
        
        for point in data:
            
            if point['begin']:
                self.start = point['point_id']
            elif point['finish']:
                self.exit = point['point_id']
            elif point['interesting']:
                self.interest_points.append(point['point_id'])
            
            self.addPoint(point['point_id'], [point['x'],point['y']], point['height'], point['characteristics'])
        
    def _create_paths(self):
        # Cargamos los datos de los puntos
        with open('./myapp/utils/edges_data.json', 'r') as file:
            data = json.load(file)
        
        for edge in data:
            self.addPath(edge['point1'], edge['point2'], edge['distance'], edge['characteristics'])
    
    def addPoint(self, point_id, location, height, characteristics=[]):
        if point_id in self.points:
            print("Este punto ya existe.")
            return
        self.points[point_id] = Point(location, height, characteristics)
        self.paths[point_id] = []  # Inicializar el camino para este punto
        
    def addPath(self, p1, p2, distance, characteristics=[]):
        if p1 not in self.points or p2 not in self.points:
            print("Ambos puntos deben estar definidos con anterioridad.")
            return
        
        if p2 not in self.paths[p1]:
            self.paths[p1].append(p2)
            self.paths[p2].append(p1)
            
            self.paths_details[(p1,p2)] = {'distance': distance, 'characteristics':characteristics}
            self.paths_details[(p2,p1)] = {'distance': distance, 'characteristics':characteristics}
        else:
            print(f"El camino entre {p1} y {p2} ya existe.")
   
