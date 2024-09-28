import json
from map_utils.points.point_utils import Point
from map_utils.edges.edge_utils import Edge
import matplotlib.pyplot as plt
import networkx as nx
import random
from map_utils.utils.random_variables import get_lower_number
import math

class Map:
    def __init__(self):
        self.starts = [] # Puntos de entrada del mapa
        self.exits = [] # Puntos de salida del mapa
        self.map_cost = 1.2 # Costo de recorrer el mapa debido a condiciones del lugar o de los turistas
        
        self.points = {} # Diccionario con la información de cada punto {id:Point}
        self.paths = {} # Diccionario con los caminos desde un punto {Point:Point[]}
        self.edges = {} # Diccionario con la información de cada camino {(Point,Point):Edge}
        
        self._create_map()
        
    def _create_map(self):
        self._create_points()
        self._create_paths()
        
    def _create_points(self):
        # Cargamos los datos de los puntos
        with open('./myapp/utils/points_data.json', 'r') as file:
            data = json.load(file)
        
        for point in data:
            if point['type'] == 'begin': # Verificar si es un punto de entrada
                self.starts.append(point['point_id'])
            elif point['type'] == 'finish': # Verificar si es un punto de salida
                self.exits.append(point['point_id'])
            
            self.addPoint(point['point_id'], (point['location'][0],point['location'][1]), point['height'], point['characteristics'])
        
    def _create_paths(self):
        # Cargamos los datos de los puntos
        with open('./myapp/utils/edges_data.json', 'r') as file:
            data = json.load(file)
        
        
        for edge in data:
            self.addPath(edge['point1'], edge['point2'], edge['distance'], edge['characteristics'])
    
    def addPoint(self, point_id, location, height, characteristics=None):
        if point_id in self.points:
            print("Este punto ya existe.")
            return
        self.points[point_id] = Point(point_id,location,height,characteristics)
        self.paths[point_id] = []  # Inicializar el camino para este punto
        
    def addPath(self, p1, p2, distance, characteristics=None):
        if p1 not in self.points or p2 not in self.points:
            print("Ambos puntos deben estar definidos con anterioridad.")
            return
        
        if p2 not in self.paths[p1]:
            self.paths[p1].append(p2)
            self.paths[p2].append(p1)
            
            self.edges[(p1,p2)] = Edge(p1,p2,distance, characteristics)
            self.edges[(p2,p1)] = self.edges[(p1,p2)]
        else:
            print(f"El camino entre {p1} y {p2} ya existe.")
   
    def update_map_conditions(self):
        # Actualizar el costo de caminar por el mapa
        if random.random() < 0.3:
            self.cost = 1 + get_lower_number()
   
    def get_cost(self, point1, point2, tourist_characteristics):
        # Obtener el puntaje de las caracteristicas del camino
        edge_characteristics = self.edges[(point1, point2)].characteristics
        point_characteristics = self.points[point2].characteristics
        
        # Información del camino
        distance = self.edges[(point1, point2)].distance
        elevation = self.points[point2].height - self.points[point1].height
        

        # Coeficiente referente a las preferencias de los turistas
        tourist_coef = 0
        for tourist in tourist_characteristics:
            for i in range(6):
                tourist_coef += 1 - abs(tourist[i]-edge_characteristics[i])
                tourist_coef += 1 - abs(tourist[i]-point_characteristics[i])
        tourist_coef = tourist_coef/(12*len(tourist_characteristics))
        
        distance_cost = math.sqrt(distance**2 + elevation**2)
        if distance_cost:
            cost = self.map_cost * tourist_coef * distance_cost
        else:
            cost = 0
            
        # Actualizar las condiciones del mapa
        self.update_map_conditions()
        return cost
    
    def view_map(self, save=False):        
        # Cargamos los datos de los puntos
        with open('./map_utils/points/points_data.json', 'r') as file:
            points = json.load(file)
        
        # Cargamos los datos de los puntos
        with open('./map_utils/edges/edges_data.json', 'r') as file:
            edges = json.load(file)
        
        # Crear el grafo
        G = nx.Graph()

        # Añadir nodos
        for point in points:
            G.add_node(point["point_id"], pos=(point["location"][0], point["location"][1]), type=point["type"])

        # Añadir aristas
        for edge in edges:
            G.add_edge(edge["point1"], edge["point2"], weight=edge["distance"])

        # Obtener posiciones de los nodos
        pos = nx.get_node_attributes(G, 'pos')

        # Definir colores según el tipo de nodo
        color_map = []
        for node in G.nodes(data=True):
            if node[1]['type'] == 'begin':
                color_map.append('green')
            elif node[1]['type'] == 'middle':
                color_map.append('blue')
            elif node[1]['type'] == 'finish':
                color_map.append('red')

        # Dibujar nodos con colores según el tipo
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color=color_map)

        # Dibujar aristas
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2)

        # Etiquetas de los nodos
        labels = {point["point_id"]: f'{point["point_id"]}' for point in points}
        nx.draw_networkx_labels(G, pos, labels, font_size=9, font_color='white')

        # Etiquetas de las aristas
        edge_labels = {(edge["point1"], edge["point2"]): edge["distance"] for edge in edges}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.title("Visualización del Mapa")
        # Ajusta el tamaño de la figura actual
        plt.gcf().set_size_inches(12, 8)
        if save:
            plt.savefig('./map_view.jpg', format='jpg', dpi=300)

        # Mostrar el grafo
        plt.show()