from collections import deque
import json
import heapq
import math

class Point:
    def __init__(self, location, height, altitude, characteristics=[]):
        self.characteristics = characteristics  
        self.location = location
        self.height = height
        self.altitude = altitude
    
    def __repr__(self) -> str:
        return 'location: ' + str(self.location) + ' , ' + 'characteristics: ' + str(self.characteristics)

class Map:
    def __init__(self):
        self.start = 0
        self.exit = 58
        self.interest_points = [10,66,19,64,32,38,36,60,53,65,55]
        
        self.points = {}
        self.paths = {}
        self.paths_details = {}
        
        self._create_map()
        
    def _create_map(self):
        self._create_points()
        self._create_paths()
        
    def _create_points(self):
        # Cargamos los datos de los puntos
        with open('./utils/points_data.json', 'r') as file:
            data = json.load(file)
        
        for point in data['points']:
            self.addPoint(point['id'], point['location'], point['height'], point['altitude'], point['characteristics'])
        
    def _create_paths(self):
        # Cargamos los datos de los puntos
        with open('./utils/edges_data.json', 'r') as file:
            data = json.load(file)
        
        for edge in data['edges']:
            self.addPath(edge['point1'], edge['point2'], edge['characteristics'])
    
    def addPoint(self, point_id, location, height, altitude, characteristics=[]):
        if point_id in self.points:
            print("Este punto ya existe.")
            return
        self.points[point_id] = Point(location, height, altitude, characteristics)
        self.paths[point_id] = []  # Inicializar el camino para este punto
        
    def addPath(self, p1, p2, characteristics=[]):
        if p1 not in self.points or p2 not in self.points:
            print("Ambos puntos deben estar definidos con anterioridad.")
            return
        
        if p2 not in self.paths[p1]:
            self.paths[p1].append(p2)
            self.paths[p2].append(p1)
            
            point1 = self.points[p1]
            point2 = self.points[p2]
            
            distance = math.sqrt(abs(point1.location[0]-point2.location[0])**2 + (point1.location[1]-point2.location[1])**2)
            
            self.paths_details[(p1,p2)] = {'distance': distance, 'characteristics':characteristics}
            self.paths_details[(p2,p1)] = {'distance': distance, 'characteristics':characteristics}
        else:
            print(f"El camino entre {p1} y {p2} ya existe.")
           
    def bfs(self, start_point):
        visited = {point: False for point in self.points}
        queue = deque([start_point])
        visited[start_point] = True
        
        while queue:
            current_point = queue.popleft()
            print(current_point)  # Puedes hacer lo que necesites con el punto visitado
            
            for neighbor in self.paths[current_point]:
                if not visited[neighbor]:
                    queue.append(neighbor)
                    visited[neighbor] = True
    
    def dfs(self, start_point):
        visited = {point: False for point in self.points}
        self._dfs_recursive(start_point, visited)
    
    def _dfs_recursive(self, current_point, visited):
        visited[current_point] = True
        print(current_point)  # Puedes hacer lo que necesites con el punto visitado
        
        for neighbor in self.paths[current_point]:
            if not visited[neighbor]:
                self._dfs_recursive(neighbor, visited)
