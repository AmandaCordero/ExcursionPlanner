from collections import deque
import heapq
from sympy import isprime

class Point:
    def __init__(self, location, name="", characteristics=[], IsRest=False):
        self.name = name # puede que el punto tenga un nombre en particular
        self.characteristics = characteristics  # conjunto donde a cada aspecto para los turistas se le asocia un nivel de relevancia
        self.rest = IsRest # lugar de descanso
        self.location = location
    
    # def set_characteristics(self, characteristics):
    #     '''
    #         Permite establecer características del terreno
    #         y su relevancia. 
            
    #         Recibe 'characteristics' que es un array de tuplas (string,num)
    #         donde el primer elemento es el nombre de la característica y el segundo
    #         es el nivel de relevancia.
    #     '''
        
    #     for characteristic in characteristics:
    #         self.characteristics.append((characteristic[0],characteristic[1]))

class Map:
    def __init__(self):
        self.len_map = 15
        self.points = {}
        self.interest_points = [28,60,74,121,155,147,196,214]
        self.start = 0
        self.exit = 224
        
        self.paths = {}
        self.slope = {}
        self.size = {}
        
        self.createmap()
        self.createpoints()

    def createmap(self):
        # Inicializar toda la matriz con 0
        self.map_matrix = [[j*self.len_map+i for i in range(self.len_map)] for j in range(self.len_map)]
        self._block_generate()

        for i in range(self.len_map):
            for j in range(self.len_map):
                if self.map_matrix[i][j] != -1:
                    self.points[self.map_matrix[i][j]] = Point((i,j))

    def _block_generate(self):
        # Generando obstáculos
        
        for i in range(self.len_map):
            for j in range(self.len_map):

                if j > 11 and self.map_matrix[i][j] != 0 and self.map_matrix[i][j] % 6 == 0:
                    self.map_matrix[i][j] = -1
                
                if j <= 11 and self.map_matrix[i][j] != 0 and self.map_matrix[i][j] % 9 == 0:
                    self.map_matrix[i][j] = -1

                if isprime(self.map_matrix[i][j]):
                    self.map_matrix[i][j] = -1
                
                if abs(5-i) < 3 and abs(11-j) < 2:
                    self.map_matrix[i][j] = -1

                if i == 12 and abs(2-j) < 4:
                    self.map_matrix[i][j] = -1
        
    def createpoints(self):
        for i in range(15):
            for j in range(15):
                element = self.map_matrix[i][j]
                if element == -1:
                    continue
                else:
                    self.points[element] = Point((i,j))

        # Establecer las características a los puntos de interés
        # Las puntuaciones irán de 1 a 10
        # interest_points = [28,60,74,121,155,147,196,214]
        self.points[28].characteristics = [('A',10)]
        self.points[60].characteristics = [('A',5)]
        self.points[74].characteristics = [('C',10)]
        self.points[121].characteristics = [('B',7)]
        self.points[155].characteristics = [('B',4)]
        self.points[147].characteristics = [('C',3)]
        self.points[196].characteristics = [('B',10)]
        self.points[214].characteristics = [('A',9)]
        
    def __repr__(self):
        rows = []
        for i in range(self.len_map):
            columns = []
            for j in range(self.len_map):
                element = ''
                num = str(self.map_matrix[i][j])
                if num == '-1':
                    num = ' # '
                if len(num) == 1:
                    num = '  ' + num
                if len(num) == 2:
                    num = ' ' + num
                
                columns.append(num)
            
            rows.append(' '.join(a for a in columns))

        return '\n'.join(row for row in rows)





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

    def heuristic(self, n1, n2):
        # Esta es una heurística simple, puedes ajustarla según tus necesidades
        # Por ejemplo, podría ser la distancia euclidiana, Manhattan, etc.
        return abs(n1.x - n2.x) + abs(n1.y - n2.y)

    def a_star(self, start_point, goal_point):
        open_list = [(0, start_point)]
        came_from = {}
        g_score = {point: float('inf') for point in self.points}
        g_score[start_point] = 0
        f_score = {point: float('inf') for point in self.points}
        f_score[start_point] = self.heuristic(start_point, goal_point)

        while open_list:
            _, current_point = heapq.heappop(open_list)

            if current_point == goal_point:
                path = [current_point]
                while current_point in came_from:
                    current_point = came_from[current_point]
                    path.append(current_point)
                path.reverse()
                return path

            for neighbor in self.paths[current_point]:
                tentative_g_score = g_score[current_point] + self.size[(current_point, neighbor)]
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_point
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal_point)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

        return None  # No se encontró camino