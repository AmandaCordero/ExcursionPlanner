import numpy as np

def calculate_statistics(data):
    all_points = [point for sublist in data for point in sublist]
    total_points = len(all_points)
    unique_points = len(set(all_points))
    mean_point = np.mean(all_points)

    median_point = np.median(all_points)
    if len(all_points) > 0:
        mode_point = np.argmax(np.bincount(all_points))  # Punto más común (moda)
        min_point = np.min(all_points)
        max_point = np.max(all_points)
    else:
        mode_point = None
        min_point = None
        max_point = None

    
    return {
        "Total points": total_points,
        "Unique points": unique_points,
        "Mean point": mean_point,
        "Median point": median_point,
        "Mode point": mode_point,
        "Min point": min_point,
        "Max point": max_point
    }