import numpy as np

def get_lower_number():
    mean = 0.2  # Media de la distribución
    std_dev = 0.3  # Desviación estándar (ajusta según necesites)
    num_samples = 1  # Número de muestras
    
    samples = np.random.normal(mean, std_dev, num_samples)
    filtered_samples = samples[(samples >= 0)]
    if len(filtered_samples) > 0:
        return filtered_samples[0]
    else:
        return get_lower_number()