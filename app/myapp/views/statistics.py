import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def calculate_statistics(simulations):

    # Crear una lista de todos los puntos únicos
    unique_points = sorted(set(point for simulation in simulations for point in simulation))

    # Crear una matriz para el mapa de calor
    heatmap_data = []
    for simulation in simulations:
        row = [1 if point in simulation else 0 for point in unique_points]
        heatmap_data.append(row)

    # Convertir a array
    heatmap_data = np.array(heatmap_data)

    # Crear el heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, xticklabels=unique_points, cmap="YlGnBu", cbar_kws={'label': 'Uso del punto'})
    plt.ylabel('Simulaciones')
    plt.xlabel('Puntos de acampada')
    plt.title('Mapa de Calor de uso de puntos de acampada en cada simulación')
    plt.show()
    