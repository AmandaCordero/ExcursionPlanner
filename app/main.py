from myapp.utils.map_utils import Map
from myapp.modules.module_1.module_1 import plan_route

# Configurar el mapa
map_data = Map()  # Asume que tienes una clase Map implementada

# for point_id in map_data.interest_points:
#     print('id: ', point_id, ', characteristics: ', map_data.points[point_id].characteristics)

# Definir las preferencias de los turistas
tourist_preferences_1 = [
    [0.6, 0.4, 0, 0.2, 0, 0.9]
]

tourist_preferences_2 = [
    [0.6, 0.4, 0.5, 0.1, 0.8, 0]
]

# Planificar la ruta
route = plan_route(map_data, tourist_preferences_1)

print("Ruta planificada:", route)