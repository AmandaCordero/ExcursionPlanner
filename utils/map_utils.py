from collections import deque
import heapq
import math

class Map:
    def __init__(self):
        self.points = []
        self.paths = {}
        self.slope = {}
        self.size = {}
        
    def addPoint(self, point):
        if point in self.points:
            print("Este punto ya existe.")
            return
        self.points.append(point)
        self.paths[point] = []  # Inicializar el camino para este punto
        
    def addPath(self, p1, p2, slope, size):
        if p1 not in self.points or p2 not in self.points:
            print("Ambos puntos deben estar definidos con anterioridad.")
            return
        
        if p2 not in self.paths[p1]:
            self.paths[p1].append(p2)
            self.slope[(p1, p2)] = slope
            self.size[(p1, p2)] = size
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
