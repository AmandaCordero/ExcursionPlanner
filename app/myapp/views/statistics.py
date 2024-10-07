
import json
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

def calculate_statistics(simulations, filename='scatter_plot.png'):

    # Crear una lista de todos los puntos únicos
    unique_points = sorted(set(point for simulation in simulations for point in simulation))

    # Crear una matriz para el scatter plot
    scatter_data = []
    for sim_idx, simulation in enumerate(simulations):
        for point in simulation:
            scatter_data.append([sim_idx, unique_points.index(point)])

    # Convertir a array
    scatter_data = np.array(scatter_data)

    # Crear el scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(scatter_data[:, 1], scatter_data[:, 0], c='blue', alpha=0.6, s=100)

    # Etiquetas y configuraciones del gráfico
    plt.xticks(ticks=range(len(unique_points)), labels=unique_points)
    plt.xlabel('Puntos en el mapa')
    plt.ylabel('Simulaciones')
    plt.title('Distribución de puntos por simulación')

    # Guardar la imagen
    plt.savefig(filename)
    plt.close()

def calculate_statistics2(costs, filename='costs_plot.png'):
    
    # Crear un array de índices para las simulaciones
    simulations_idx = np.arange(len(costs))

    # Crear el gráfico de dispersión de los costos
    plt.figure(figsize=(10, 6))
    plt.scatter(simulations_idx, costs, c='blue', alpha=0.6, s=100)

    # Etiquetas y configuraciones del gráfico
    plt.xticks(ticks=simulations_idx, labels=[f'Simulación {i+1}' for i in simulations_idx])
    plt.xlabel('Simulaciones')
    plt.ylabel('Costo')
    plt.title('Costo por simulación')

    # Guardar la imagen
    plt.savefig(filename)
    plt.close()


def calculate_statistics3(simulations, filename='map_with_routes.svg'):
    # Cargar los datos
    with open('./myapp/utils/points_data.json', 'r') as file1:
        points = json.load(file1)
        
    with open('./myapp/utils/edges_data.json', 'r') as file2:
        edges = json.load(file2)

    # Crear el grafo
    G = nx.Graph()

    # Añadir nodos al grafo
    for point in points:
        G.add_node(point['point_id'])

    # Añadir aristas y contadores de uso
    edge_count = {}
    for edge in edges:
        point1 = edge['point1']
        point2 = edge['point2']
        G.add_edge(point1, point2, distance=edge['distance'])
        edge_count[(point1, point2)] = 0

    # Contar la cantidad de veces que cada arista es usada en las simulaciones
    for simulation in simulations:
        for i in range(len(simulation) - 1):
            point1 = simulation[i]
            point2 = simulation[i + 1]
            if (point1, point2) in edge_count:
                edge_count[(point1, point2)] += 1
            elif (point2, point1) in edge_count:  # Aristas no dirigidas
                edge_count[(point2, point1)] += 1

    # Obtener el valor máximo de uso para normalizar los colores
    max_usage = max(edge_count.values()) if edge_count.values() else 1

    # Utilizar un layout automático de NetworkX (spring_layout) con más iteraciones y mayor separación
    pos = nx.spring_layout(G, k=5, iterations=200)

    # Dibujar el grafo con caminos
    plt.figure(figsize=(10, 6))
    
    # Dibujar los nodos
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue')

    # Colormap para las aristas
    cmap = cm.get_cmap('Reds')  # Escala de colores desde el más claro al más oscuro (rojo)
    
    # Dibujar las aristas con colores basados en el uso
    for edge in G.edges():
        point1, point2 = edge
        weight = edge_count.get((point1, point2), 0) + edge_count.get((point2, point1), 0)
        
        # Normalizar el peso para obtener un valor entre 0 y 1
        normalized_weight = weight / max_usage
        
        # Obtener el color basado en la cantidad de uso
        edge_color = cmap(normalized_weight)
        
        # Dibujar la arista con el color correspondiente
        nx.draw_networkx_edges(G, pos, edgelist=[(point1, point2)], width=2, edge_color=[edge_color])

    # Dibujar etiquetas de los nodos
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')

    # Guardar la imagen en formato SVG
    plt.savefig(filename, format='png', dpi=300, bbox_inches='tight')
    plt.close()