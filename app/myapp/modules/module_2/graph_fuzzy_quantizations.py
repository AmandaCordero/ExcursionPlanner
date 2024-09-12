import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Definir el universo del discurso para la variable 'waiting_time'
x_waiting_time = np.arange(0, 61, 1)

# Definir las funciones de membresía para 'waiting_time'
waiting_short = fuzz.trimf(x_waiting_time, [0, 0, 10])
waiting_medium = fuzz.trimf(x_waiting_time, [10, 20, 30])
waiting_long = fuzz.trimf(x_waiting_time, [30, 40, 60])

# Graficar las funciones de membresía
plt.figure(figsize=(8, 6))
plt.plot(x_waiting_time, waiting_short, 'b', label='Short')
plt.plot(x_waiting_time, waiting_medium, 'g', label='Medium')
plt.plot(x_waiting_time, waiting_long, 'r', label='Long')
plt.title('Membership Functions for Waiting Time')
plt.xlabel('Waiting Time (minutes)')
plt.ylabel('Membership Degree')
plt.legend()
plt.grid(True)
plt.show()